#!/usr/bin/env python
import numpy as np
import subprocess,time

###Main function
def MACE_iter(agent_inputs,gradient_file,N_atoms,gms_agent_ids,atomicMass, gamma, tolerance,iterationcount,q_prev,grad_prev):
  mix = not all(gms_agent_ids)
  agentcount = 0
  agent_outputs = [file for file in agent_inputs]
  q = np.zeros([N_atoms*3, len(agent_inputs)],dtype=np.float64)
  gradient = np.zeros([N_atoms*3, len(agent_inputs)],dtype=np.float64)
  outfiles = []
  for agent in agent_inputs:
      #Generate output filenames
      file_output_tmp = agent.split('.')
      iter = int(file_output_tmp[1])+1
      agent_outputs[agentcount] = file_output_tmp[0] + '.' + str(iter) + '.' + file_output_tmp[2]
      #Read agent coordinates, prepare outputs as arrays 
      with open(agent) as file:
          input = file.read()
          sep = input.split()
          idx = sep.index('$DATA')+5 #Find the $DATA section and begin replacing coordinates at first coordinate
          outfiles.append(input.split()) #initialize data in file to write
          for i in range(0,N_atoms*3):
              q[i,agentcount] = float(sep[idx])
              idx = idx+1
              if ((i+1)%3)==0:
                  idx = idx+2
      #If agent is from GAMESS, read the gradient
      if gms_agent_ids[agentcount]:
          with open(gradient_file[agentcount]) as gradfile:
              grad = gradfile.read()
              idx = 0
              for element in grad.split():
                  gradient[idx,agentcount] = float(element) #0.529177249*float(element)
                  idx += 1
      #Else, agent is assumed to be inertia, compute the gradient.
      else:
          idx = sep.index('$EXPERIMENT') + 1
          MOI = sep[idx:idx+3]
          MOI = np.array([float(element) for element in MOI]).reshape((3,1))
          inertia_index = gms_agent_ids.index(False)
          grad = numerical_gradient_inertia(q[:,inertia_index],q_prev[:,inertia_index],MOI,atomicMass)
          gradient[:,agentcount] = np.nan
          grad_ratio = np.abs(grad.ravel()/np.nanmean(gradient,axis=1))
          grad_ratio[np.isinf(grad_ratio)] = np.nan
          scale = np.nanmean(grad_ratio)
          gradient[:,agentcount] = grad.ravel()/scale
          gradient[np.isnan(gradient)] = 0
          print("This step's gradient is:", gradient)
      agentcount += 1
  ##Update Step    
  q_out, convergence_flag = compute_MACE_step(q,gradient,gamma,tolerance)

  if iterationcount > 0:
        q_prev = q
##Update the coordinates in the output file to those obtained from MACE iteration
  for agentcount in range(0,len(outfiles)):
      idx = outfiles[agentcount].index('$DATA')+5
      for i in range(0,N_atoms*3-1):
          outfiles[agentcount][idx] = q_out[i,agentcount]
          idx += 1
          if (i+1)%3==0:
              idx += 2
      format_GAMESS_input(outfiles[agentcount],agent_outputs[agentcount])
  return q_out, q_prev, gradient, agent_outputs, convergence_flag

###Update function
def compute_MACE_step(q,gradient,gamma,tolerance):
    N_agents = q.shape[1]
    weights = np.ones(N_agents)/N_agents
    Fx = q - gamma*gradient
    v = 2*Fx - q
    Gx = np.average(q,axis=1,weights=weights).reshape((len(q),1))
    Gv = np.average(v,axis=1,weights=weights).reshape((len(q),1))
    q_out = 2*Gv - v
    print("The current state is:")
    print(q)
    print("The change in coordinates is:")
    print(q-q_out)
    print("This step's residuals are:")
    print(np.abs(Fx - Gx))
    #epsilon = np.sum(np.square(Gx - q),axis=0)
    #if epsilon != 0.:
    #  test_weights = 1/epsilon/np.sum(1/epsilon)
    print('Convergence check is:')
    print((np.abs(Fx-Gx))<tolerance)
    if ((np.abs(Fx - Gx))<tolerance).all():
        convergence_flag = True
    else:
        convergence_flag = False
    return q_out, convergence_flag

###Evaluate the numerical gradient of inertia agent.
def numerical_gradient_inertia(r,q_prev,MOI,atomicMass):
  gradient = np.zeros_like(r)
  h = 1e-6
  for idx in range(r.size):
    r_neg = 0.529177249*np.copy(r)
    r_pos = 0.529177249*np.copy(r)
    r_neg[idx] = (r_neg[idx]-h/2) 
    r_pos[idx] = (r_pos[idx]+h/2)
    B_neg = create_B_mat(r_neg,atomicMass)
    B_pos = create_B_mat(r_pos,atomicMass)
    inertiaTensor = np.zeros((3, 3)) 
    inertiaTensor[np.diag_indices_from(inertiaTensor)] = MOI.ravel()
#Commented lines are for the original gradient method; direct evaluation of whole tensor
    F_neg = np.sum(np.square(np.dot(B_neg,r_neg)-inertiaTensor.ravel()))
    F_pos = np.sum(np.square(np.dot(B_pos,r_pos)-inertiaTensor.ravel()))
#Evaluation of only eigenvalues of tensor.
#    F_neg = np.sum(np.square(np.diag(np.linalg.eigvalsh(np.dot(B,r_neg).reshape((3,3)))).ravel()-inertiaTensor.ravel()))
#    F_pos = np.sum(np.square(np.diag(np.linalg.eigvalsh(np.dot(B,r_pos).reshape((3,3)))).ravel()-inertiaTensor.ravel()))
    gradient[idx] = (F_pos - F_neg)/h
  B = create_B_mat(0.529177249*r,atomicMass)
  print('Gradient of inertia is:')
  print(gradient)
  print('Predicted Inertia Tensor:')
  print(np.dot(B,0.529177249*r))
  #print(np.diag(np.linalg.eigvals(np.dot(B,0.529177249*r).reshape((3,3)))))
  return gradient

###Create the operator to calculate inertia.
def create_B_mat(r,atomicMass):
  N_atoms = int(len(r)/3)
  massMat = np.repeat(atomicMass,3).reshape((N_atoms,3))
  masks = np.array([[0,1,1],[0,1,0],[0,0,1],[0,1,0],[1,0,1],[0,0,1],[0,0,1],[0,0,1],[1,1,0]])
  circs = [0,1,2,1,0,1,2,1,0]
  signs = [1,-1,-1,-1,1,-1,-1,-1,1]
  r = r.reshape((N_atoms,3))
  B_mat = np.zeros((int(9),int(3*N_atoms)))
  for i in range(9):
    mask = np.transpose(np.repeat(masks[i],N_atoms).reshape((3,N_atoms)))
    circ = circs[i]
    r_circ = np.roll(r,circ,axis=1)
    B_mat[i,:] = signs[i]*(r_circ*mask*massMat).ravel()
  return B_mat

###Function to run GAMESS agents in parallel.
def mp_gms(agent):
    if agent.split('.')[2]=='inp':
        gms_out = subprocess.run(["./fegms.sh",agent],stdout=subprocess.PIPE)
        return gms_out

###Function to read status of agents.
def parse_state(agent_inputs,N_atoms):
  agentcount = 0
  q = np.zeros([N_atoms*3, len(agent_inputs)],dtype=np.float64)
  gradient = np.zeros([N_atoms*3, len(agent_inputs)],dtype=np.float64)
  outfiles = []
  for agent in agent_inputs:
      #Generate output filenames
      with open(agent) as file:
          input = file.read()
          sep = input.split()
          idx = sep.index('$DATA')+5 #Find the $DATA section and begin replacing coordinates at first coordinate
          for i in range(0,N_atoms*3):
              q[i,agentcount] = float(sep[idx])
              idx = idx+1
              if ((i+1)%3)==0:
                  idx = idx+2
      agentcount += 1
      
  return q

### Function for formatting GAMESS inputs determined by the MACE step 
def format_GAMESS_input(data_to_write, outfilename):
    count = 0
    flag_count = 0
    flag_subcount = 0
    dataflag = 0
    entry_store = ''
    for entry in data_to_write:
        entry = str(entry)
        if dataflag == 1:
            flag_count += 1
            if flag_count >= 3:
                flag_subcount += 1
                entry_store = entry_store + entry + ' '
                if entry != '$END':
                    entry = ''
                if flag_subcount == 5:
                    entry = entry_store + '\n'
                    entry_store = ''
                    flag_subcount = 0
            else:
                entry = entry + '\n'

        if entry=='$DATA':
            dataflag = 1
            entry = ' ' + entry + '\n'
        elif entry=='$END':
            entry = ' ' + entry + '\n'
        else:
            entry = ' ' + entry

        data_to_write[count] = entry
        count += 1

    with open(outfilename, 'w') as file:
        for entry in data_to_write:
            file.write(entry)

###Function to directly evaluate gradient descent on inertia. Deprecated.
def inertia_agent(q,q_prev,MOI,atomicMass):
  gamma = 0.1
  N_atoms = int(len(q)/3)
  sigma = 0.01
  B = create_B_mat(q_prev,atomicMass)
  inertiaTensor = np.zeros((3, 3)) 
  inertiaTensor[np.diag_indices_from(inertiaTensor)] = MOI.ravel()
  gradient = numerical_gradient_inertia(q,q_prev,MOI,atomicMass)
  print('Predicted Inertia Tensor:')
  print(np.dot(B,q))
  q_out = q - gamma*gradient
  #q_out = q.reshape((9,1))+np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(B),B)+sigma*np.identity(9)),np.transpose(B)),np.dot(B,q.reshape((9,1)))-inertiaTensor.reshape(9,1))
  return q_out

###Function to write final structure to a .xyz file for use with RMSD scripts.
def write_xyz(q,atoms,filename):
  q = q*0.52917724
  N_atoms = int(len(q)/3)
  with open(filename+'.xyz','w') as file:
    file.write(str(N_atoms)+'\n')
    file.write('\n')
    for atom in range(N_atoms):
      file.write(str(atoms[atom]) + " " + " ".join([str(item) for item in (q.reshape((N_atoms,3))[atom,:])])+'\n')
