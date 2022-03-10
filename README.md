# Client-Server
For English please scroll down



Данный проект – мессенджер. Состоит и серверного клиентских приложений.
![API](https://github.com/AleksandrVladimirovichNaumov/Client-Server/raw/main/MyMessenger/screenshots/client-server.png)

Перед запуском приложений установите необходимые пакеты из requirements.txt

Для запуска сервера запустите server.py.
Для запуска клиента запустите client.py.
Для запуска сервера и двух клиентов на одной машине запустите launcher.py (работает только на linux).

Структура проека:

client.py - главный модуль клиента

client_gui.py - модуль графической оболочки клиента

client_storage.py - модуль локальной бд клиента

server.py - главный модуль сервера

server.py - модуль графической оболочки сервера

storage.py - модуль бд сервера



decorators.py - общий модуль декораторов для клиента и сервера

descriptor.py - общий модуль дескрипторов для клиента и сервера

arg_parser.py - общий модуль обработки аргументов командной строки для клиента и сервера

metaclasses.py - общий модуль метаклассов для клиента и сервера

my_socket.py - общий модуль сокета для клиента и сервера


*******************************************************************************************************************************************



This project is a messanger. It consists from server and client app.
![API](https://github.com/AleksandrVladimirovichNaumov/Client-Server/raw/main/MyMessenger/screenshots/client-server.png)

Install required packages from requirements.txt before applications run.

To start a server run server.py.
To start a client run client.py.
To start a server and two clients run launcher.py (works only on linux).

Project structure:

client.py - main client module

client_gui.py - client gui module

client_storage.py - client local database module

server.py - main server module

server.py - server gui module

storage.py - server database module

decorators.py - decorators module for client and server

descriptor.py - descriptors module for client and server

arg_parser.py - command line arguments module for client and server

metaclasses.py - metaclass module for client and server

my_socket.py - socket module for client and server