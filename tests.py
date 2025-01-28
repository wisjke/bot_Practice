from database.models import database


db = database


res = db.get_early_reminders("28.01")

print(res)