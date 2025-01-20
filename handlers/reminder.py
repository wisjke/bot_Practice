from aiogram import types, Router, F
from datetime import datetime
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from database.models import Database
from states.reminder import ReminderStates

db = Database()
router = Router()


@router.message(Command(commands=['newreminder']))
async def cmd_new_reminder(message: types.Message, state: FSMContext):
    await state.set_state(ReminderStates.waiting_for_name)
    await message.answer("Please enter the name of the person:")


@router.message(ReminderStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ReminderStates.waiting_for_date)
    await message.answer(
        "Please enter the birth date in DD.MM.YYYY format:\n"
        "Example: 25.12.1990"
    )


@router.message(ReminderStates.waiting_for_date)
async def process_date(message: types.Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, "%d.%m.%Y")
        await state.update_data(date=message.text)
        await state.set_state(ReminderStates.waiting_for_message)
        await message.answer("Please enter a custom reminder message:")

    except ValueError:
        await message.answer("Invalid date format. Please use DD.MM.YYYY format.\nExample: 25.12.1990")


@router.message(ReminderStates.waiting_for_message)
async def process_message(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='✅', callback_data='early_yes'),
            InlineKeyboardButton(text='❌', callback_data='early_no')
        ]
    ])

    await state.set_state(ReminderStates.waiting_for_early_reminder)
    await message.answer(
        "Would you like to receive an additional reminder before the birthday? "
        "(For example, to buy gifts)",
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("early_"))
async def process_early_reminder(callback:CallbackQuery, state: FSMContext):
    action = callback.data.split('_')[1]
    if action == 'no':
        data = await state.get_data()
        db.add_reminder(
            callback.from_user.id,
            data['name'],
            data['date'],
            data['message']
        )

        await callback.message.edit_text(
            f"Reminder set!\n\n"
            f"Name: {data['name']}\n"
            f"Birth date: {data['date']}\n"
            f"Message: {data['message']}"
        )
        await state.clear()
    else:
        await state.set_state(ReminderStates.waiting_for_days_before)
        await callback.message.edit_text(
            "How many days before the birthday would you like to receive the early reminder?\n"
            "Please enter a number (1-30):"
        )


@router.message(ReminderStates.waiting_for_days_before)
async def process_days_before(message: Message, state: FSMContext):
    try:
        days = int(message.text)
        if 1 <= days <= 30:
            data = await state.get_data()
            db.add_reminder(
                message.from_user.id,
                data['name'],
                data['date'],
                data['message'],
                True,
                days
            )

            await message.answer(
                f"Reminder set!\n\n"
                f"Name: {data['name']}\n"
                f"Birth date: {data['date']}\n"
                f"Message: {data['message']}\n"
                f"Early reminder: {days} days before"
            )
            await state.clear()
        else:
            await message.answer("Please enter a number between 1 and 30.")
    except ValueError:
        await message.answer("Please enter a valid number.")



@router.message(Command(commands=['myreminders']))
async def cmd_my_reminders(message: Message):
    reminders = db.get_user_reminders(message.from_user.id)

    if not reminders:
        await message.answer("You don't have any reminders set.")
        return

    for name, date, msg in reminders:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🗑 Delete",
                callback_data=f"delete_{name}_{date}"
            )]
        ])

        await message.answer(
            f"🎂 {name} - {date}\n"
            f"📝 {msg}",
            reply_markup=keyboard
        )


@router.callback_query(F.data.startswith("delete_"))
async def process_delete_reminder(callback: CallbackQuery):
    # Extract name and date from callback data
    _, name, date = callback.data.split('_')

    # Delete from database
    if db.delete_reminder(callback.from_user.id, name, date):
        # Update the message to show it's deleted
        await callback.message.edit_text(
            f"✅ Deleted reminder:\n"
            f"🎂 {name} - {date}",
            reply_markup=None
        )
        await callback.answer("Reminder deleted successfully!")
    else:
        await callback.answer("Error deleting reminder. Please try again.", show_alert=True)