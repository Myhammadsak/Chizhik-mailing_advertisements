import asyncio
from datetime import datetime, time
import pytz
from telethon.sync import TelegramClient
from telethon.errors import ChatWriteForbiddenError, ChannelPrivateError, InviteRequestSentError, \
    UserAlreadyParticipantError, FloodWaitError, InviteHashExpiredError, InviteHashInvalidError
from telethon.tl.functions.channels import JoinChannelRequest
import json

from telethon.tl.functions.messages import ImportChatInviteRequest


with open('../accaunts.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

account = data['myhambara']

API_ID = account['api_id']
API_HASH = account['api_hash']
SESSION_NAME = account['session_name']
GROUPS = account['groups']
MESSAGE = "Аниме"
SCHEDULE_TIME = "15:30"
TIMEZONE = "Europe/Moscow"


async def join_groups(client):
    print("🔹 Начинаю вступление в группы...")

    for invite_link in GROUPS:
        try:
            # Извлекаем хэш из ссылки
            invite_hash = invite_link.split("+")[-1]

            print(f"Пытаюсь вступить: {invite_link}")

            # Пробуем вступить
            await client(ImportChatInviteRequest(invite_hash))
            print(f"✅ Успешно вступил в группу: {invite_link}")

        except UserAlreadyParticipantError:
            print(f"⚠️ Уже состою в группе: {invite_link}")
        except InviteHashExpiredError:
            print(f"❌ Ссылка устарела: {invite_link}")
        except InviteHashInvalidError:
            print(f"❌ Неверная ссылка: {invite_link}")
        except FloodWaitError as e:
            print(f"⏳ Telegram требует подождать {e.seconds} секунд")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"⚠️ Неизвестная ошибка с {invite_link}: {str(e)}")

        # Пауза между попытками
        await asyncio.sleep(10)


async def send_to_group(client, group):
    """Функция для отправки сообщения в группу"""
    try:
        await client.send_message(group, MESSAGE)
        print(f"✅ Сообщение отправлено в {group}")
    except (ChatWriteForbiddenError, ChannelPrivateError):
        print(f"❌ Нет прав на отправку в {group}")
    except Exception as e:
        print(f"⚠️ Ошибка при отправке в {group}: {str(e)}")


async def scheduled_mailing():
    """Основная функция рассылки"""
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    # Сначала вступаем во все группы
    await join_groups(client)

    print("\n🔹 Скрипт запущен. Ожидание времени рассылки...")

    tz = pytz.timezone(TIMEZONE)
    target_time = datetime.strptime(SCHEDULE_TIME, "%H:%M").time()

    while True:
        now = datetime.now(tz).time()

        # Если текущее время >= времени рассылки
        if now >= target_time:
            print("\n🔹 Начинаю рассылку...")
            for group in GROUPS:
                await send_to_group(client, group)
                await asyncio.sleep(30)

            # Ждем 24 часа перед следующей рассылкой
            await asyncio.sleep(86400)
        else:
            # Проверяем каждую минуту
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(scheduled_mailing())