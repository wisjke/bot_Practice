import logging
import os
from typing import List, Tuple

from dotenv import load_dotenv
from supabase import create_client, Client


class SupabaseDatabase:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.client: Client = create_client(supabase_url, supabase_key)

    @staticmethod
    def create_tables():
        logging.info("Table creation is managed in Supabase Dashboard or SQL Editor.")

    def add_reminder(self, user_id: int, name: str, birth_date: str,
                     message: str, early_reminder: bool = False, days_before: int = 0):
        try:
            data = {
                "user_id": user_id,
                "name": name,
                "birth_date": birth_date,
                "message": message,
                "early_reminder": early_reminder,
                "days_before": days_before
            }
            response = self.client.table("reminders").insert(data).execute()

        except Exception as e:
            logging.error(f"Error adding reminder: {e}")

    def get_user_reminders(self, user_id: int) -> List[Tuple]:
        try:
            response = self.client.table("reminders").select("*").eq("user_id", user_id).execute()

            # Process data
            data = response.data  # List of dictionaries
            reminders = [(item['name'], item['birth_date'], item['message']) for item in data]
            return reminders
        except Exception as e:
            logging.error(f"Error fetching user reminders: {e}")
            return []

    def get_today_reminders(self, today_date: str) -> List[Tuple]:
        try:
            response = self.client.table("reminders").select("user_id, name, message").filter(
                "birth_date", "like", f"{today_date}%"
            ).execute()

            return [(r["user_id"], r["name"], r["message"]) for r in response.data]
        except Exception as e:
            logging.error(f"Error fetching today's reminders: {e}")
            return []

    def get_early_reminders(self, future_date: str) -> List[Tuple]:
        try:
            response = self.client.table("reminders").select("user_id, name, message, days_before, birth_date").filter(
                "early_reminder", "eq", True).execute()

            early_reminders = [
                (r["user_id"], r["name"], r["message"], r["days_before"])
                for r in response.data
                if r["days_before"] and future_date == (r["birth_date"])
            ]
            return early_reminders
        except Exception as e:
            logging.error(f"Error fetching early reminders: {e}")
            return []

    def delete_reminder(self, user_id: int, name: str, date: str) -> bool:
        try:
            response = self.client.table("reminders").delete().match({
                "user_id": user_id,
                "name": name,
                "birth_date": date
            }).execute()
            return True

        except Exception as e:
            logging.error(f"Error deleting reminder: {e}")
            return False

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
database = SupabaseDatabase(supabase_url, supabase_key)
