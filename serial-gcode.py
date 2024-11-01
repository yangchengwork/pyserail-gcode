#!/usr/bin/env python3

# 使用pyserial-asyncio库，实现异步串口通信，发送G代码
# 2024-10-31
# Gump Yang

import asyncio
import serial_asyncio
import serial
import argparse

#是否使用syncio方式
asyncio_flag = False

async def read_func(gcode:str):
    reader, writer = await serial_asyncio.open_serial_connection(url='/dev/ttyUSB0', baudrate=115200)
    writer.write(gcode.encode())
    data = await reader.read(100)
    print(f'Received: {data.decode()}')
    writer.close()
    await writer.wait_closed()

def serial_func(gcode:str, ser:serial.Serial):
    ser.write(gcode.encode())
    read = ser.readline()
    print(f'Received: {read.decode()}')

# 读取命令行参数来确认串口名
def cmd_line():
    args = argparse.ArgumentParser()
    args.add_argument('-p', '--port', type=str, default='COM3', help='串口名')
    args.add_argument('-b', '--baudrate', type=int, default=115200, help='波特率')
    # 这个参数必须要
    args.add_argument('-f', '--file', type=str, required=True, help='G代码文件名')
    return args.parse_args()

def main_func():
    args = cmd_line()
    # 按行读取
    with open(args.file, 'r') as f:
        file_buf = f.readlines()

    if asyncio_flag:
        for line in file_buf:
            asyncio.run(read_func(line))
    else:
        ser = serial.Serial(args.port, args.baudrate, timeout=10)
        for line in file_buf:
            serial_func(line, ser)
        ser.close()

if __name__ == '__main__':
    main_func()