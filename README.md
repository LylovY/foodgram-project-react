

![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
![](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white)
![](https://github.com/LylovY/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Foodgram - проект, позволяющий публиковать рецепты пользователей. Foodgram поддерживает следующий функционал:

- Публикование рецептов
- Выбор тегов
- Выбор ингредиентов
- Регистрация пользователей

Проект доступен по адресу
http://51.250.78.86


## Пользовательские роли

- Аноним — может просматривать список пользователей, список рецептов, конкретный рецепт и регистрироваться.
- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может просматривать профиль пользователей, публиковать рецепты, добавлять их в лист избранного и в лист для покупок. Эта роль присваивается по умолчанию каждому новому пользователю.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять пользователей, рецепты, теги и ингредиенты. Может назначать роли пользователям.
- Суперюзер Django обладает всеми правами администратора

Frontend на Node.js React общается с Backend на Django при помощи API.

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:LylovY/foodgram-project-react.git
```
BACKEND

```
cd infra
```
Запустить контейнеры:


```
docker-compose up -d
```

Провести миграции в БД:

```
docker-compose exec backend python manage.py migrate
```

Создать Superuser:

```
docker-compose exec backend python manage.py createsuperuser
```

Собрать статику

```
docker-compose exec backend python manage.py collectstatic --no-input
```

Загрузка ингредиентов в базу

```
python3 manage.py csv_to_sql
```



## Примеры работы API

http://localhost/api/users/

GET
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/?page=4",
  "previous": "http://foodgram.example.org/api/users/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": false
    }
  ]
}
```

POST
```
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```
http://localhost/api/tags/

GET
```
[
  {
    "id": 0,
    "name": "Завтрак",
    "color": "#E26C2D",
    "slug": "breakfast"
  }
]
```


http://localhost/api/recipes/


GET
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

POST
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

PATCH
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

http://localhost/api/recipes/{id}/favorite/

POST
```
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
```


http://localhost/api/ingredients/

GET
```
[
  {
    "id": 0,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
```
