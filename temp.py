import asyncio
import aiosmtplib
from email.message import EmailMessage


async def send_mail(sender, to, subject, text):
    hostname = 'smtp.mail.ru'
    port = 587
    user = 'uglin76'
    password = '$51t012@'

    message = EmailMessage()
    message["From"] = sender
    message["To"] = to
    message["Subject"] = subject
    message.set_content(text)

    smtp = aiosmtplib.SMTP(hostname=hostname, port=port)
    await smtp.connect()
    await smtp.starttls()
    await smtp.login(user, password)

    try:
        await smtp.send_message(message)
        print(f'send email to {to}')
    except Exception as e:
        print(e)

    await smtp.quit()

if __name__ == '__main__':
    sender_email = 'uglin76@mail.ru'
    to_email = 'uglin76@mail.ru'
    subject = 'Hi from spam bot'
    text = f'Dear!\nThank you for using our classifieds service.'
    coro1 = send_mail(sender_email, to_email, subject, text)

    to_email = 'prime-alfa@mai_l.ru'
    coro2 = send_mail(sender_email, to_email, subject, text)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(coro1, coro2))

