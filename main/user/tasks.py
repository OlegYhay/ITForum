from django.core.mail import send_mail
from main.celery import app


@app.task
def send_friend_request(username, email):
    send_mail(
        'Вам отправили запрос в друзья:' + username,
        f'Пользователь {username} хочет добавить вас в друзья, зайдите в профиль чтоб принять либо отклонить заявку',
        'olesya198fwaefawfawf@gmail.com',
        [email,],
    )
