
import pytest

from store import RedisStore, InvalidIntegerError


def test_set_and_get():
    db = RedisStore()

    db.set("name", "Anmol")

    assert db.get("name") == "Anmol"


def test_get_missing_key():
    db = RedisStore()

    assert db.get("missing") is None


def test_overwrite():
    db = RedisStore()

    db.set("name", "Anmol")
    db.set("name", "John")

    assert db.get("name") == "John"
    assert db.dbsize() == 1


def test_delete():
    db = RedisStore()

    db.set("name", "Anmol")

    assert db.delete("name") == 1
    assert db.delete("name") == 0
    assert db.get("name") is None


def test_exists():
    db = RedisStore()

    assert db.exists("name") is False

    db.set("name", "Anmol")

    assert db.exists("name") is True


def test_incr():
    db = RedisStore()

    db.set("visits", "10")

    assert db.incr("visits") == 11
    assert db.get("visits") == "11"


def test_incr_missing_key():
    db = RedisStore()

    assert db.incr("visits") == 1
    assert db.get("visits") == "1"


def test_incr_invalid_value():
    db = RedisStore()
    db.set("status", "active")

    with pytest.raises(InvalidIntegerError):
        db.incr("status")

    assert db.get("status") == "active"


def test_incr_overflow():
    db = RedisStore()
    db.set("counter", str(2**63 - 1))

    with pytest.raises(InvalidIntegerError):
        db.incr("counter")

    assert db.get("counter") == str(2**63 - 1)


def test_invalid_value_type():
    db = RedisStore()

    with pytest.raises(TypeError):
        db.set("age", 25)


def test_instances_are_independent():
    db1 = RedisStore()
    db2 = RedisStore()

    db1.set("name", "Anmol")

    assert db2.get("name") is None


# ---------- CLEAR ----------

def test_clear():
    db = RedisStore()

    db.set("a", "1")
    db.set("b", "2")
    db.set("c", "3")

    assert db.clear() == 3
    assert db.dbsize() == 0


def test_clear_empty_database():
    db = RedisStore()

    assert db.clear() == 0


# ---------- MGET ----------

def test_mget():
    db = RedisStore()

    db.set("name", "Anmol")
    db.set("city", "NY")

    result = db.mget(["name", "age", "city"])

    assert result == ["Anmol", None, "NY"]


def test_mget_empty_list():
    db = RedisStore()

    assert db.mget([]) == []


def test_mget_duplicate_keys():
    db = RedisStore()
    db.set("name", "Anmol")

    assert db.mget(["name", "name"]) == [
        "Anmol",
        "Anmol"
    ]


def test_mget_invalid_key():
    db = RedisStore()

    with pytest.raises(TypeError):
        db.mget(["name", 123])


# ---------- DECR ----------

def test_decr():
    db = RedisStore()

    db.set("counter", "10")

    assert db.decr("counter") == 9
    assert db.get("counter") == "9"


def test_decr_missing_key():
    db = RedisStore()

    assert db.decr("counter") == -1
    assert db.get("counter") == "-1"


def test_decr_invalid_value():
    db = RedisStore()
    db.set("counter", "hello")

    with pytest.raises(InvalidIntegerError):
        db.decr("counter")

    assert db.get("counter") == "hello"


def test_decr_underflow():
    db = RedisStore()
    db.set("counter", str(-(2**63)))

    with pytest.raises(InvalidIntegerError):
        db.decr("counter")

    assert db.get("counter") == str(-(2**63))


def test_decr_out_of_range_value():
    db = RedisStore()
    db.set("counter", str(2**63))

    with pytest.raises(InvalidIntegerError):
        db.decr("counter")

    assert db.get("counter") == str(2**63)
