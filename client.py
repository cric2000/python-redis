import socket


HOST = "127.0.0.1"
PORT = 6380


def main() -> None:
    with socket.create_connection(
        (HOST, PORT)
    ) as client:

        with client.makefile("rb") as reader:

            print("Connected to Python Redis")
            print("Type EXIT to quit")

            while True:
                command = input("python-redis> ")

                if command.upper() == "EXIT":
                    break

                client.sendall(
                    f"{command}\n".encode("utf-8")
                )

                response = reader.readline()

                if not response:
                    print("Server disconnected")
                    break

                print(
                    response.decode("utf-8").rstrip("\n")
                )


if __name__ == "__main__":
    main()
