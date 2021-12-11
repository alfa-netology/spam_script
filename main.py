import asyncio
import aiosqlite
from aiosmtplib import send
import more_itertools

HOSTNAME = 'smtp.mail.ru'
PORT = 587
SENDER = 'username@mail.ru'
USERNAME = 'username'
PASSWORD = 'password'

async def get_and_send():
    messages = []
    async with aiosqlite.connect('data/contacts.db') as db:
        async with db.execute("SELECT first_name, email FROM contacts") as cursor:
            async for row in cursor:
                name, email = row[0], row[1]
                message = f'Dear {name}!\nThank you for using our classifieds service.'
                messages.append(
                    send(
                        message,
                        recipients=email,
                        sender=SENDER,
                        hostname=HOSTNAME,
                        port=PORT,
                        username=USERNAME,
                        password=PASSWORD,
                        start_tls=True
                    )
                )

                for chunk in more_itertools.chunked(messages, 10):
                    await asyncio.gather(*chunk)

if __name__ == '__main__':
    asyncio.run(get_and_send())

