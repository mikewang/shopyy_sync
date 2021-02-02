# -*- coding: utf-8 -*-

import datetime, time
from multiprocessing import Pool


global_file_list = ['water1','water2','water3','water4']
thread_count = 0

run_times_limit = 10


def make_mace(file_first):
    agent_index = global_file_list.index(file_first)
    start_time = datetime.datetime.now()
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    global thread_count
    thread_count = thread_count + 1
    print("agent work info , agent_index is", agent_index, "file is ", file_first, start_time_str)
    time.sleep(3)


if __name__ == '__main__':
    run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Beginning MACE job on the following agents:", run_time_str)
    run_times = 1
    done = 0
    while not done:
        run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("iterate:", run_times, run_time_str)
        with Pool(processes=len(global_file_list)) as pool:
            pool.map(make_mace, global_file_list)
        run_times += 1
        if run_times > run_times_limit:
            done = 1
    run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("End MACE job on the following agents:", run_time_str)
    # the end