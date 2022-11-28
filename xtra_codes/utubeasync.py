import asyncio

async def main():
    print ('tim')
    #await foo('text')
    task =asyncio.create_task (foo('text'))
    await task
    print ('finished')

async def foo(text):
    print (text)
    await asyncio.sleep(.2)

asyncio.run(main())
