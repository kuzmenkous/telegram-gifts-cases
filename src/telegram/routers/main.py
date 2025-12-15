from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

main_router = Router(name="main_router")


@main_router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    await message.answer("Welcome! This is the start command handler.")
