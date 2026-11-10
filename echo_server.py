import socket


HOST = "127.0.0.1"
PORT = 6380


def main() -> None:
    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as server:

        server.bind((HOST, PORT))
        server.listen()

        print(f"Listening on {HOST}:{PORT}")

        connection, address = server.accept()

        with connection:
            print(f"Connected by {address}")

            while True:
                data = connection.recv(1024)

                if not data:
                    break

                connection.sendall(data)


if __name__ == "__main__":
    main()
