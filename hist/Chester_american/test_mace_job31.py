# -*- coding: utf-8 -*-

import datetime, time
from multiprocessing import Pool
from multiprocessing import Process,Manager
import os
import configparser
import subprocess
import numpy as np
import re

run_times_limit = 10
N_BASIS = 1


def make_inp_file(iteration, file_list, i, q_out):
    file_name = file_list[i]
    f1 = open(file_name, "r")
    content = f1.read()
    f1.close()
    bk_file_name = file_name + "_bk" + str(iteration-1)
    with open(bk_file_name, "w") as f2:
        f2.write(content)
        print("inp文件的备份完成，", bk_file_name)
    # 拆分 按行 数组
    content = content.splitlines()
    # 矩阵处理，成一个 一维数组。

    entries_updated = (q_out.tolist())[i]
    print("*" * 100)
    print("写入inp文件的数组 应该是科学计数格式的字符串")
    # print("q2 is ", entries_updated)

    # for entries in q:
    #     for entry in entries:
    #         entries_updated.append(entry)

    data_begin = False
    temp_content = []
    for line in content:
        if line.__contains__("$END"):
            data_begin = False
            temp_content.append(line)
        else:
            if data_begin and len(entries_updated) > 0:
                entries = line.split("  ")
                col1 = entries.pop(0)
                aline = "  ".join(entries)
                col2 = aline[:1]
                aline = aline[1:]
                row_entries = re.findall(r'.{15}', aline)
                row_entries_new = []
                for row_entry in row_entries:
                    entry_updated = entries_updated.pop(0)
                    ss = np.format_float_scientific(entry_updated, unique=False, precision=8)
                    prefixss = ss[:1]
                    if prefixss != "-":
                        ss = " " + ss
                    row_entries_new.append(ss)
                    print("q len is ", len(ss), "old is ", row_entry, "new is ", ss)
                line = col1 + "  " + col2 + "".join(row_entries_new)
            if line.__contains__("$VEC"):
                data_begin = True
            temp_content.append(line)
    #print(temp_content)
    file_content = "\n".join(temp_content)
    with open(file_name, "w") as f2:
        f2.write(file_content)


def get_agent_filelist():
    config = configparser.ConfigParser()
    config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
    config.read(config_file)
    file_list_str = config.get("agent", "file_list")
    file_list = file_list_str.split(";")
    gamma = config.get("agent", "gamma")
    tolerance = config.get("agent", "tolerance")
    n_basis = config.get("agent", "n_basis")
    # print(file_list)
    return file_list, gamma, tolerance, int(n_basis)


def open_agent_file(file):
    print("file in open_agent_file is", file)
    # 使用 fegms.sh 生成 .out文件，并同时生成一个.dat文件。
    if file.split('.')[2] == 'inp':
        fegms_sh = os.path.normpath(os.path.join(os.curdir, "fegms.sh"))
        gms_out_filename = subprocess.run(["./fegms.sh", file])
        #gms_out_filename = subprocess.run(["./fegms.sh", file], stdout=subprocess.PIPE)
        # generate name.x.dat file for generation of name.x+1.inp
        gms_out_filename = file + ".out"
        return gms_out_filename
    else:
        print("Error file name is wrong.", file)
        return ""


def get_q(file_name, agent_index, q_dict):
    data_lines = []
    data_begin = False

    with open(file_name) as file:
        for line in file:
            if line.__contains__("$END"):
                data_begin = False
            if data_begin:
                entries = line.split("  ")
                del entries[0]
                aline = " ".join(entries)
                aline = aline[1:]
                # print(aline)
                data_lines.append(aline)
            if line.__contains__("$VEC"):
                data_begin = True
    # print all data line
    line_text = "".join(data_lines)
    #getEntries(line_text)
    #print("q1 line text is ", line_text)
    entries = re.findall(r'.{15}', line_text)
    q1 = []
    i = 0
    global N_BASIS
    for entry in entries:
        entry = entry.strip()
        q1.append(entry)
        i += 1
        if i >= N_BASIS*68:
            break
    print("*"*100)
    #print("agent_index is ", agent_index, "q1 array is ", q1)
    q_dict[agent_index] = q1
    return q_dict


def get_dat_gradient(file_name, agent_index, q_dict, gradient_dict, iteration):
    file_name_dat = file_name.replace(".inp", ".dat")
    data_lines = []
    data_begin = False
    #
    file_name_dat = "/scratch/bell/rong10/" + file_name_dat

    f1 = open(file_name_dat, "r")
    content = f1.read()
    f1.close()

    with open(file_name_dat + "_bk" + str(iteration-1), "w") as f2:
        f2.write(content)
        print("dat文件备份完成，", file_name_dat + "_bk" + str(iteration-1))

    with open(file_name_dat) as file:
        for line in file:
            if line.__contains__("$END"):
                data_begin = False
            if data_begin:
                entries = line.split("  ")
                del entries[0]
                aline = " ".join(entries)
                aline = aline[1:]
                # print(aline)
                data_lines.append(aline)
            if line.__contains__("$VEC"):
                data_begin = True
    # print all data line
    line_text = "".join(data_lines)
    #getEntries(line_text)
    entries = re.findall(r'.{15}', line_text)
    q2 = []
    i = 0
    global N_BASIS
    for entry in entries:
        entry = entry.strip()
        q2.append(entry)
        i += 1
        if i >= N_BASIS * 68:
            break

    print("*"*100)
    #print("agent_index is ", agent_index, "q2 array is ", q2)
    # 返回 结果矩阵
    q1 = q_dict[agent_index]

    np_q2 = np.zeros([len(q2)], dtype=np.float64)
    for i in range(len(np_q2)):
        np_q2[i] = np.float64(q2[i])

    np_q1 = np.zeros([len(q1)], dtype=np.float64)
    for i in range(len(np_q1)):
        np_q1[i] = np.float64(q1[i])

    np_gradient = np_q1 - np_q2

    gradient = []
    for i in range(len(np_gradient)):
        v = np_gradient[i]
        ss = np.format_float_scientific(v, unique=False, precision=8)
        gradient.append(ss)

    gradient_dict[agent_index] = gradient
    print("*" * 100)
    #print("agent_index is ", agent_index, "q2-q1 array is ", gradient)
    return gradient_dict


def make_mace(file_list, i, q_dict, gradient_dict, iteration):
    file_name = file_list[i]
    run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print("agent work info , agent_index is", i, "file is ", file_name, run_time_str)
    # create .out file from .inp file
    open_agent_file(file_name)
    # create .gradmatrix from first .out file
    q1 = get_q(file_name, i, q_dict)
    q2 = get_dat_gradient(file_name, i, q_dict, gradient_dict, iteration) # 结果为最终结果，两个矩阵的差。

    run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    #print("agent work info , agent_index is", i, "file is ", current_file, run_time_str)
    #time.sleep(25)


def compute_MACE_step(q, gradient, gamma, tolerance):
    #print("q is", q)
    print("gradient is", gradient)
    print('gamma is ', gamma)
    print('tolerance is', tolerance)
    N_agents = q.shape[1]
    weights = np.ones(N_agents)/N_agents
    tolerance = eval(tolerance)
    gamma = float(gamma)
    Fx = q - gamma*gradient
    v = 2*Fx - q
    Gx = np.average(q, axis=1, weights=weights).reshape((len(q), 1))
    Gv = np.average(v, axis=1, weights=weights).reshape((len(q), 1))
    q_out = 2*Gv - v
    print('iteration is,', iterationcount)
    print("The v:")
    print(v)
    print('Gv is',Gv)
    print('iteration is,', iterationcount)
    print("The current state is:")
    print(q)
    print('Gx is',Gx)
    print('iteration is,', iterationcount)
    print("The change in coordinates is:")
    print(q-q_out)
    print('iteration is,', iterationcount)
    print('updated state is', q_out)
    print("This step's residuals are:")
    print(np.abs(Fx - Gx))
    #epsilon = np.sum(np.square(Gx - q),axis=0)
    #if epsilon != 0.:
    #  test_weights = 1/epsilon/np.sum(1/epsilon)
    print('iteration is,', iterationcount)
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

    # a = np.array([[1, 2], [3, 4], [5, 6]])
    # a_trans = a.transpose()
    # print(a_trans)
    # exit()
    # N_BASIS = 2
    # exit()
    # file_name = "water_631g_mo6.0"
    # q = get_dat_q(file_name,  None, None)
    #
    # file_name = "water_631g_create"
    # create_inp_file(1, file_name, q, None, None)

    # s = "1.28424950E-02"
    # ss = np.float64(s)
    # # sss = np.format_float_scientific(ss, unique=False, precision=8)
    #
    # a = np.array([ss])
    # b = np.array([ss])
    #
    # c = a - b
    # print(len(c), c[0])
    #
    # # print(sss.upper())
    # # print(s)
    # exit()

    # exit()
    #test end.
    # 初始化数据，读取数据文件列表
    iterationcount = 1
    tot_time_gms = 0
    tot_time = 0
    done = 0
    q1 = None
    q2 = None
    manager = Manager()
    q_dict = manager.dict()  # 所有进程可以读写的全局对象，用于并发操作。
    gradient_dict = manager.dict()  # 所有进程可以读写的全局对象，用于并发操作。

    file_list = manager.list()  # 生成一个列表
    # global N_BASIS
    temp_file_list, gamma, tolerance, N_BASIS = get_agent_filelist()
    for file in temp_file_list:
        file_list.append(file)  # 填充文件
    while not done:
        print("file list " + str(iterationcount) + " is ", file_list)
        iter_time_start = time.time()
        run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("iterate " + str(iterationcount) + ":", run_time_str)
        p_list = []
        for i in range(len(file_list)):
            p = Process(target=make_mace, args=(file_list, i, q_dict, gradient_dict, iterationcount))
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
        q1 = np.zeros([m, n], dtype=np.float64)
        for k in q_dict.keys():
            item = q_dict[k]
            for i in range(len(item)):
                q1[k][i] = item[i]
        q2 = np.zeros([m, n], dtype=np.float64)
        for k in gradient_dict.keys():
            item = gradient_dict[k]
            for i in range(len(item)):
                q2[k][i] = item[i]
        q1 = q1.transpose()
        q2 = q2.transpose()
        q_out, convergence_flag = compute_MACE_step(q1, q2, gamma, tolerance)
        q_out = q_out.transpose()
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
            print("Time elapsed: %s seconds" % (time.time() - iter_time_start))
            print("Average time elapsed running GAMESS: %s seconds" % avg_time_gms)
            print("Total time elapsed: %s seconds" % tot_time)
            done = 1
        else:
            if iterationcount == 200:
                done = 1
            # 根据 q_out 生成新的.inp文件。
            run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(" create new inp file BEGIN: " + run_time_str)
            p_list = []
            for i in range(len(file_list)):
                p = Process(target=make_inp_file, args=(iterationcount, file_list, i, q_out))
                p.start()
                p_list.append(p)
            for res in p_list:
                res.join()
            run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(" create new inp file END: " + run_time_str)
    run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("End MACE job on the following agents:", run_time_str)
    # the end


def getEntries(line_text):
    entry = ""
    rows = 1
    cols = 1
    for i in range(len(line_text)):
        entry = entry + line_text[i]
        if len(entry) == 15:
            print(rows, cols, entry)
            entry = ''
            if cols == 68:
                cols = 1
                rows = rows + 1
            else:
                cols = cols + 1
