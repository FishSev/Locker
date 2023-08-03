# Пояснения

## Backend
- файл [backend.py](backend.py) реализует backend на Flask
- время до сообщения при открытой двери 'PANIC_TIME' составляет 60 сек.
- пароль для доступа хранится захэшированным. Если что он '1234' 🫣
- backend запущен на сервере в Detach-mode на screen. При перезагрузке сервера необходимо запустить заново.

## Frontend

- папка [/frontend](frontend/) реализует frontend на React
    - [App.js](frontend/src/App.js) подключение компонент к роутам
    - [LockerComponent.js](frontend/src/LockerComponent.js) страница камеры хранения
    - [App.css](frontend/src/App.css) стили
- доступ к frontend через сайт [madenews.me](https://madenews.me/)

## Unit-тесты

файл [test_app.py](test_app.py) покрывает backend Unit-тестами


### Доп. для себя 
установка Node.js и npm для работы React

``` bash
sudo apt update
sudo apt update

nodejs -v
sudo apt install npm

npm cache clean -f && sudo npm install -g n && sudo n latest

npm install react-router-dom@5.2.0

```