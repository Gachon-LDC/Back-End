def int_or_0(s: str | None | int):
    if s is None:
        return 0
    try:
        return int(s)
    finally:
        return 0
