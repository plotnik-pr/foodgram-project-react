# Продуктовый помощник "Foodgram"
Удобный сервис для публикации рецептов, с возможностью составить и сохранить список покупок, исходя из выбранных блюд. Реализована состема подписок, чтобы не потерять любимых авторов.

# Для ревью

foodgram-practicum.freedynamicdns.org
Суперюзер:
Почта: admin@mail.ru
Пароль: qwerty123
Обычный юзер:
Почта: user@mail.ru
Палорь: usertest


#### Запуск API проекта на локальном компьютере

- Клонируйте репозиторий github.com/plotnik-pr/foodgram-project-react
- Создайте виртуальное окружение и установите зависимости
```
cd backend
python -m venv venv
. venv/Scripts/activate
pip install --upgade pip
pip install -r -requirements.txt
```
- Установите миграции
```
python manage.py makemigrations
python manage.py migrate
```
- По умолчанию база ингредиентов пуста. Воспользуйтесь скриптом для её наполнения
```
python manage.py loaddata
```
- Запустите сервер
```
python manage.py runserver 
```
### Установка проекта

Приложение запускается при помощи платформы Docker.
Скачайте файл 'docker-compose.production.yml' из репозитория 'github.com/plotnik-pr/foodgram-project-react' и добавьте на ваш сервер в любую пустую папку.
Перед запуском добавьте необходимые переменные окружения в файл '.env' в папке с проектом:
```
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_NAME=foodgram
DB_HOST=db
DB_PORT=5432
SECRET_KEY = 'SECRET_KEY'
DEBUG = 'True'
ALLOWED_HOSTS = 'HOST'
```
Для запуска проекта выполните команду 
```
sudo docker compose -f docker-compose.production.yml up --build 
```

### Доступные эндпоинты

- Ваш IP - главная страница проекта
- Ваш IP/admin/ - страница администратора(суперпользователя)
Вместо Ваш_IP может быть использован домен.

### Авторы

Программисты Яндекс Практикум, Плотник Ульяна (https://github.com/plotnik-pr)