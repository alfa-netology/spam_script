import asyncio
import aiosqlite
import aiosmtplib
import more_itertools
from email.message import EmailMessage
import os
from dotenv import load_dotenv

"""
С ошибками, о которых писал в комментариях к работе, справился.
Но возникли новые вопросы:
Как прикрутить прогресс бар?
"""

async def send_mail(hostname, port, username, password, message):
    smtp = aiosmtplib.SMTP(hostname=hostname, port=port)
    await smtp.connect()
    await smtp.starttls()
    await smtp.login(username, password)

    try:
        await smtp.send_message(message)
        print(f'send email to {message["To"]}')
    except Exception as e:
        print(f'[ERROR] {e}')

    await smtp.quit()


async def get_data(sender, hostname, port, username, password):
    coros = []

    async with aiosqlite.connect('data/contacts.db') as db:
        async with db.execute("SELECT first_name, email FROM contacts") as cursor:
            async for row in cursor:

                name, email = row[0], row[1]

                message = EmailMessage()
                message["From"] = sender
                message["To"] = email
                message["Subject"] = 'Hello from spam bot!'
                message.set_content(f'Dear {name}!\nThank you for using our classifieds service.')

                coros.append(send_mail(hostname, port, username, password, message))

    return coros


async def main(params):
    data = await get_data(**params)
    for chunk in more_itertools.chunked(data, 10):
        await asyncio.gather(*chunk, return_exceptions=False)


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
