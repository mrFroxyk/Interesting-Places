<img alt="logo" src="https://sabaton-enjoyer.online/static/core/img/logo.png" width="50">

> Сайт для сетевой игры на веб сокетах



** Проект залит на VPS : [sabaton-enjoyer.online](https://sabaton-enjoyer.online/)

## 🤔 Что за проект?

Простой сайт, на Django, который хранит воспоминания о посещенных вами местах
на карте с привязкой к месту

<img src="https://sabaton-enjoyer.online/static/auth_vk/media/demo.gif">

## 🔧 Запуск проекта

1. Клонирование репозитория

```
git clone https://github.com/mrFroxyk/Interesting-Places.git
```

2. Создание своего ключа приложения для вк авторизации
   по [инструкции вк](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/create-application)
   для создания авторизации через этот самый вк.


3. Добавление ключа приложения в settings.json

```
{
  "service_token": "YOUR_VK_APP_TOKEN"
}
```

4. Поднятие кластера

```
docker-compose up
```
