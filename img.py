col = {
    "oq": "⚪",
    "qora": "⚫",
    "qizl": "🔴",
    "ko'k": "🔵",
}


def color(r: str) -> str:
    try:
        return f"{col[r]} {r}"
    except Exception:
        return r
