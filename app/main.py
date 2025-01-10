'''

FastAPI + WebSocket

Небольшой пример работы терминального чата с использованием FastAPI и WebSocket.


Автор: @jesuszwer (https://github.com/jesuszwer)

Первая работа для портфолио.

'''

import uvicorn
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("websocket_logger")

app = FastAPI()

# Словарь для хранения подключенных пользователей
USERS = {}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept() # Принимаем соединение

    try:
        # Подключение нового пользователя
        name = await websocket.receive_text()
        USERS[name] = websocket # Добавляем пользователя в словарь, что бы не потерять его
        logger.info(f"User connected: {name}")
        logger.info(f"Current users: {list(USERS.keys())}") # Выводим список подключенных пользователей

        # Обработка сообщений
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received from {name}: {data}")

            # Отправка сообщений в чат
            for user_name, user_ws in USERS.items():
                await user_ws.send_text(f"{name}: {data}")

    except WebSocketDisconnect:
        # Отключение пользователя
        del USERS[name]
        logger.info(f"User disconnected: {name}")
        logger.info(f"Current users: {list(USERS.keys())}")

    # Обработка ошибок
    except Exception as e:
        logger.error(f"Error with user {name}: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)