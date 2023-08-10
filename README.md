# Продуктовый помощник "Foodgram"
Удобный сервис для публикации рецептов, с возможностью составить и сохранить список покупок, исходя из выбранных блюд. Реализована состема подписок, чтобы не потерять любимых авторов.

# Для ревью


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

### Авторы

Программисты Яндекс Практикум, Плотник Ульяна (https://github.com/plotnik-pr)