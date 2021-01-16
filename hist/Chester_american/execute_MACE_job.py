#!/usr/bin/env python
import subprocess, argparse, time
import numpy as np
from multiprocessing import Pool
from MACE_module import *

start_time = time.time()
parser = argparse.ArgumentParser()
parser.add_argument('-gamma',default=0.1,help='Step size for gradient descent, default = 0.1.')
parser.add_argument('-tol',default=1e-3,help='Precision in agreement between Fx and Gx, default = 1e-3.')
for i in range(0,10):
  agent_name = '-agent'+ str(i)
  parser.add_argument(agent_name)
args = parser.parse_args()
#Parse args corresponding to agents, ignore agents with no defined input, compile into list.
arg_set = [str(agent) for agent in list(vars(args).values())[2:]]
arg_set = np.array(arg_set)
agents = []
gms_agent_ids = []
for agent in arg_set:
  if agent != 'None':
    agents.append(agent)
  if ('.inp' in agent):
    gms_agent_ids.append(True)
  else:
    gms_agent_ids.append(False)
agent_num = sum(arg_set != 'None')
gms_agent_ids = gms_agent_ids[0:agent_num]
dataflag = False
mix = all(gms_agent_ids)
job_ID = agents[0].split('_')[0] #Assumes _ separates parts of input file, takes the first part as in identifier for the output .xyz equilibrium structure. For example, H2O_HF.0.inp -> H2O.xyz
#Count atoms.  This will be wrong if: 1) symmetry is being used. 2) extra lines exist within the $DATA section.
#Read atomic numbers.
with open(agents[0]) as file:
    atomcount = 0
    elementcount = 0
    atomic_nums = []
    atoms = []
    for line in file:
        entry = line.split()
        if dataflag and entry[0] == '$END':
            dataflag = False
        if dataflag:
            atomcount += 1
            if len(entry)>1:
                atoms.append(entry[0])
                atomic_nums.append(float(entry[1]))
        if entry:
            if entry[0] == '$DATA':
                dataflag = True
    atomcount = (atomcount - 2)
#Approximate nuclear masses
periodic_masses = [1,4,7,9,11,12,14,16,19,20,23,24,27,28,31,32,35,40]
masses = [periodic_masses[int(atomN)-1] for atomN in atomic_nums]
N_atoms = int(atomcount)
gamma = float(args.gamma)
tolerance = float(args.tol)
done = 0
iterationcount = 0
tot_time_gms = 0
tot_time_matlab = 0
tot_time = 0
q_prev = parse_state(agents,N_atoms)
grad_prev = np.zeros_like(q_prev)
print("Beginning MACE job on the following agents:")
print(agents)
print("Atomic masses are:",masses)
print("Running with gamma = %s" % gamma)
print("Tolerance = %s" % tolerance)
while not done:
    iter_time_start = time.time()
    time_gms_start = time.time()
    if __name__ == '__main__':
        with Pool(processes=len(agents)) as pool:
            returncodes = pool.map(mp_gms,agents)
    time_gms = time.time() - time_gms_start
    agent_outputs = [agent + '.out' for agent in agents]
    for agentfile in agent_outputs:
      if agentfile.split('.')[2]=='inp':
        filename = agentfile + ".grad"
        returncode = subprocess.run(["./extract_gradient_args.sh",agentfile,filename])
        if returncode.returncode != 0:
          print("Error extracting gradient from GAMESS output.  Agent in question:")
          print(agentfile)
    gradlist = [agentfile + ".grad" for agentfile in agent_outputs]
    print('grad_prev is:',grad_prev)
    q, q_prev, grad_prev, agents, convergence_flag = MACE_iter(agents,gradlist,N_atoms,gms_agent_ids,masses,gamma,tolerance,iterationcount,q_prev,grad_prev)
    iterationcount += 1
    tot_time_gms = tot_time_gms + time_gms
    iter_time_fin = time.time()-iter_time_start
    tot_time = tot_time + iter_time_fin
    #if iterationcount == 1:
    #    convergence_flag = True
    if convergence_flag:
        if iterationcount == 200:
          print("Max iterations reached.")
        q_equilibrium = np.mean(q,axis=1,keepdims=True)
        if N_atoms == 2:
          distance = q_equilibrium[0]-q_equilibrium[3]
          print("Internuclear distance: %s Angstroms" % distance)
        else:
          print("Final States:")
          print(q)
          print("Final coordinates:")
          print(q_equilibrium.reshape(N_atoms,3))
        avg_time_gms = (tot_time_gms)/iterationcount
        print("Converged in %s iterations." % iterationcount )
        print("Time elapsed: %s seconds" % (time.time() - start_time))
        print("Average time elapsed running GAMESS: %s seconds" % avg_time_gms)
        print("Total time elapsed: %s seconds" % tot_time)
        write_xyz(q_equilibrium,atoms,job_ID) #Write xyz file of result in Angstrom units
        done = 1
