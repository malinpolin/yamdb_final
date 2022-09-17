REST API YamDB - база отзывов о фильмах, музыке и книгах
![yamdb workflow](https://github.com/malinpolin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Описание

Финальный проект 10-го спринта "API".

Выполнили:
- [Сергей Патрушев](https://github.com/iPatrushevSergey)

- [Ольга Хомутова](https://github.com/Oborotistova)

- [Полина Стрельникова](https://https://github.com/malinpolin)


## Результат

Проект **YaMDb** собирает **отзывы (Review)** пользователей на **произведения (Titles)**. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список **категорий (Category)** может быть расширен администратором.
Сами произведения в **YaMDb** не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведению может быть присвоен **жанр (Genre)** из списка предустановленных. Новые жанры может создавать только администратор.
Пользователи оставляют к произведениям текстовые **отзывы (Review)** и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — **рейтинг** (целое число). На одно произведение пользователь может оставить только один отзыв.


## Пользовательские роли

- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь (user)** — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять **свои** отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор (moderator)** — те же права, что и у **Аутентифицированного пользователя** плюс право удалять **любые** отзывы и комментарии.
- **Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- **Суперюзер Django** — обладет правами администратора (admin)


## Установка:

### 1. Клонировать репозиторий в рабочую директорию на компьютере:

##### Linux или MacOS
```bash
git clone git@github.com:malinpolin/infra_sp2.git
```
##### Windows
```bash
git clone https://github.com/malinpolin/infra_sp2.git
```

### 2. Создать .env файл в директории infra/, в котором должны содержаться следующие переменные:

>DB_ENGINE=django.db.backends.postgresql
>
>DB_NAME= # имя базы данных
>
>POSTGRES_USER= # логин для подключения к базе данных
>
>POSTGRES_PASSWORD= # пароль для подключения к БД (установите свой)
>
>DB_HOST=db
>
>DB_PORT=5432


### 3. Перейти в папку infra/ и собрать образ:

```bash
docker-compose up -d --build
```

### 4. Выполнить миграции:

```bash
docker-compose exec web python manage.py migrate
```

### 5. Соберать статику:

```bash
docker-compose exec web python manage.py collectstatic --no-input
```

### 6. Для доступа к админке создать суперюзера:

```bash
docker-compose exec web python manage.py createsuperuser
```

## Алгоритм регистрации пользователей

1. Пользователь отправляет POST-запрос на эндпоинт /api/v1/auth/signup/

*Обязательные поля*: **email, username**

> Тело запроса:
>```json
>{
>  "email": "user@example.com",
>  "username": "string",
>}
>```

2. YaMDB отправляет письмо с кодом подтверждения **(confirmation_code)** на адрес **email**.

3. Пользователь отправляет POST-запрос на эндпоинт /api/v1/auth/token/

*Обязательные поля*: **username, confirmation_code**

> Тело запроса:
>```json
>{
>  "username": "string",
>  "confirmation_code": "string",
>}
>```

> Ответ:
>```json
>{
>  "token": "string"
>}

4. При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание — в документации).


## Примеры

### 1. Получение списка всех категорий:
GET-запрос /api/v1/categories/

Права доступа: **Доступно без токена**

> Ответ:
>```json
>{
>  "count": 0,
>  "next": "string",
>  "previous": "string",
>  "results": [
>    {
>      "name": "string",
>      "slug": "string"
>    }
>  ]
>}
>```

### 2. Добавление новой категории:
POST-запрос /api/v1/categories/

Права доступа: **Администратор**

*Обязательные поля*: **name, slug**

> Тело запроса:
>```json
>{
>  "name": "string",
>  "slug": "string"
>}
>```

### 3. Удаление категории:
DELETE-запрос /api/v1/categories/{slug}/

Права доступа: **Администратор**

*Обязательные параметры*: **slug**


### 4. Получение списка всех жанров:
GET-запрос /api/v1/genres/

Права доступа: **Доступно без токена**

> Ответ:
>```json
>{
>  "count": 0,
>  "next": "string",
>  "previous": "string",
>  "results": [
>    {
>      "name": "string",
>      "slug": "string"
>    }
>  ]
>}
>```

### 5. Добавление жанра:
POST-запрос /api/v1/genres/

Права доступа: **Администратор**

*Обязательные поля*: **name, slug**

> Тело запроса:
>```json
>{
>  "name": "string",
>  "slug": "string"
>}
>```

### 6. Удаление жанра:
DELETE-запрос /api/v1/genres/{slug}/

Права доступа: **Администратор**

*Обязательные параметры*: **slug**

### 7. Получение списка всех произведений:
GET-запрос /api/v1/titles/

Права доступа: **Доступно без токена**

> Ответ:
>```json
>{
>  "count": 0,
>  "next": "string",
>  "previous": "string",
>  "results": [
>    {
>      "id": 0,
>      "name": "string",
>      "year": 0,
>      "rating": 0,
>      "description": "string",
>      "genre": [
>        {
>          "name": "string",
>          "slug": "string"
>        }
>      ],
>      "category": [
>        {
>          "name": "string",
>          "slug": "string"
>        }
>      ]
>    }
>  ]
>}
>```

### 8. Добавление произведения:
POST-запрос /api/v1/titles/

Права доступа: **Администратор**

*Обязательные поля*: **name, year, genre, category**

> Тело запроса:
>```json
>{
>  "name": "string",
>  "year": 0,
>  "description": "string",
>  "genre": [
>    "string"
>  ],
>  "category": "string"
>}
>```

### 9. Получение информации о произведении:
GET-запрос /api/v1/titles/{title_id}/

Права доступа: **Доступно без токена**

*Обязательные параметры*: **title_id**

> Ответ:
>```json
>{
>  "id": 0,
>  "name": "string",
>  "year": 0,
>  "rating": 0,
>  "description": "string",
>  "genre": [
>    {
>      "name": "string",
>      "slug": "string"
>    }
>  ],
>  "category": [
>    {
>      "name": "string",
>      "slug": "string"
>    }
>  ]
>}
>```

### 10. Частичное обновление информации о произведении:
PATCH-запрос /api/v1/titles/{title_id}/

Права доступа: **Администратор**

*Обязательные параметры*: **title_id**

*Обязательные поля*: **name, year, genre, category**

> Тело запроса:
>```json
>{
>  "name": "string",
>  "year": 0,
>  "description": "string",
>  "genre": [
>      "string"
>  ],
>  "category": "string",
>}
>```

### 11. Удаление произведения:
DELETE-запрос /api/v1/titles/{title_id}/

Права доступа: **Администратор**

*Обязательные параметры*: **title_id**

### 12. Получение списка всех отзывов:
GET-запрос /api/v1/titles/{title_id}/reviews/

Права доступа: **Доступно без токена**

*Обязательные параметры*: **title_id**

> Ответ:
>```json
>{
>  "count": 0,
>  "next": "string",
>  "previous": "string",
>  "results": [
>    {
>      "id": 0,
>      "text": "string",
>      "author": "string",
>      "score": 1,
>      "pub_date": "2019-08-24T14:15:22Z"
>    }
>  ]
>}
>```

### 13. Добавление нового отзыва:
POST-запрос /api/v1/titles/{title_id}/reviews/

Права доступа: **Аутентифицированные пользователи**

*Обязательные параметры*: **title_id**

*Обязательные поля*: **text, score**

> Тело запроса:
>```json
>{
>  "text": "string",
>  "score": 1
>}
>```

### 14. Полуение отзыва по id:
GET-запрос /api/v1/titles/{title_id}/reviews/{review_id}/

Права доступа: **Доступно без токена**

*Обязательные параметры*: **title_id, review_id**

> Ответ:
>```json
>{
>  "id": 0,
>  "text": "string",
>  "author": "string",
>  "score": 1,
>  "pub_date": "2019-08-24T14:15:22Z"
>}
>```

### 15. Частичное обновление отзыва по id:
PATCH-запрос /api/v1/titles/{title_id}/reviews/{review_id}/

Права доступа: **Автор отзыва, модератор или администратор**

*Обязательные параметры*: **title_id, review_id**

*Обязательные поля*: **text, score**

> Тело запроса:
>```json
>{
>  "text": "string",
>  "score": 1
>}
>```

### 16. Удаление отзыва по id:
DELETE-запрос /api/v1/titles/{title_id}/reviews/{review_id}/

Права доступа: **Автор отзыва, модератор или администратор**

*Обязательные параметры*: **title_id, review_id**

### 17. Получение списка всех комментариев к отзыву:
GET-запрос /api/v1/titles/{title_id}/reviews/{review_id}/comments/

Права доступа: **Доступно без токена**

*Обязательные параметры*: **title_id, review_id**

> Ответ:
>```json
>{
>  "count": 0,
>  "next": "string",
>  "previous": "string",
>  "results": [
>    {
>      "id": 0,
>      "text": "string",
>      "author": "string",
>      "pub_date": "2019-08-24T14:15:22Z"
>    }
>  ]
>}
>```

### 18. Добавление комментария к отзыву:
POST-запрос /api/v1/titles/{title_id}/reviews/{review_id}/comments/

Права доступа: **Аутентифицированные пользователи**

*Обязательные параметры*: **title_id, review_id**

*Обязательные поля*: **text**

> Тело запроса:
>```json
>{
>  "text": "string",
>}
>```

### 19. Получение комментария к отзыву:
GET-запрос /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

Права доступа: **Доступно без токена**

*Обязательные параметры*: **title_id, review_id, comment_id**

> Ответ:
>```json
>{
>  "id": 0,
>  "text": "string",
>  "author": "string",
>  "pub_date": "2019-08-24T14:15:22Z"
>}
>```

### 20. Частичное обновление комментария к отзыву:
PATCH-запрос /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

Права доступа: **Автор комментария, модератор или администратор**

*Обязательные параметры*: **title_id, review_id, comment_id**

*Обязательные поля*: **text**

> Тело запроса:
>```json
>{
>  "text": "string",
>}
>```

### 21. Удаление комментария к отзыву:
DELETE-запрос /api/v1/titles/{title_id}/reviews/{review_id}/

Права доступа: **Автор комментария, модератор или администратор**

*Обязательные параметры*: **title_id, review_id, comment_id**

### 22. Получение списка всех пользователей:
GET-запрос /api/v1/users/

Права доступа: **Администратор**

> Ответ:
>```json
>{
>  "count": 0,
>  "next": "string",
>  "previous": "string",
>  "results": [
>    {
>      "username": "string",
>      "email": "user@example.com",
>      "first_name": "string",
>      "last_name": "string",
>      "bio": "string",
>      "role": "user"
>    }
>  ]
>}
>```

### 23. Добавление пользователя:
POST-запрос /api/v1/users/

Права доступа: **Администратор**

*Обязательные поля*: **username, email**

> Тело запроса:
>```json
>{
>  "username": "string",
>  "email": "user@example.com",
>  "first_name": "string",
>  "last_name": "string",
>  "bio": "string",
>  "role": "user"
>}
>```

### 24. Получение пользователя по username:
GET-запрос /api/v1/users/{username}/

Права доступа: **Администратор**

*Обязательные параметры*: **username**

> Ответ:
>```json
>{
>  "username": "string",
>  "email": "user@example.com",
>  "first_name": "string",
>  "last_name": "string",
>  "bio": "string",
>  "role": "user"
>}
>```

### 25. Изменение данных пользователя по username:
PATCH-запрос /api/v1/users/{username}/

Права доступа: **Администратор**

*Обязательные параметры*: **username**

*Обязательные поля*: **username, email**

> Тело запроса:
>```json
>{
>  "username": "string",
>  "email": "user@example.com",
>  "first_name": "string",
>  "last_name": "string",
>  "bio": "string",
>  "role": "user"
>}
>```

### 26. Удаление пользователя по username:
DELETE-запрос /api/v1/users/{username}/

Права доступа: **Администратор**

*Обязательные параметры*: **username**

### 27. Получение данных своей учетной записи:
GET-запрос /api/v1/users/me/

Права доступа: **Любой авторизованный пользователь**

> Ответ:
>```json
>{
>  "username": "string",
>  "email": "user@example.com",
>  "first_name": "string",
>  "last_name": "string",
>  "bio": "string",
>  "role": "user"
>}
>```

### 28. Изменение данных своей учетной записи:
PATCH-запрос /api/v1/users/me/

Права доступа: **Любой авторизованный пользователь**

*Обязательные поля*: **username, email**

> Тело запроса:
>```json
>{
>  "username": "string",
>  "email": "user@example.com",
>  "first_name": "string",
>  "last_name": "string",
>  "bio": "string",
>}
>```

