# -*- coding: utf-8 -*-
import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu,modbus_tcp


def ip(slave=1):
    print("load modbus_tk complete")
    try:
        master = modbus_tcp.TcpMaster()
        master.set_timeout(5.0)
        master.set_verbose(True)
        slave_name = "slave " + str(slave)
        print("-"*10, slave_name, "begin")
        red = master.execute(slave, cst.READ_HOLDING_REGISTERS, 40100, 2)
        print(slave_name + " red is ", red)
        print("-"*10, slave_name, "  end")
        alarm = slave_name + " is ok"
        return list(red), alarm
    except Exception as exc:
        print("*" * 100)
        print(str(exc))
        alarm = (str(exc))
        return [], alarm


if __name__ == "__main__":
    for i in range(0):
        slave = i + 1
        red, alarm = ip(slave=slave)
        print(alarm)
        print(red)
        print("~"*100)
    print("*"*120, "the end")
