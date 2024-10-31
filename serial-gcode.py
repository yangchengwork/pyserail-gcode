#!/usr/bin/env python3

# 使用pyserial-asyncio库，实现异步串口通信，发送G代码
# 2024-10-31
# Gump Yang

import asyncio
import serial_asyncio

async def read_func():
    reader, writer = await serial_asyncio.open_serial_connection(url='/dev/ttyUSB0', baudrate=115200)
    writer.write(b'G28\n')
    data = await reader.read(100)
    print(f'Received: {data.decode()}')
    writer.close()
    await writer.wait_closed()

def main_func():
    # print("Hello, World!")
    # data = await reader.read(100)
    asyncio.run(read_func())

if __name__ == '__main__':
    main_func()