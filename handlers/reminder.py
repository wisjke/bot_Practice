import os
from dotenv import load_dotenv
from aiogram import types, Router, F
from datetime import datetime
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from database.models import db
from states.reminder import ReminderStates


router = Router()


@router.message(Command(commands=['newreminder']))
async def cmd_new_reminder(message: types.Message, state: FSMContext):
    await state.set_state(ReminderStates.waiting_for_name)
    await message.answer("✨ Введіть ім'я іменинника/іменинниці:")


@router.message(ReminderStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ReminderStates.waiting_for_date)
    await message.answer(
        "📅 Введіть дату народження у форматі: <b>ДД.ММ.РРРР</b>\n"
        "Наприклад: 25.12.1990",
        parse_mode='HTML'
    )


@router.message(ReminderStates.waiting_for_date)
async def process_date(message: types.Message, state: FSMContext):
    try:
        await state.update_data(date=message.text)
        await state.set_state(ReminderStates.waiting_for_message)
        await message.answer("📝 Напишіть персональне привітання або повідомлення:")

    except ValueError:
        await message.answer("❌ Невірний формат дати. Спробуйте ще раз.\nПриклад: 25.12.1990")


@router.message(ReminderStates.waiting_for_message)
async def process_message(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='✅ Так', callback_data='early_yes'),
            InlineKeyboardButton(text='❌ Ні', callback_data='early_no')
        ]
    ])

    await state.set_state(ReminderStates.waiting_for_early_reminder)
    await message.answer(
        "🎁 Бажаєте отримати нагадування заздалегідь, щоб підготувати подарунок?\n"
        "Виберіть опцію нижче:",
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("early_"))
async def process_early_reminder(callback: CallbackQuery, state: FSMContext):
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
            f"✅ Нагадування створено!\n\n"
            f"👤 Ім'я: {data['name']}\n"
            f"📅 Дата народження: {data['date']}\n"
            f"📝 Повідомлення: {data['message']}"
        )
        await state.clear()
    else:
        await state.set_state(ReminderStates.waiting_for_days_before)
        await callback.message.edit_text(
            "⏳ За скільки днів до дня народження надіслати нагадування?\n"
            "Введіть число від 1 до 30:"
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
                f"✅ Нагадування створено!\n\n"
                f"👤 Ім'я: {data['name']}\n"
                f"📅 Дата народження: {data['date']}\n"
                f"📝 Повідомлення: {data['message']}\n"
                f"⏳ Попереднє нагадування: за {days} днів"
            )
            await state.clear()
        else:
            await message.answer("❌ Будь ласка, введіть число від 1 до 30")
    except ValueError:
        await message.answer("❌ Введіть, будь ласка, коректне число")


@router.message(Command(commands=['myreminders']))
async def cmd_my_reminders(message: Message):
    reminders = db.get_user_reminders(message.from_user.id)

    if not reminders:
        await message.answer("ℹ️ У вас ще немає жодного нагадування")
        return

    for name, date, msg in reminders:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🗑 Видалити",
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

    _, name, date = callback.data.split('_')

    if db.delete_reminder(callback.from_user.id, name, date):
        await callback.message.edit_text(
            f"✅ Нагадування видалено:\n"
            f"🎂 {name} - {date}",
            reply_markup=None
        )
        await callback.answer("Нагадування успішно видалено!")
    else:
        await callback.answer(f'❌ Помилка при видаленні нагадування \nСпробуйте ще раз.', show_alert=True)
