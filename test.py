import asyncio
import time

async def func1():
    print("Starting Asynchronous Operation")
    num = 0
    while num < 5:
        num += 1
        print(num)
        await asyncio.sleep(1)


async def func2():
    num = 10
    while num < 16:
        num += 1
        print(num)
        await asyncio.sleep(2)


def func3():
    print("Starting Linear Operation")
    num = 0
    while num < 5:
        num += 1
        print(num)
        time.sleep(2)


def func4():
    num = 10
    while num < 16:
        num += 1
        print(num)
        time.sleep(2)


async def main():
    await asyncio.gather(func1(), func2())
    func3()
    func4()

if __name__ == '__main__':
    asyncio.run(main())
