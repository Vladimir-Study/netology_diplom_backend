## Даннный репозиторий является серверной частью дипломного проекта от Netology по курсу Fullstack Developer for Python.

### Развертывание проекта

Для полноценной работы проекта на вашем устройстве должна быть установлена БД Postgresql.

1. Создайте копию репозитория на вашем устройстве командой `git clone`. 

1. Командой `pip install -r requirements.txt` установите необходимые для работы проекта библиотеки.

1. В БД Postgres необходимо создать БД с именем diplom_project

1. В файле .env установите следующие переменные для подключения к БД.
   - DB_USER - имя пользователя для подключения к БД
   - DB_PASSWORD - пароль для подключения к БД
   - DB_PORT- порт для подключения к БД
   - DB_HOST - хост для подключения к БД
   - SECRET_KEY - секретный ключ Django приложения
   - TIMEZONE - верменная зона
   - CORS_ALLOWED_ORIGINS - разрешенные политикой CORS адреса (необходимо устанавливать в случае если закоментирована строка CORS_ORIGIN_ALLOW_ALL и раскоментирована CORS_ALLOWED_ORIGINS в settings.py)
   - BASE_MEDIA_DIR - папка хранения файлов загружаемых пользователями
   - DEBUG - режим отладки (по умолчанию True)

1. Выполните миграции из директории с файлом manage.py командой `python manage.py migrate` 

1. Запуск проекта производится из директории с файлом manage.py командой `pyhton manage.py runserver`

В проекте реализован по следующим критериям:

1. Реализация на Python с использованием фреймворка Django и СУБД Postgres для хранения информации.

2. Настройки приложения, такие как параметры подключения к БД, размещения файлового хранилища и т. п., выделены в коде в отдельный модуль.

3. Загрузка статических ресурсов (HTML, CSS, JS-файлы фронтенда), а также API-вызовы обрабатываются единым сервером.

4. В проекте созданы все миграции, необходимые для инициализации БД в работоспособное состояние, — создание БД, таблиц, пользователя admin с правами администратора.

5. Все API-вызовы соответствуют семантическим правилам для REST API, для обмена данными между фронтендом и бэкендом используется формат JSON.

6. Сервер содержит реализацию бэкенда для двух основных блоков приложения: административный интерфейс и работа с файловым хранилищем.

7. Административный интерфейс включает следующие функции (конкретные API-вызовы):

- [x] регистрация пользователя — с валидацией входных данных на соответствие требованиям, описанным выше;
- [x] получение списка пользователей;
- [x] удаление пользователя;
- [x] аутентификация пользователя (реализована с помощью JWT токена);
- [x] выход пользователя из системы — logout.

Общие комментарии к этому блоку:

- данные о пользователях храняться в таблице БД в полях, имеющих соответствующие им типы: логин, полное имя, email, пароль, признак администратора, путь к хранилищу пользователя относительно общего пути к хранилищу файлов;
- все вызовы, кроме регистрации пользователя, и скачивания файла по сгенерированной сслыке защищены проверкой аутентификации пользователя в системе;
- функция удаления пользователей доступна только пользователю, имеющему признак администратора;
- ошибки должны возвращаться из API в виде соответствующих статус-кодов, а также в формате JSON.

8. Блок работы с файловым хранилищем содержит следующие функции:

- получение списка файлов пользователя;
- загрузка файла в хранилище;
- удаление файла из хранилища;
- переименование файла;
- изменение комментария к файлу;
- скачивание файла;
- формирование специальной ссылки на файл для использования внешними пользователями;
- скачивание файла через специальную ссылку, используемую внешними пользователями или веб-приложениями.

Общие комментарии к этому блоку:

- все функции работы с хранилищем проверяют права доступа пользователя к хранилищу;
- администратору доступна работа с хранилищем любого пользователя — функция получения списка файлов принимает параметр с указанием хранилища, если пользователь — администратор;
- файлы сохранятюся на диске сервера под уникальными именами в системе папок, не допускающей конфликтов имён в случае, если разные пользователи загружают файлы с одинаковыми именами;
- для каждого файла в БД сохраняться следующая информация: оригинальное имя файла, размер, дата загрузки, последняя дата скачивания, комментарий, путь к файлу в хранилище, специальная ссылка, по которой файл может быть скачан внешним пользователем;
- необходимо, чтобы базовая папка для хранения файлов настраивалась как параметр системы;
- специальная ссылка на файлы формируется в максимально обезличенном виде, т.е. не содержит в себе имени пользователя, информации о его хранилище и оригинальном имени файла (генерируется uuid);
- необходимо, чтобы при скачивании файла по такой ссылке он выгружался сервером с указанием оригинального имени.

Общие требования к серверу:

- состояние аутентификации пользователя должно отслеживаться через сохранение информации о сессии;
- все API-вызовы должны проверяют права доступа пользователя и возвращают соответствующие ошибки через HTTP-статус и сообщение в формате JSON;
- все события сервера логируются в файл, консоль и базу данных путём вывода сообщений «debug», «info», «warning», «error» с указанием даты и времени, информации, достаточной для анализа работоспособности и отладки сервера.