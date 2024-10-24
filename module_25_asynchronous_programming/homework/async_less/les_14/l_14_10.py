import functools
import selectors
import socket
from selectors import BaseSelector

from l_14_8 import CustomFuture


def accept_connection(future: CustomFuture, connection: socket):
    """Установить сокет для чтения и записи в будущем объекте CustomFuture
     когда придет запрос за подключение от клиента.
      Callback функция, которая будет вызвана после подключения клиента."""
    print(f'Получен запрос на подключение от {connection}!')
    future.set_result(connection)  # Устанавливаем результат, в данном случае это будет сокет для чтения.


async def sock_accept(sel: BaseSelector, sock) -> socket:
    """Зарегистрировать в селекторе сокет и ждать запроса на подключение."""
    print('Регистрируется сокет для прослушивания подключений')
    future = CustomFuture()
    # Регистрируем запрос на подключение.
    sel.register(sock, selectors.EVENT_READ, functools.partial(accept_connection, future))
    print('Прослушиваю запросы на подключение...')
    connection: socket = await future  # Отдаем управление, так как реализован метод __await__()
    return connection


async def main(sel: BaseSelector):
    sock = socket.socket()  # Создаем сокет
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Задаем поведение сокета

    sock.bind(('127.0.0.1', 8000))  # Устанавливаем адрес и порт
    sock.listen()  # Запускаем сервер
    sock.setblocking(False)  # Отключаем блокировку сокета

    print('Ожидаю подключения к сокету!')
    connection = await sock_accept(sel, sock)  # Ждать, когда клиент подключится.
    print(f'Получено подключение {connection}!')


selector = selectors.DefaultSelector()  # Создаем селектор

coro = main(selector)  # Создаем сопрограмму.

print('Приложение запущено!')
while True:
    # В бесконечном цикле вызывается метод send() главное сопрограммы
    # при каждом событии селектора выполнять зарегистрированный обратный вызов.
    try:
        state = coro.send(None)  # Продвигаем сопрограмму.

        events = selector.select()  # Выбираем события из селектора, блокирующий вызов.

        for key, mask in events:  # Выбираем события из селектора
            print('Обрабатываются события селектора...')
            callback = key.data  # Извлекаем callback  функции `accept_connection`.
            callback(key.fileobj)  # Вызывает соответствующий обратный вызов, передавая в него объект файла.
    except StopIteration as si:
        print('Приложение завершилось!')
        break

"""
Здесь в начале определена функция `accept_connection`, которая принимает объект `CustomFuture` и клиентский сокет. 
Мы печатаем сообщение о том, что получен запрос на подключение, после чего устанавливаем сокет в качестве значения 
будущего объекта. Следующая функция `sock_accept` принимает серверный сокет и селектор, и регистрирует функцию 
`accept_connection` (привязанную к объекту `CustomFuture`) в качестве обратного вызова для событий чтения в 
серверном сокете. После этого мы ждем будущий объект с помощью `await` и, когда подключение будет 
установлено, возвращаем его. В сопрограмме `main` мы создаем серверный сокет, а затем выполняем `await` 
для сопрограммы `sock_accept` в ожидании подключения. Когда запрос на подключение поступит, мы печатаем сообщение 
и завершаем приложение. Таким образом, мы написали минимально работоспособный цикл событий. Мы создаем экземпляр 
сопрограммы `main`, передаем ему селектор и входим в бесконечный цикл. В цикле первым делом вызываем `send`, чтобы 
продвинуть `main` к первому предложению `await`, а затем вызываем функцию `selector.select`, которая блокирует 
выполнение в ожидании подключения клиента. После этого вызываются зарегистрированные обратные вызовы — в нашем случае 
только `accept_connection`. Как только клиент подключился, мы вызываем `send` во второй раз, при этом все сопрограммы 
снова продвигаются вперед, что дает возможность приложению завершиться.Мы написали простое асинхронное приложение,
используя только ключевые слова `async` и `await`, но не используя `asyncio`! Цикл `while` в конце программы — пример
простого цикла событий, который демонстрирует принцип работы цикла событий в `asyncio`. Разумеется, без задач от 
конкурентности толку будет немного.
"""
