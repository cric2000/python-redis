import socket


HOST = "127.0.0.1"
PORT = 6380


def main() -> None:
    with socket.create_connection(
        (HOST, PORT)
    ) as client:

        message = "Hello everyone"

        client.sendall(message.encode("utf-8"))

        response = client.recv(1024)

        print(response.decode("utf-8"))


if __name__ == "__main__":
    main()
