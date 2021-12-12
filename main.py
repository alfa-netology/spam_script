import asyncio
import aiosqlite
from aiosmtplib import send
import more_itertools
from email.message import EmailMessage
import os
from dotenv import load_dotenv


async def get_data(sender, hostname, port, username, password):
    messages = []

    async with aiosqlite.connect('data/contacts.db') as db:
        async with db.execute("SELECT first_name, email FROM contacts") as cursor:
            async for row in cursor:

                name, email = row[0], row[1]

                message = EmailMessage()
                message["From"] = sender
                message["To"] = email
                message["Subject"] = 'Hello from spam bot!'
                message.set_content(f'Dear {name}!\nThank you for using our classifieds service.')

                messages.append(
                    send(
                        message,
                        hostname=hostname,
                        port=port,
                        username=username,
                        password=password,
                        start_tls=True
                    )
                )

    return messages


async def main(params):
    data = await get_data(**params)

    for chunk in more_itertools.chunked(data, 10):
        try:
            await asyncio.gather(*chunk, return_exceptions=False)
        except Exception as e:
            print(f'[ERROR] {e}')


if __name__ == '__main__':
    load_dotenv()

    config = {
        'hostname': os.getenv('HOSTNAME'),
        'port': os.getenv('PORT'),
        'sender': os.getenv('SENDER'),
        'username': os.getenv('USER'),
        'password': os.getenv('PASSWORD'),
    }

    asyncio.run(main(config))
