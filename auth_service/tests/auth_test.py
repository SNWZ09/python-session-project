# импорт пайтеста, настроки которого указаны в pytest.ini
# + тут нужны асинхронные тесты
import pytest

#импорт AsyncClient, async и await работали
from httpx import AsyncClient

# тестовые почта и пароль
test_email = 'test@mailmail.ru'
text_passwd = 'test-passwd'


# проверяем весь процесс (регистрация, логин, получение профиля)
# + узкие места
# так же надо будет проверить, что указаной почты в бд нет (почта должна быть уникальной)
# указываем, что тест асинхронный
@pytest.mark.asyncio
async def test_auth(test_client: AsyncClient):

    # проверяем указанную почту и пароль
    # делаем это в json, мол, реальный пользователь
    # заполнил все на сайте
    # используем post() и assert, как на уроке 5.
    # Production-практики FastAPI. Ошибки и тестирование.
    # Запуск интеграционных тестов с помощью TestClient
    response = await test_client.post(
        '/auth/register', json={'email': test_email, 'password': text_passwd}
    )

    # сервер ответил кодом 200 - круто
    assert response.status_code == 200

    # проверяем, что после всех манипуляций вернулась правильная почта
    assert response.json()['email'] == test_email

    # делаем запрос с такой же почтой
    # должна быть ошибка 409 (пользователь уже сущ.)
    response_email_dublicate = await test_client.post(
        '/auth/register', json={'email': test_email, 'password': text_passwd}
    )
    assert response_email_dublicate.status_code == 409

    # проверяем логин
    # теперь отправляем не в json, а в формате OAuth2
    response_for_login = await test_client.post(
        '/auth/login', data={'username': test_email, 'password': text_passwd}
    )

    # сервер ответил кодом 200 - круто
    assert response_for_login.status_code == 200

    # смотрим, что токен сгенерировался, то есть не пустой
    token = response_for_login.json()['access_token']
    assert token is not None

    # проверим, что логин с неверным паролем возвращает 401
    response_login_with_wrong_pswd = await test_client.post(
        '/auth/login', data={'username': test_email, 'password': 'auaua_wrong_passwd'}
    )

    assert response_login_with_wrong_pswd.status_code == 401

    # смотрим эндпоинт me
    # передаем токен в заголовках
    # смотрим, что сервер узнал тестового юзера по токену и дал правильную почту
    response_for_me = await test_client.get(
        '/auth/me', headers={'Authorization': f'Bearer {token}'}
    )

    assert response_for_me.status_code == 200
    assert response_for_me.json()['email'] == 'test@mailmail.ru'

    # последние два теста
    # запрос к /me без токена - ошибка 401
    response_for_me_without_token = await test_client.get('/auth/me')

    assert response_for_me_without_token.status_code == 401

    # и запрос к /me с неправильным токеном - ошибка 401
    response_for_me_incorr_token = await test_client.get(
        '/auth/me', headers={'Authorization': 'Bearer incorrect_token_sorry'}
    )

    assert response_for_me_incorr_token.status_code == 401
