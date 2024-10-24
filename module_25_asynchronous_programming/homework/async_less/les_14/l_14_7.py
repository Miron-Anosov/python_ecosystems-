async def say_hello():
    print('Hello!')


async def say_goodbye():
    print('Goodbye!')


async def meet_and_greet():
    await say_hello()
    await say_goodbye()


coro = meet_and_greet()

coro.send(None)

"""
Вызов метода send для нашей сопрограммы запускает все сопрограммы в meet_and_greet. Поскольку нам негде 
приостанавливаться в ожидании результата, весь код выполняется немедленно, даже тот, которому предшествует слово await.
А как заставить сопрограмму приостановиться и проснуться после выполнения медленной операции? Для этого покажем, как 
создать допускающий  ожидание  объект,  чтобы  можно  было  использовать синтаксис await 
вместо основанного на генераторах.
"""