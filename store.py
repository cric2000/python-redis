
MIN_INT64 = -(2**63)
MAX_INT64 = 2**63 - 1


class InvalidIntegerError(ValueError):
    """Raised when a value cannot be incremented."""


class RedisStore:
    def __init__(self) -> None:
        self._data: dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        self._validate_key(key)

        if not isinstance(value, str):
            raise TypeError("Value must be a string")

        self._data[key] = value

    def get(self, key: str) -> str | None:
        self._validate_key(key)
        return self._data.get(key)

    def delete(self, key: str) -> int:
        self._validate_key(key)

        if key not in self._data:
            return 0

        del self._data[key]
        return 1

    def clear(self) -> int:
        count = len(self._data)
        self._data.clear()
        return count

    def mget(self, keys: list[str]) -> list[str | None]:
        return [self.get(key) for key in keys]

    def decr(self, key: str) -> int:
        self._validate_key(key)

        value = self._data.get(key, "0")

        try:
            number = int(value)
        except ValueError as exc:
            raise InvalidIntegerError(
                "Value is not an integer"
            ) from exc

        if number <= MIN_INT64 or number > MAX_INT64:
            raise InvalidIntegerError(
                "Decrement would exceed signed 64-bit range"
            )

        number -= 1
        self._data[key] = str(number)

        return number

    def exists(self, key: str) -> bool:
        self._validate_key(key)
        return key in self._data

    def dbsize(self) -> int:
        return len(self._data)

    def incr(self, key: str) -> int:
        self._validate_key(key)

        value = self._data.get(key, "0")

        try:
            number = int(value)
        except ValueError as exc:
            raise InvalidIntegerError(
                "Value is not an integer"
            ) from exc

        if number < MIN_INT64 or number >= MAX_INT64:
            raise InvalidIntegerError(
                "Increment would exceed signed 64-bit range"
            )

        number += 1
        self._data[key] = str(number)

        return number

    @staticmethod
    def _validate_key(key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
