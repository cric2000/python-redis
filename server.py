import socket

from store import RedisStore, InvalidIntegerError


HOST = "127.0.0.1"
PORT = 6380


def execute_command(
    db: RedisStore,
    command: str
) -> str:

    parts = command.split()

    if not parts:
        return "ERROR empty command"

    action = parts[0].upper()
    args = parts[1:]

    try:
        if action == "PING":
            if args:
                return "ERROR wrong number of arguments"
            return "PONG"

        if action == "SET":
            if len(args) != 2:
                return "ERROR expected SET key value"

            db.set(args[0], args[1])
            return "OK"

        if action == "GET":
            if len(args) != 1:
                return "ERROR expected GET key"

            result = db.get(args[0])
            return result if result is not None else "(nil)"

        if action == "DEL":
            if len(args) != 1:
                return "ERROR expected DEL key"

            return str(db.delete(args[0]))

        if action == "EXISTS":
            if len(args) != 1:
                return "ERROR expected EXISTS key"

            return "1" if db.exists(args[0]) else "0"

        if action == "INCR":
            if len(args) != 1:
                return "ERROR expected INCR key"

            return str(db.incr(args[0]))

        if action == "DECR":
            if len(args) != 1:
                return "ERROR expected DECR key"

            return str(db.decr(args[0]))

        if action == "DBSIZE":
            if args:
                return "ERROR wrong number of arguments"

            return str(db.dbsize())

        if action == "CLEAR":
            if args:
                return "ERROR wrong number of arguments"

            return str(db.clear())

        return f"ERROR unknown command: {action}"

    except (InvalidIntegerError, TypeError) as exc:
        return f"ERROR {exc}"


def handle_client(
    connection: socket.socket,
    db: RedisStore
) -> None:

    with connection:
        with connection.makefile(
            "rb"
        ) as reader:

            while True:
                line = reader.readline()

                if not line:
                    break

                try:
                    command = line.decode(
                        "utf-8"
                    ).strip()

                    result = execute_command(
                        db, command
                    )

                except UnicodeDecodeError:
                    result = "ERROR invalid UTF-8"

                response = f"{result}\n".encode(
                    "utf-8"
                )

                connection.sendall(response)


def main() -> None:
    db = RedisStore()

    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as server:

        server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        server.bind((HOST, PORT))
        server.listen()

        print(f"Python Redis listening on {HOST}:{PORT}")

        while True:
            connection, address = server.accept()

            print(f"Client connected: {address}")

            handle_client(connection, db)


if __name__ == "__main__":
    main()
