# testing-system
Проект системы тестирования по предмету "Проектирование защищенных информационных систем" НИЯУ МИФИ

## Как запустить локально проект
Для того чтобы запустить проект необходимо иметь на своём
компьютере **docker** и **docker-compose**.  

## Установка **docker** и **docker-compose**
[Docker install](https://docs.docker.com/get-docker/)

## Запуск
Перед запуском необходимо создать `.env` файл в корне проекта   
В этот файл следует добавить следующие переменные окружения
```dotenv
DJANGO_SECRET_KEY='some_secret'
DJANGO_DEBUG=true
POSTGRES_DATABASE='testflow-db'
POSTGRES_USER='testflow-user'
POSTGRES_PASSWORD='s3cret'
```
Следующей командой в корне проекта выполняться все необходимые инструкции и локально запуститься проект.
```shell
docker-compose up -d --build
```