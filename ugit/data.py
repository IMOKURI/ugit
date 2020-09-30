import hashlib
import os

GIT_DIR = ".ugit"


def init():
    os.makedirs(GIT_DIR)
    os.makedirs(f"{GIT_DIR}/objects")


def update_ref(ref, oid):
    rel_path = f"{GIT_DIR}/{ref}"
    os.makedirs(os.path.dirname(rel_path), exist_ok=True)
    with open(rel_path, "w") as f:
        f.write(oid)


def get_ref(ref):
    rel_path = f"{GIT_DIR}/{ref}"
    if os.path.isfile(rel_path):
        with open(rel_path) as f:
            return f.read().strip()
    return False


def hash_object(data, type_="blob"):
    obj = type_.encode() + b"\x00" + data
    oid = hashlib.sha1(obj).hexdigest()
    with open(f"{GIT_DIR}/objects/{oid}", "wb") as out:
        out.write(obj)
    return oid


def get_object(oid, expected="blob"):
    with open(f"{GIT_DIR}/objects/{oid}", "rb") as f:
        obj = f.read()

    type_, _, content = obj.partition(b"\x00")
    type_ = type_.decode()

    if expected is not None:
        assert type_ == expected, f"Expected {expected}, got {type_}"

    return content
