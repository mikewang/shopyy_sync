from multiprocessing import Process,Manager
import datetime, time
import numpy as np
import os
# 这里实现的就是多个进程之间共享内存，并修改数据
# 这里不需要加锁，因为manager已经默认给你加锁了


def make_mace(file_list, i, q_dict):
    name = file_list[i]
    q_dict[i] = name
    file_no = int(name.split(".")[1]) + len(file_list)
    q_dict[i] = [file_no*0.01, file_no*0.02]
    file_name = name.split(".")[0] + "." + str(file_no)
    file_list[i] = file_name
    print("index=", i, file_name, file_list)
    time.sleep(3)


if __name__ == '__main__':
    manager = Manager()
    file_list = manager.list()  #生成一个列表
    file_list.append("water.1")
    file_list.append("water.2")
    q_dict = manager.dict()
    done = 0
    run_times = 1
    q1 = None
    q2 = None
    while not done:
        p_list = []
        for i in range(len(file_list)):
            p = Process(target=make_mace, args=(file_list, i, q_dict))
            p.start()
            p_list.append(p)
        for res in p_list:
            res.join()
        if q1 is None:
            print(q_dict.keys())
            print(q_dict.items())
            m = len(q_dict.keys())
            item = q_dict.items()[0]
            key = q_dict.keys()[0]
            item = q_dict[key]
            n = len(item)
            print("m,n", m, n)
            q1 = np.zeros([m, n], dtype=np.float64)
            for k in q_dict.keys():
                item = q_dict[k]
                for i in range(len(item)):
                    q1[k][i] = item[i]
        else:
            m = len(q_dict.keys())
            item = q_dict.items()[0]
            key = q_dict.keys()[0]
            item = q_dict[key]
            n = len(item)
            print("m,n", m, n)
            q2 = np.zeros([m, n], dtype=np.float64)
            for k in q_dict.keys():
                item = q_dict[k]
                for i in range(len(item)):
                    q2[k][i] = item[i]
            print("计算 q1", q1)
            print("计算 q2", q2)

            q1 = q2.copy()
            q2 = None
            print("计算 again", q1)
        print("iterator ", run_times, file_list, q_dict)
        run_times += 1
        if run_times >= 10:
            done = 1