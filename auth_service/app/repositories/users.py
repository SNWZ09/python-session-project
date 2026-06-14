# берем код из предыдущей работы (llm-p), которую можно найти на моём гитхабе

# реализуем репозиторий пользователей
# тут будут использоваться асинхронные функции,
# которые будут реализовать методы
# получения пользователя по email и по id

# импорт, тк нам понадобится создание SQL-запросов
from sqlalchemy import select

# импорт для асинхронного подключения к БД
from sqlalchemy.ext.asyncio import AsyncSession

# созданная ранее таблица с пользователями
from app.db.models import User


class UserRepository:
    #'Репозиторий должен принимать AsyncSession
    # в конструктор и хранить его как приватное поле.'
    def __init__(self, session: AsyncSession):
        self._session = session

    # в итоге метод вернет либо пользователя (если найдет его
    # по эл. адресу), либо ничего
    async def get_by_email(self, email: str) -> User | None:
        # пишем запрос (ищем по эл. адресу)
        statement = select(User).where(User.email == email)
        # выполняем его
        result = await self._session.execute(statement)
        # получаем результат
        # строчку scalar_one_or_none() подсмотрел,
        # но она даёт то, что нам нужно:
        # либо вернётся - все нормально,
        # либо ноль - тоже нормально,
        # либо несколько - будет ошибка
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        # пишем запрос (ищем по id)
        statement = select(User).where(User.id == user_id)
        # выполняем его
        result = await self._session.execute(statement)
        # получаем результат
        # строчку scalar_one_or_none() подсмотрел,
        # но она даёт то, что нам нужно:
        # либо вернётся - все нормально,
        # либо ноль - тоже нормально,
        # либо несколько - будет ошибка
        return result.scalar_one_or_none()

    # метод создания пользователя
    async def create(self, email: str, password_hash: str) -> User:
        #'В этом файле нельзя хешировать пароль
        # и нельзя создавать JWT'
        user = User(email=email, password_hash=password_hash)

        # добавляем юзера в сессию, сохраняем (INSERT) и обновляем
        # везде await чтобы дождаться ответа от SQLite
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
