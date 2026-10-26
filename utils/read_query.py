from pathlib import Path


def query(path: str, **kwargs) -> str:
    with open(file=Path(path), mode="r") as q:
        query = q.read().format(**kwargs)
    return query
