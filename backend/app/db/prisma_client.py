from typing import Any


class PrismaFacade:
    """Provides a safe wrapper around Prisma client usage with lazy initialization."""

    def __init__(self) -> None:
        """Initializes facade state without eagerly importing runtime-only dependencies."""

        self._client: Any = None

    async def connect(self) -> None:
        """Connects to Prisma if available, otherwise keeps a no-op fallback mode."""

        if self._client is not None:
            return
        try:
            from prisma import Prisma  # type: ignore

            self._client = Prisma()
            await self._client.connect()
        except Exception:
            self._client = None

    async def disconnect(self) -> None:
        """Disconnects Prisma client when active so shutdown remains clean."""

        if self._client is None:
            return
        await self._client.disconnect()

    @property
    def client(self) -> Any:
        """Exposes the underlying client reference for advanced service operations."""

        return self._client


prisma_facade = PrismaFacade()
