![yamdb_workflow](https://github.com/denisvolkov67/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

# Яндекс.Практикум. Python backend. Диплом

## Содержание
- [Описание_проекта](#Описание_проекта)
- [Технологии](#Технологии)
- [Запуск проекта](#Запуск_проекта)
- [Тесты](#Тесты)
- [Авторы](#Авторы)

### <a name="Описание_проекта">Описание</a>

Foodgram реализован для публикации рецептов. Авторизованные пользователи могут 
подписываться на понравившихся авторов, добавлять рецепты в избранное, 
в покупки, скачать список покупок ингредиентов для добавленных в покупки 
рецептов.

Проект запущен и доступен по [http://51.250.9.203/recipes](http://51.250.9.203/recipes)
Админка: admin, 1234

### <a name="Технологии">Технологии</a>

В проекте применяется 
- **Django REST Framework**, 
- **Python 3**,
- **PostgreSQL**,
- **Docker**, 
- **Nginx**,
- **Gunicorn**,
- **Git**, 
- Аутентификация реализована с помощью **токена**.

### <a name="Запуск проекта">Запуск проекта</a>

- Установите Docker на ваш сервер:
```python
 sudo apt install docker.io
```

- Установите Docker-compose на сервер:
```python
 sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
 sudo chmod +x /usr/local/bin/docker-compose
```

- Скопируйте на сервер файлы Docker-compose.yml и nginx.conf из папки infra/. Не забудьте указать свой ip в конфиге.
```python
scp docker-compose.yml admin@51.250.9.203:/home/admin/docker-compose.yml
scp nginx.conf admin@51.250.9.203:/home/admin/nginx.conf
```

- После успешного деплоя зайдите на боевой сервер и выполните команды (только после первого деплоя):
    Собрать статические файлы в STATIC_ROOT:
```python
  docker-compose exec web python3 manage.py collectstatic --noinput
```

- После запуска контейнеров выполните команды в терминале:
```python
 docker-compose exec web python manage.py makemigrations
 docker-compose exec web python manage.py migrate --noinput
```

- Создаём суперпользователя
```python
 docker-compose exec web python manage.py createsuperuser
```

- Загружаем ингредиенты в базу данных (необязательно):
```python
 docker-compose exec web python manage.py load_data
```

- Запуск контейнеров выполняется командой:
```python
 docker-compose up
```

- Остановка контейнеров выполняется командой:
```python
 docker-compose stop
```

### <a name="Тесты">Тесты</a>
```python
  flake8
```

### <a name="Авторы">Авторы</a>
```
 Денис Волков
```