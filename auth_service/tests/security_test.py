# импортируем все функции, которые будем тестировать
# тут все без базы, ФастАПИ и прочего, поэтому асинхронности не будет
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)


# проверка того, как хешируется пароль
def test_password_hashing():
    raw_password = 'password_test_123'

    # хешируем пароль
    hashed = hash_password(raw_password)

    # далее возьму формулировки из задания
    #'хеш не равен исходному паролю'
    assert hashed != raw_password

    #'правильный пароль проходит verify'
    assert verify_password(raw_password, hashed) is True

    #'а неправильный — не проходит'
    assert verify_password('Степа_Люблю_Питон_Мангу_волейбол_игры', hashed) is False


# проверяем генерацию JWT
#'В тесте вы создаёте токен через create_access_token,
# затем декодируете его через decode_token и проверяете,
# что в payload присутствуют sub, role, iat, exp,
# и что sub и role совпадают с теми, что вы передавали.'
def test_jwt_gen():
    user_id = 25598111
    role = 'user'

    # создаем токен
    token = create_access_token(user_id=user_id, role=role)

    # декодируем
    payload = decode_token(token)

    # смотрим пэйлоад
    # если все нормально декодировалось - он не пустой
    assert payload is not None

    # проверяем, что есть все изначальные поля
    assert 'sub' in payload
    assert 'role' in payload
    assert 'iat' in payload
    assert 'exp' in payload

    # проверяем, что sub и role те же, что и были переданы
    assert payload['sub'] == str(user_id)
    assert payload['role'] == role
