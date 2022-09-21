![yamdb workflow](https://github.com/malinpolin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

API развернут по адресу http://158.160.5.214/api/v1/

# CI и CD проекта api_yamdb.

## Описание

Настроены для приложения Continuous Integration и Continuous Deployment: автоматический запуск тестов, обновление образов на Docker Hub, автоматический деплой на боевой сервер при пуше в главную ветку main.

Проект Yamdb_final создан для демонстрации методики DevOps (Development Operations) и идеи Continuous Integration (CI),
суть которых заключается в интеграции и автоматизации следующих процессов:
* синхронизация изменений в коде
* сборка, запуск и тестерование приложения в среде, аналогичной среде боевого сервера
* деплой на сервер после успешного прохождения всех тестов
* уведомление об успешном прохождении всех этапов

Само приложение взято из проекта [api_yamdb](https://github.com/malinpolin/api_yamdb), который представляет собой API сервиса отзывов о фильмах, книгах и музыке.
Зарегистрированные пользователи могут оставлять отзывы (Review) на произведения (Title).
Произведения делятся на категории (Category): «Книги», «Фильмы», «Музыка». 
Список категорий может быть расширен администратором. Приложение сделано с помощью Django REST Framework.

Для Continuous Integration в проекте используется облачный сервис GitHub Actions.
Для него описана последовательность команд (workflow), которая будет выполняться после события push в репозиторий.


## Установка:

### 1. Клонировать репозиторий в рабочую директорию на компьютере:

##### Linux или MacOS
```bash
git clone git@github.com:malinpolin/yamdb_final.git
```
##### Windows
```bash
git clone https://github.com/malinpolin/yamdb_final.git
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

### 3. Добавить Action secrets в репозитории на GitHub в разделе settings -> Secrets:

* DOCKER_PASSWORD - пароль от DockerHub;
* DOCKER_USERNAME - имя пользователя на DockerHub;
* HOST - ip-адрес сервера;
* SSH_KEY - приватный ssh ключ (публичный должен быть на сервере);
* TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
* TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)

### Результат

После каждого обновления репозитория (`git push`) будет происходить:
1. Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest из репозитория yamdb_final
2. Сборка и доставка докер-образов на Docker Hub.
3. Автоматический деплой.
4. Отправка уведомления в Telegram.