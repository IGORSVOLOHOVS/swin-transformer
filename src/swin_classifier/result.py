from typing import TypeVar, Generic, Callable, Any

T = TypeVar("T")
E = TypeVar("E")


class Result(Generic[T, E]):
    """
    A simple Result type for monadic error handling in Python.
    Provides Success(T) or Failure(E).
    """

    def __init__(self, value: T | E, is_success: bool) -> None:
        self._value = value
        self._is_success = is_success

    @property
    def is_success(self) -> bool:
        return self._is_success

    @property
    def is_failure(self) -> bool:
        return not self._is_success

    def unwrap(self) -> T:
        if self._is_success:
            return self._value  # type: ignore
        raise ValueError(f"Called unwrap on Failure: {self._value}")

    def error(self) -> E:
        if not self._is_success:
            return self._value  # type: ignore
        raise ValueError(f"Called error on Success: {self._value}")

    @classmethod
    def success(cls, value: T) -> "Result[T, E]":
        return cls(value, True)

    @classmethod
    def failure(cls, error: E) -> "Result[T, E]":
        return cls(error, False)

    def map(self, fn: Callable[[T], Any]) -> "Result[Any, E]":
        if self._is_success:
            return Result.success(fn(self._value))  # type: ignore
        return Result.failure(self._value)  # type: ignore

    def __repr__(self) -> str:
        return f"Result(success={self._is_success}, value={self._value})"
