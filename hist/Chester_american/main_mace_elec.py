# -*- coding: utf-8 -*-

import sys
import datetime, time
import os
import configparser
import subprocess
import numpy as np
from multiprocessing import Pool

global_file_list = []


def get_agent_filelist():
    config = configparser.ConfigParser()
    config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
    config.read(config_file)
    file_list_str = config.get("agent", "file_list")
    file_list = file_list_str.split(";")
    gamma = config.get("agent", "gamma")
    tolerance = config.get("agent", "tolerance")
    # print(file_list)
    return file_list, gamma, tolerance


def open_agent_file(file):
    print("file in open_agent_file is", file)
    if file.split('.')[2] == 'inp':
        fegms_sh = os.path.normpath(os.path.join(os.curdir, "fegms.sh"))
        gms_out_filename = subprocess.run(["./fegms.sh", file], stdout=subprocess.PIPE)
        # generate name.x.dat file for generation of name.x+1.inp
        gms_out_filename = file + ".out"
        return gms_out_filename
    else:
        print("Error file name is wrong.", file)
        return ""


def get_q(file_name, agent_index):
    file_name_out = file_name + ".out"
    file_name_q = file_name + ".gradmatrix"
    print("get_q", file_name_out, file_name_q)
    extract_gradmatrix_sh = os.path.normpath(os.path.join(os.curdir, "extract_gradmatrix.sh"))
    print("extract_gradmatrix.sh filepath = ", extract_gradmatrix_sh)
    returncode = subprocess.run(["./extract_gradmatrix.sh", file_name_out, file_name_q])
    if returncode.returncode != 0:
        print("Error extracting gradient from GAMESS output.  Agent in question:")
        print(file_name)
        return
    N_orbitals = 0
    with open(file_name_q) as file:
        for line in file:
            N_orbitals = N_orbitals + 1
    # get N_orbitals = 19
    global global_file_list
    agent_count = len(global_file_list)
    print('size of N_orbitals', N_orbitals, "agent_count is ", str(agent_count))
    q = np.zeros([N_orbitals*N_orbitals, agent_count], dtype=np.float64)
    with open(file_name_q) as file:
        j = 0
        for line in file:
            entry = line.split()
            i = 0
            for col_value in entry:
                q[i + N_orbitals*j, agent_index] = col_value
                i = i + 1
            j = j + 1
    print(q)
    return q


def make_mace(file_first):
    agent_index = global_file_list.index(file_first)
    start_time = time.time()
    # create .out file from .inp file
    open_agent_file(file_first)
    # create .gradmatrix from first .out file
    q1 = get_q(file_first, agent_index)
    done = 0
    iterationcount = 0
    tot_time_gms = 0
    tot_time_matlab = 0
    tot_time = 0
    current_file = file_first
    while not done:
        iter_time_start = time.time()
        # get q from second file
        extract_dat_to_inp_sh = os.path.normpath(os.path.join(os.curdir, "extract_dat_to_inp.sh"))
        subprocess.run(["./extract_dat_to_inp.sh"])
        file_num = int(current_file.split('.')[1]) + 1
        file_next = current_file.split('.')[0] + "." + str(file_num) + ".inp"
        if not os.path.isfile(file_next):
            print("Error file is not existed .", file_next)
            break
            return
        # create .out  next file from .inp next file
        open_agent_file(file_next)
        # create .gradmatrix from .out next file
        q2 = get_q(file_next)
        q_out, convergence_flag = compute_MACE_step(q1, q2-q1, gamma, tolerance)
        print("q_out is", q_out)

        iterationcount += 1
        iter_time_fin = time.time() - iter_time_start
        tot_time = tot_time + iter_time_fin
        # if iterationcount == 1:
        #    convergence_flag = True
        if convergence_flag:
            if iterationcount == 200:
                print("Max iterations reached.")
            avg_time_gms = (tot_time_gms) / iterationcount
            print("Converged in %s iterations." % iterationcount)
            print("Time elapsed: %s seconds" % (time.time() - start_time))
            print("Average time elapsed running GAMESS: %s seconds" % avg_time_gms)
            print("Total time elapsed: %s seconds" % tot_time)
            done = 1
        else:
            current_file = file_next
            q1 = q2
            print("current file is", current_file)


def compute_MACE_step(q,gradient,gamma,tolerance):
    print("q is", q)
    print("gradient is", gradient)
    print('gamma is ', gamma)
    print('tolerance is', tolerance)
    N_agents = q.shape[1]
    weights = np.ones(N_agents)/N_agents
    tolerance = eval(tolerance)
    gamma = float(gamma)
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
    print((np.abs(Fx-Gx)) < tolerance)
    if ((np.abs(Fx - Gx)) < tolerance).all():
        convergence_flag = True
    else:
        convergence_flag = False
    return q_out, convergence_flag


if __name__ == '__main__':
    run_time = datetime.datetime.now()
    run_time_str = run_time.strftime('%Y-%m-%d %H:%M:%S')
    print("Beginning MACE job on the following agents:", run_time_str)
    global global_file_list
    global_file_list, gamma, tolerance = get_agent_filelist()
    pool = Pool(len(global_file_list))
    pool.map(make_mace, global_file_list)
    pool.close()
    pool.join()
    run_time_str = run_time.strftime('%Y-%m-%d %H:%M:%S')
    print("End MACE job on the following agents:", run_time_str)
    # the end
