#!/usr/bin/env python3

# 使用pyserial-asyncio库，实现异步串口通信，发送G代码
# 2024-10-31
# Gump Yang

import asyncio
import serial_asyncio
import serial
import argparse

#是否使用syncio方式
asyncio_flag = False # True #
#是否上电复位
poweron_reset = False # True #

async def read_func(lines, port, baudrate):
    reader, writer = await serial_asyncio.open_serial_connection(url=port, baudrate=baudrate)
    for line in lines:
        writer.write(line.encode())
        data = await reader.read(100)
        print(f'send: {line} Received: {data.decode()}')
    writer.close()
    await writer.wait_closed()

def serial_func(gcode:str, ser:serial.Serial):
    ser.write(gcode.encode())
    read = ser.readline()
    print(f'send: {gcode} Received: {read.decode()}')

# 读取命令行参数来确认串口名
def cmd_line():
    args = argparse.ArgumentParser()
    args.add_argument('-p', '--port', type=str, default='COM3', help='串口名')
    args.add_argument('-b', '--baudrate', type=int, default=115200, help='波特率')
    # 这个参数必须要
    args.add_argument('-f', '--file', type=str, required=True, help='G代码文件名')
    return args.parse_args()

def serial_reset(ser:serial.Serial):
    ser.setDTR(True)
    ser.setDTR(False)
    ser.setDTR(True)

    before_len = 0
    while True:
        read = ser.readline()
        if len(read) == 0:
            if before_len == 0:
                break
        before_len = len(read)
        print(f'reset: {read.decode()}')

# 读取gcode G1的数据并减少XY小数点后的位数
def change_gcode_G1(line:str):
    x = float(line.split('X')[1].split('Y')[0])
    y = float(line.split('Y')[1].split(' ')[0])
    # x y都只保留小数点后三位，输出成str
    out_len = f'G1 X{x:.3f} Y{y:.3f}'
    return out_len

def read_gcode(file:str):
    with open(file, 'r') as f:
        file_buf = f.readlines()
    for line in file_buf:
        if line.startswith('G1 X') and ' Y' in line:
            line = change_gcode_G1(line)
            print(line)

def main_func():
    args = cmd_line()
    # 按行读取
    with open(args.file, 'r') as f:
        file_buf = f.readlines()

    if asyncio_flag:
         asyncio.run(read_func(file_buf, args.port, args.baudrate))
    else:
        ser = serial.Serial(args.port, args.baudrate, timeout=1)
        if poweron_reset:
            serial_reset(ser)
        if line.startswith('G1 X') and ' Y' in line:
            line = change_gcode_G1(line)
        for line in file_buf:
            serial_func(line, ser)
        ser.close()

if __name__ == '__main__':
    main_func()
    # read_gcode('out.gcode')
