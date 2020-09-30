def format_date(date: int) -> str:
    if not date:
        return "Unknown"
    else:
        return str(date)[:4] + "-" + str(date)[4:6] + "-" + str(date)[6:]
