import asyncio

async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    

    for i in range(5):


        await asyncio.sleep(1 / power)
        print(f'Силач {name} поднял шар номер {i + 1}')
    print(f'Силач {name} закончил соревнования')

async def start_tournment():
    task1 = asyncio.create_task(start_strongman('Misha', 2))
    task2 = asyncio.create_task(start_strongman('Masha', 1))
    task3 = asyncio.create_task(start_strongman('Vitya', 5))
    await task1
    await task2
    await task3


asyncio.run(start_tournment())