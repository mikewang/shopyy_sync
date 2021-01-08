# -*- coding: utf_8 -*-


import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu,modbus_tcp


def mod(PORT="com10"):
    #print("加载modbus_tk 完成")
    red = []
    alarm = ""
    try:
        #设定串口为从站
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT,
        baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)

        #读保持寄存器 03H 1站号 地址2700 长度0-42
        red = master.execute(1, cst.READ_HOLDING_REGISTERS, 2700, 43) #这里可以修改需要读取的功能码
        #print(red)
        alarm="正常"
        return list(red),alarm

    except Exception as exc:
        #print(str(exc))
        alarm = (str(exc))

    return red, alarm      ##如果异常就返回[],故障信息


def ip(ip="11.101.102.180"):
    print("加载modbus_tk 完成")
    red = []
    alarm = ""
    try:
        #设定串口为从站
        master = modbus_tcp.TcpMaster(host=ip)
        master.set_timeout(5.0)
        master.set_verbose(True)
        red = master.execute(1, cst.READ_HOLDING_REGISTERS, 40100, 2) #这里可以修改需要读取的功能码
        #print(red)
        alarm="正常"
        return list(red),alarm

    except Exception as exc:
        #print(str(exc))
        alarm = (str(exc))

    return red, alarm      ##如果异常就返回[],故障信息


if __name__ == "__main__":
    ip()