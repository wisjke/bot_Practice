# Birthday Reminder Bot 🎂

A Telegram bot created with aiogram 3.x and Supabase for birthday reminders. The bot helps you never forget important dates and prepare for celebrations in advance.

## Key Features 🚀

- Create birthday reminders with personalized messages
- Set up early reminders (1-30 days before the event)
- Automatic birthday greeting delivery
- View and manage your reminder list
- Ability to delete reminders

## Tech Stack 💻

- Python 3.12
- aiogram 3.x
- Supabase (PostgreSQL)
- APScheduler
- Docker

## Installation and Setup 🔧

### Prerequisites

- Docker
- Supabase account and project
- Telegram Bot Token

### Environment Variables Setup

Create an `.env` file in the project root with the following variables:

```env
TOKEN_API=your_telegram_bot_token
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t birthday-reminder-bot .
```

2. Run the container:
```bash
docker run -d --env-file .env birthday-reminder-bot
```

### Local Development (without Docker)

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # for Linux/MacOS
venv\Scripts\activate     # for Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the bot:
```bash
python main.py
```

## Bot Usage 🤖

After launching, the bot provides the following commands:

- `/start` - Begin interaction with the bot
- `/newreminder` - Add a new reminder
- `/myreminders` - Display all saved reminders
- `/help` - Get command information

## Project Structure 📁

```
├── database/
│   └── models.py          # Supabase integration
├── handlers/
│   ├── common.py          # Common command handlers
│   └── reminder.py        # Reminder handlers
├── states/
│   └── reminder.py        # FSM states
├── utils/
│   ├── commands.py        # Bot commands configuration
│   ├── scheduler.py       # Reminder scheduler
│   └── validators.py      # Input validation
├── main.py               # Main application file
├── requirements.txt      # Project dependencies
├── Dockerfile           # Docker configuration
└── .env                 # Environment variables
```



## Scheduling ⏰

The bot checks for birthdays and sends reminders daily at 10:00 AM server local time.

## Notes 📝

- Birth dates are stored in DD.MM.YYYY format
- Early reminders can be set from 1 to 30 days before the date
