# FOODGRAM  «Продуктовый помощник»

 Онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

#### Приложение представляет из себя 4 контейнера:

* web - django  bachend API приложение
* frontend - frontend написанный на React, компилируется и копирует файлы в nginx
* nginx - сервер http сервер объединияющий front и backens
* postgresql - база данных

#### Требуемые приложения для установки (requirements)

Django==2.2.16  
djoser==2.1.0  
pytest==6.2.4  
pytest-pythonpath==0.7.3  
pytest-django==4.4.0  
djangorestframework==3.12.4  
djangorestframework-simplejwt==4.8.0  
Pillow==8.3.1  
PyJWT==2.1.0  
requests==2.26.0  
reportlab  
gunicorn==20.0.4  
psycopg2-binary==2.8.6  
django-filter  

### УСТАНОВКА
Для установки Вам потребуется перейти в папку infra

```cd infra ```

Запуистить сборку проекта

```docker-compose up -d ```

Выполнить миграции:

```docker-compose exec web python manage.py migrate```

Создайте пользователя, администратора сайта

```docker-compose exec web python manage.py createsuperuser```

Загрузиет статические файлы

```docker-compose exec web python manage.py collectstatic --no-input ```


#### Главная страница
Содержимое главной страницы — список первых шести рецептов, отсортированных по дате публикации (от новых к старым). Остальные рецепты доступны на следующих страницах: внизу страницы есть пагинация.
#### Страница рецепта
На странице — полное описание рецепта. Для авторизованных пользователей — возможность добавить рецепт в избранное и в список покупок, возможность подписаться на автора рецепта.
#### Страница пользователя
На странице — имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя.
#### Подписка на авторов
Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.
Сценарий поведения пользователя:
Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке «Подписаться на автора».
Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, опубликованных теми авторами, на которых он подписался. Сортировка записей — по дате публикации (от новых к старым).
При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора».
#### Список избранного
Работа со списком избранного доступна только авторизованному пользователю. Список избранного может просматривать только его владелец.
Сценарий поведения пользователя:
Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.
При необходимости пользователь может удалить рецепт из избранного.
#### Список покупок
Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.

### Примеры запросов

## Пользователи

### /api/users/

#### GET

##### Список пользователей

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| page | query | Номер страницы. | No | integer |
| limit | query | Количество объектов на странице. | No | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

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

### /api/users/

#### POST

##### Регистрация пользователя

```
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |


##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Пользователь успешно создан |
| 400 | 400 Ошибки валидации в стандартном формате DRF  |

```
{
  "email": "vpupkin@yandex.ru",
  "id": 0,
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин"
}
```


### /api/users/{id}/

#### GET

##### Профиль пользователя

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | - |
| 401 | Пользователь не авторизован  |
| 404 | Объект не найден  |

```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": false
}
```

### /api/users/me/

#### GET

##### Текущий пользователь

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | - |
| 401 | Пользователь не авторизован  |

```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": false
}
```


### /api/users/set_password/

#### POST

##### Изменение пароля

```
{
  "new_password": "string",
  "current_password": "string"
}
```

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Пароль успешно изменен |
| 401 | Пользователь не авторизован  |
| 404 | Объект не найден  |


### /api/auth/token/login/

#### POST

##### Получить токен авторизации

```
{
  "password": "string",
  "email": "string"
}
```

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | - |

```
{
  "auth_token": "string"
}
```
### /api/auth/token/logout/

#### POST

##### Удаление токена


##### Responses

| Code | Description |
| ---- | ----------- |
| 204 | - |
| 401 | Пользователь не авторизован  |

## Теги

### /api/tags/

#### GET
##### Cписок тегов

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

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

### /api/tags/{id}/

#### GET
##### Получение тега


##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path | Уникальный идентификатор этого Тега. | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |
| 404 |  |

```
{
  "id": 0,
  "name": "Завтрак",
  "color": "#E26C2D",
  "slug": "breakfast"
}
```
## Рецепты

### /api/recipes/

#### GET
##### Список рецептов

Страница доступна всем пользователям. Доступна фильтрация по избранному, автору, списку покупок и тегам.

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| page | query | Номер страницы. | No | integer |
| limit | query | Количество объектов на странице. | No | integer |
| is_favorited | query | Показывать только рецепты, находящиеся в списке избранного. | No | integer |
| is_in_shopping_cart | query | Показывать только рецепты, находящиеся в списке покупок. | No | integer |
| author | query | Показывать рецепты только автора с указанным id. | No | integer |
| tags | query | Показывать рецепты только с указанными тегами (по slug) | No | [ string ] |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

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

#### POST
##### Создание рецепта

Доступно только авторизованному пользователю

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Рецепт успешно создан |
| 400 | Ошибки валидации в стандартном формате DRF |
| 401 |  |
| 404 |  |

##### Security

| Security Schema | Scopes |
| --- | --- |
| Token | |

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
### /api/recipes/{id}/
#### GET
##### Получение рецепта

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path | Уникальный идентификатор этого Рецепта. | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

```
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
```

#### PATCH
##### Обновление рецепта

Доступно только авторизованному пользователю

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path | Уникальный идентификатор этого Рецепта. | Yes | string |

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

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Рецепт успешно обновлен |
| 400 | Ошибки валидации в стандартном формате DRF, в том числе с внутренними элементами. |
| 401 | Пользователь не авторизован  |
| 403 | Недостаточно прав  |
| 404 | Объект не найден  |

```
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
```

#### DELETE
##### Удаление рецепта

Доступно только авторизованному пользователю

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path | Уникальный идентификатор этого Рецепта. | Yes | string |


##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Рецепт успешно удален |
| 401 | Пользователь не авторизован  |
| 403 | Недостаточно прав  |
| 404 | Объект не найден  |

```
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
```

## Список покупок

### /api/recipes/download_shopping_cart/

#### GET
##### Скачать список покупок

Скачать файл со списком покупок. Это может быть TXT/PDF/CSV. Важно, чтобы контент файла удовлетворял требованиям задания. Доступно только авторизованным пользователям.

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |
| 401 | Пользователь не авторизован |

##### Security

| Security Schema | Scopes |
| --- | --- |
| Token | |


### /api/recipes/{id}/shopping_cart/

#### POST
##### Добавить рецепт в список покупок

Доступно только авторизованным пользователям

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path | Уникальный идентификатор этого рецепта. | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Рецепт успешно добавлен в список покупок |
| 400 | Ошибка добавления в список покупок (Например, когда рецепт уже есть в списке покупок) |
| 401 | Пользователь не авторизован |

```
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
```
##### Security

| Security Schema | Scopes |
| --- | --- |
| Token | |

#### DELETE
##### Удалить рецепт из списка покупок

Доступно только авторизованным пользователям

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path | Уникальный идентификатор этого рецепта. | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 204 | Рецепт успешно удален из списка покупок |
| 400 | Ошибка удаления из списка покупок (Например, когда рецепта там не было) |
| 401 |  |

##### Security

| Security Schema | Scopes |
| --- | --- |
| Token | |

## Избранное

### /api/recipes/{id}/favorite/

#### POST
##### Добавить рецепт в избранное

Доступно только авторизованному пользователю.

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path | Уникальный идентификатор этого рецепта | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Рецепт успешно добавлен в избранное |
| 400 | Ошибка добавления в избранное (Например, когда рецепт уже есть в избранном) |
| 401 |  |

```
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
```

##### Security

| Security Schema | Scopes |
| --- | --- |
| Token | |

#### DELETE
##### Удалить рецепт из избранного

Доступно только авторизованным пользователям

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path | Уникальный идентификатор этого рецепта. | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 204 | Рецепт успешно удален из избранного |
| 400 | Ошибка удаления из избранного (Например, когда рецепта там не было) |
| 401 | Пользователь не авторизован |

##### Security

| Security Schema | Scopes |
| --- | --- |
| Token | |

## Подписки

### /api/users/subscriptions/

#### GET
##### Мои подписки

Возвращает пользователей, на которых подписан текущий пользователь. В выдачу добавляются рецепты.

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| page | query | Номер страницы. | No | integer |
| limit | query | Количество объектов на странице. | No | integer |
| recipes_limit | query | Количество объектов внутри поля recipes. | No | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |
| 401 |  |

```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/subscriptions/?page=4",
  "previous": "http://foodgram.example.org/api/users/subscriptions/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": true,
      "recipes": [
        {
          "id": 0,
          "name": "string",
          "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
          "cooking_time": 1
        }
      ],
      "recipes_count": 0
    }
  ]
}
```

### /api/users/{id}/subscribe/

#### POST
##### Подписаться на пользователя

Доступно только авторизованным пользователям

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path | Уникальный идентификатор этого пользователя. | Yes | string |
| recipes_limit | query | Количество объектов внутри поля recipes. | No | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Подписка успешно создана |
| 400 | Ошибка подписки (Например, если уже подписан или при подписке на себя самого) |
| 401 | Пользователь не авторизован |
| 404 | Объект не найден |

```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": true,
  "recipes": [
    {
      "id": 0,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "cooking_time": 1
    }
  ],
  "recipes_count": 0
}
```

##### Security

| Security Schema | Scopes |
| --- | --- |
| Token | |

#### DELETE
##### Отписаться от пользователя

Доступно только авторизованным пользователям

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path | Уникальный идентификатор этого пользователя. | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 204 | Успешная отписка |
| 400 | Ошибка отписки (Например, если не был подписан) |
| 401 | Пользователь не авторизован |
| 404 | Объект не найден |

##### Security

| Security Schema | Scopes |
| --- | --- |
| Token | |

## Ингредиенты

### /api/ingredients/

#### GET
##### Список ингредиентов

Список ингредиентов с возможностью поиска по имени.

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| name | query | Поиск по частичному вхождению в начале названия ингредиента. | No | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

```
[
  {
    "id": 0,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
```

### /api/ingredients/{id}/

#### GET
##### Получение ингредиента

Уникальный идентификатор этого ингредиента.

##### Параметры

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

```
{
  "id": 0,
  "name": "Капуста",
  "measurement_unit": "кг"
}
```
