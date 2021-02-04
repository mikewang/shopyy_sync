# -*- coding: utf-8 -*-

import datetime, time
from multiprocessing import Pool
from multiprocessing import Process,Manager
import os
import configparser
import subprocess
import numpy as np

run_times_limit = 10


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
        #gms_out_filename = subprocess.run(["./fegms.sh", file], stdout=subprocess.PIPE)
        gms_out_filename = os.system('./fegms.sh ' + file)
        # generate name.x.dat file for generation of name.x+1.inp
        gms_out_filename = file + ".out"
        return gms_out_filename
    else:
        print("Error file name is wrong.", file)
        return ""


def get_q(file_name, agent_index, q_dict):
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
    print('size of N_orbitals', N_orbitals - 1)
    q = []
    with open(file_name_q) as file:
        for line in file:
            entry = line.split()
            for col_value in entry:
                q.append(col_value)
    print(q)
    q_dict[agent_index] = q
    return q_dict


def make_mace(file_list, i, q_dict):
    file_name = file_list[i]
    run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("agent work info , agent_index is", i, "file is ", file_name, run_time_str)
    # create .out file from .inp file
    open_agent_file(file_name)
    # create .gradmatrix from first .out file
    q1 = get_q(file_name, i, q_dict)

    # get q from second file
    current_file = file_name
    extract_dat_to_inp_sh = os.path.normpath(os.path.join(os.curdir, "extract_dat_to_inp.sh"))
    subprocess.run(["./extract_dat_to_inp.sh"])
    file_num = int(current_file.split('.')[1]) + 1
    file_next = current_file.split('.')[0] + "." + str(file_num) + ".inp"
    if not os.path.isfile(file_next):
        print("Error file is not existed .", file_next)
    file_list[i] = file_next
    print("set after", i, file_list[i])
    run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print("agent work info , agent_index is", i, "file is ", current_file, run_time_str)
    time.sleep(3)


def compute_MACE_step(q, gradient, gamma, tolerance):
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
    run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Beginning MACE job on the following agents:", run_time_str)
    # 初始化数据，读取数据文件列表
    iterationcount = 1
    tot_time_gms = 0
    tot_time = 0
    done = 0
    q1 = None
    q2 = None
    manager = Manager()
    q_dict = manager.dict()
    file_list = manager.list()  # 生成一个列表
    temp_file_list, gamma, tolerance = get_agent_filelist()
    for file in temp_file_list:
        file_list.append(file)  # 填充文件
    while not done:
        print("file list " + str(iterationcount) + " is ", file_list)
        iter_time_start = time.time()
        run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("iterate " + str(iterationcount) + ":", run_time_str)
        p_list = []
        for i in range(len(file_list)):
            p = Process(target=make_mace, args=(file_list, i, q_dict))
            p.start()
            p_list.append(p)
        for res in p_list:
            res.join()
        run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("iterate run " + str(iterationcount) + ":", run_time_str)
        m = len(q_dict.keys())
        item = q_dict.items()[0]
        key = q_dict.keys()[0]
        item = q_dict[key]
        n = len(item)
        print("q size is m,n", m, n)
        if q1 is None:
            q1 = np.zeros([m, n], dtype=np.float64)
            for k in q_dict.keys():
                item = q_dict[k]
                for i in range(len(item)):
                    q1[k][i] = item[i]
        else:
            q2 = np.zeros([m, n], dtype=np.float64)
            for k in q_dict.keys():
                item = q_dict[k]
                for i in range(len(item)):
                    q2[k][i] = item[i]
            q_out, convergence_flag = compute_MACE_step(q1, q2 - q1, gamma, tolerance)
            iterationcount += 1
            iter_time_fin = time.time() - iter_time_start
            tot_time = tot_time + iter_time_fin
            # if iterationcount == 1:
            #    convergence_flag = True
            if convergence_flag:
                if iterationcount == 20:
                    print("Max iterations reached.")
                avg_time_gms = (tot_time_gms) / iterationcount
                print("Converged in %s iterations." % iterationcount)
                print("Time elapsed: %s seconds" % (time.time() - iter_time_start))
                print("Average time elapsed running GAMESS: %s seconds" % avg_time_gms)
                print("Total time elapsed: %s seconds" % tot_time)
                done = 1
            else:
                q1 = q2.copy()
                q2 = None
    run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("End MACE job on the following agents:", run_time_str)
    # the end