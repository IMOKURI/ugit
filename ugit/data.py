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
    value = None
    if os.path.isfile(rel_path):
        with open(rel_path) as f:
            value = f.read().strip()

    if value and value.startswith("ref:"):
        return get_ref(value.split(":", 1)[1].strip())

    return value


def iter_refs():
    refs = ["HEAD"]
    for root, _, filenames in os.walk(f"{GIT_DIR}/refs/"):
        root = os.path.relpath(root, GIT_DIR)
        refs.extend(f"{root}/{name}" for name in filenames)

    for refname in refs:
        yield refname, get_ref(refname)


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
