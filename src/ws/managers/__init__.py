from abc import ABC, abstractmethod
from typing import Any

from fastapi import WebSocket


class AbstractConnectionManager(ABC):
    @abstractmethod
    async def connect(
        self, websocket: WebSocket, *args: Any, **kwargs: Any
    ) -> None: ...

    @abstractmethod
    async def disconnect(
        self, websocket: WebSocket, *args: Any, **kwargs: Any
    ) -> None: ...

    @abstractmethod
    async def broadcast(self, *args: Any, **kwargs: Any) -> None: ...
