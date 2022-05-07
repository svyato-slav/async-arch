###  ДЗ №1 

[Модель данных](https://cloud.mail.ru/public/DV5n/VGk43ZTut)

[Модель доменов](https://cloud.mail.ru/public/7MpB/Bfq2NrKYa)

[Составляющие бизнес-требований, сервисы, события](https://docs.google.com/document/d/1QNE8lLybthXvNGZnA8_lF-MmCNK8fiTr1WTt9ie8oNU/edit?usp=sharing)

### ДЗ №2

Chose oAuth, RabbitMQ 

Run auth service:
python auth/manage.py runserver localhost:8000

Run task tracker service:
python task_tracker/manage.py runserver localhost:8010

Run task tracker consumer:
python task_tracker/consumer.py
