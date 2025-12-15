import asyncio

from faststream import FastStream

from src.adapters.broker import broker
from src.telegram import handlers as handlers
from src.telegram.loader import bot, dispatcher, storage
from src.telegram.routers.main import main_router

app = FastStream(broker)


@app.on_startup
async def startup_event() -> None:
    for router in (main_router,):
        dispatcher.include_router(router)
    asyncio.create_task(dispatcher.start_polling(bot))  # noqa: RUF006


@app.on_shutdown
async def shutdown_event() -> None:
    await bot.close()
    await storage.close()
