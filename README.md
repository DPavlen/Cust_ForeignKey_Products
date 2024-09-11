![image](https://github.com/user-attachments/assets/f4a08bc2-d27a-4b30-a3c5-738cccf7d623)# Cust_ForeignKey_Products

## 1. [Задание и требования](#1)
## 2. [Функционал API, эндпойнты и технические особенности](#2)
## 3. [Стек технологий](#3)
## 4. [Запуск проекта через docker compose и ссыылка на него](#4)
## 5. [Автор проекта:](#5)

## 1. Описание  <a id=1></a>
Продукт имеет уникальные продукты. Уникальные продукты создаются на основе атрибутов продукта.
Задача: 
Написать кастомный ForeignKey, который обеспечивает интерфейс взаимодействия Product instance с UniqueProduct instances (по сути создаёт дополнительную абстракцию для reverse_many_to_one_manager).
Интерфейс должен иметь 2 метода: all, generate.
Метод all проксирует метод all ReverseManyToOne менеджера.
Метод generate создаёт UniqueProduct для данного Product instance (правила генерации не имеют значения).
Подсказка: Обратите внимание на атрибут related_accessor_class класса ForeignKey или его bases.

## 2. Функционал API, эндпойнты и технические особенности <a id=2></a>

Создан UserManager и кастомный пользователь CustUser с регистрацией по email. ()
Написана COLLECT_SCHEMA для документирования эндпойнтов.
- http://localhost:8000/api/swagger/ реализована возможность автоматической генерации документации для вашего API, с помощью Swagger
- https://localhost:8000/api/redoc/ реализована возможность автоматической генерации документации для вашего API, с помощью Redoc
- http://localhost:8000/api/users/  Djoser эндпойнты. Работа с пользователями. Регистрация пользователей, удаление, 
изменение данных.Вывод пользователей. POST, GET, PUT, PATCH, DEL запросы.(Смотри документацию Swagger или Redoc)
- http://localhost:8000/api/auth/token/login/ Djoser эндпойнт.POST-запрос. Вход по email и паролю и получение токена.
- http://localhost:8000/api/auth/token/login/ Djoser эндпойнт.POST-запрос. Выход и удаление токена.

- http://localhost:8000/api/products/ GET.Получить список всех продуктов
- http://localhost:8000/api/products/{id} GET. Получить информацию о продукте по ID. 
- http://localhost:8000/api/unique-products/ GET. Получить информацию об уникальном продукте.
- http://localhost:8000/api/unique-products/{id} GET. Получить информацию об уникальном продукте по ID.
- В моделях написан CustForeignKey(ForeignKey) - Кастомный внешний ключ для установки связи "ManyToOne" между моделями.
    Обеспечивает использование кастомного менеджера для обратных связей.  
- Также UniqueProductManager(models.Manager) - Кастомный менеджер для модели UniqueProduct
- У модели UniqueProduct прицеплен кастомный objects = UniqueProductManager()
- Также написаны тесты для моделей: test_models.py, которые проверяют работу CustForeignKey и всех его связей.

## 3. Стек технологий <a id=3></a>
[![Django](https://img.shields.io/badge/Django-^4.1.10-6495ED)](https://www.djangoproject.com) 
[![Djangorestframework](https://img.shields.io/badge/djangorestframework-3.14.0-6495ED)](https://www.django-rest-framework.org/) 
[![Django Authentication with Djoser](https://img.shields.io/badge/Django_Authentication_with_Djoser-2.2.0-6495ED)](https://djoser.readthedocs.io/en/latest/getting_started.html) 
[![Nginx](https://img.shields.io/badge/Nginx-1.21.3-green)](https://nginx.org/ru/)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)
[![Swagger](https://img.shields.io/badge/Swagger-%201.21.7-blue?style=flat-square&logo=swagger)](https://swagger.io/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-%2020.0.4-blue?style=flat-square&logo=gunicorn)](https://gunicorn.org/) 
[![Docker](https://img.shields.io/badge/Docker-%2024.0.5-blue?style=flat-square&logo=docker)](https://www.docker.com/)
[![DockerCompose](https://img.shields.io/badge/Docker_Compose-%202.21.0-blue?style=flat-square&logo=docsdotrs)](https://docs.docker.com/compose/)

Backend API
![image](https://github.com/user-attachments/assets/f36ed2e9-04de-4781-aad5-b97fe6570427)
![image](https://github.com/user-attachments/assets/23f82ad2-786a-49d8-8226-43ad936aec82)
![image](https://github.com/user-attachments/assets/f227969c-aa85-4e36-9477-97e3a45ab711)
![image](https://github.com/user-attachments/assets/92308dca-ed86-40bc-ae80-024a7565ad96)


## 4. Запуск проекта через docker compose и ссыылка на него <a id=4></a>
## Запуск проекта локально в Docker-контейнерах с помощью Docker Compose

Склонируйте проект из репозитория:

```shell
git clone git@github.com:DPavlen/Cust_ForeignKey_Products.git
```

Перейдите в директорию проекта:

```shell
cd Cust_ForeignKey_Products/
```
Ознакомьтесь с .env.example и после этого перейдите в  
корень директории **Cust_ForeignKey_Products/** и создайте файл **.env**:

```shell
nano .env
```

Добавьте строки, содержащиеся в файле **.env.example** и подставьте 
свои значения.

Пример из .env файла:

```dotenv
SECRET_KEY=DJANGO_SECRET_KEY        # Ваш секретный ключ Django
DEBUG=False                         # True - включить Дебаг. Или оставьте пустым для False
IS_LOGGING=False                    # True - включить Логирование. Или оставьте пустым для False
ALLOWED_HOSTS=127.0.0.1 backend     # Список адресов, разделенных пробелами

# Помните, если вы выставляете DEBUG=False, то необходимо будет настроить список ALLOWED_HOSTS.
# 127.0.0.1 и backend является стандартным значением. Через пробел.
# Присутствие backend в ALLOWED_HOSTS обязательно.

В зависимости какую БД нужно запустит:
#DB_ENGINE=sqlite3
DB_ENGINE=postgresql

POSTGRES_USER=django_user                  # Ваше имя пользователя для бд
POSTGRES_PASSWORD=django                   # Ваш пароль для бд
POSTGRES_DB=django                         # Название вашей бд
DB_HOST=db                                 # Стандартное значение - db
DB_PORT=5432                               # Стандартное значение - 5432

```

```shell
В директории **docker** проекта находится файл **docker-compose.yml**, с 
помощью которого вы можете запустить проект локально в Docker контейнерах.
```

Находясь в директории **Cust_ForeignKey_Products/** выполните следующую команду:

> **Примечание.** Если нужно - добавьте в конец команды флаг **-d** для запуска
> в фоновом режиме. Она сбилдит Docker образы и запустит backend django, СУБД PostgreSQL, и Nginx в отдельных Docker контейнерах.
> отработает pytest-1
```shell
sudo docker compose -f docker-compose.yml up --build
```

>**Примечание.** Запускаем собраный уже ранее командой:
```shell      
sudo docker compose -f docker-compose.yml up -d**
```

>**Примечание.** Для того чтобы необходимо остановить и удалить контейнер нужно использовать:   
```shell
sudo docker compose -f docker-compose.yml down 
```

По завершении всех операции проект будет запущен и доступен по адресу
http://127.0.0.1/ или http://localhost:8000/ в зависимости от настроек

Либо просто завершите работу Docker Compose в терминале, в котором вы его
запускали, сочетанием клавиш **CTRL+C**.

***

## 5. Автор проекта: <a id=5></a> 

**Павленко Дмитрий**  
- Ссылка на мой профиль в GitHub [Dmitry Pavlenko](https://github.com/DPavlen)  
