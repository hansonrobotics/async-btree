"""
Utility function.
"""
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterable,
    Awaitable,
    Callable,
    Iterable,
    TypeVar,
    Union,
)


__all__ = ['amap', 'afilter', 'run']

T = TypeVar('T')


async def amap(
    corofunc: Awaitable[Callable[[Any], T]], iterable: Union[AsyncIterable, Iterable]
) -> AsyncGenerator[T, None]:
    """Map an async function onto an iterable or an async iterable.

    # Parameters
    corofunc (Awaitable[Callable[[Any], T]]): coroutine function
    iterable (Union[AsyncIterable, Iterable]): iterable or async iterable collection
        which will be applied.

    # Returns
    AsyncGenerator[T]: an async iterator of corofunc(item)

    # Example
    ```[i async for i in amap(inc, afilter(even, [0, 1, 2, 3, 4]))]```

    """
    if hasattr(iterable, '__aiter__'):
        async for item in iterable:
            yield await corofunc(item)
    else:
        for item in iterable:
            yield await corofunc(item)


async def afilter(
    corofunc: Awaitable[Callable[[T], bool]], iterable: Union[AsyncIterable, Iterable]
) -> AsyncGenerator[T, None]:
    """Filter an iterable or an async iterable with an async function.

    # Parameters
    corofunc (Awaitable[Callable[[T], bool]]): filter async function
    iterable (Union[AsyncIterable, Iterable]): iterable or async iterable collection
        which will be applied.

    # Returns
    (AsyncGenerator[T]): an async iterator of item which satisfy corofunc(item) == True

    # Example
    ```[i async for i in amap(inc, afilter(even, [0, 1, 2, 3, 4]))]```

    """
    if hasattr(iterable, '__aiter__'):
        async for item in iterable:
            if await corofunc(item):
                yield item
    else:
        for item in iterable:
            if await corofunc(item):
                yield item


# pylint: disable=unused-import
try:
    import curio  # noqa: F401
    from contextvars import copy_context

    def run(kernel, target, *args):
        """Curio run with independent contextvars."""
        return copy_context().run(kernel.run, target, *args)


except Exception:  # pylint: disable=bare-except
    # default to asyncio
    from asyncio import run
