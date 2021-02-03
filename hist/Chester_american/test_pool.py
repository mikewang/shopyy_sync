# -*- coding: utf-8 -*-

import datetime, time
from multiprocessing import Pool
from hist.Chester_american import global_v as gl
import threading


thread_count = 0
global_file_list = ['water.1', 'water.2', 'water.3', 'water.4']
run_times_limit = 10
product = gl.Product()


class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance


def make_mace(file):
    agent_index = global_file_list.index(file)
    start_time = datetime.datetime.now()
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    global thread_count
    thread_count = thread_count + 1
    file_no = int(global_file_list[agent_index].split(".")[1]) + 4
    file_name = global_file_list[agent_index].split(".")[0] + "." + str(file_no)

    global_file_list[agent_index] = file_name
    product.name = file_name
    print("file_name is ", global_file_list[agent_index])
    print("agent work info , agent_index is", agent_index, "file is ", file, start_time_str)
    print("global_file_list is", global_file_list)
    obj1 = Singleton()
    print("Singleton is", obj1)
    time.sleep(3)


def task(arg):
    obj = Singleton()
    time.sleep(3)
    print("Singleton is", arg, obj)


if __name__ == '__main__':
    obj1 = Singleton()
    obj2 = Singleton()
    print(obj1, obj2)
    done = 0
    run_times = 1
    while not done:
        run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("iterate begin:", run_times, run_time_str)
        for i in range(10):
            t = threading.Thread(target=task, args=[i, ])
            t.start()
        run_times += 1
        if run_times > run_times_limit:
            done = 1

    run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Beginning MACE job on the following agents:", run_time_str)
    run_times = 1
    done = 0
    while not done:
        run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("iterate begin:", run_times, run_time_str)
        with Pool(processes=len(global_file_list)) as pool:
            pool.map(make_mace, global_file_list)
        print("iterate  done:", run_times, run_time_str, global_file_list)
        print("product is ", product.name)
        run_times += 1
        if run_times > run_times_limit:
            done = 1
    run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("End MACE job on the following agents:", run_time_str)
    # the end