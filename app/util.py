def format_date(date: int) -> str:
    if not date:
        return "Unknown"
    else:
        return str(date)[:4] + "-" + str(date)[4:6] + "-" + str(date)[6:]


def format_nth_place(number: int) -> str:
    if number == 1:
        return "1st"
    elif number == 2:
        return "2nd"
    elif number == 3:
        return "3rd"
    else:
        return str(number) + "th"
