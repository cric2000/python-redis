from store import RedisStore, InvalidIntegerError


def main() -> None:
    db = RedisStore()

    db.set("name", "Anmol")
    db.set("visits", "12")

    print("Name:", db.get("name"))
    print("Exists:", db.exists("name"))
    print("Visits:", db.incr("visits"))
    print("DB size:", db.dbsize())

    print("Deleted:", db.delete("name"))
    print("Name exists:", db.exists("name"))

    try:
        db.set("status", "active")
        db.incr("status")
    except InvalidIntegerError as exc:
        print("Error:", exc)


if __name__ == "__main__":
    main()
