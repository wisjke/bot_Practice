from datetime import datetime


def validate_date(date_text: str) -> bool:
    try:
        user_date = datetime.strptime(date_text, "%d.%m.%Y").date()
    except ValueError:
        raise ValueError("Дата повинна бути у форматі DD.MM.YYYY. Приклад: 27.01.2025")

    today_date = datetime.today().date()

    if user_date > today_date:
        raise ValueError("Дата не може бути у майбутньому.")

    return True
