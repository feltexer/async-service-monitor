   -------Async Service Monitor — Высокопроизводительная асинхронная система мониторинга доступности сервисов и замера latency на Python (asyncio, asyncpg) с хранением метрик в PostgreSQL.------





                                                  Ключевой функционал
																									

-Асинхронная оркестрация: параллельная проверка множества сервисов 
без блокировки основного потока (asyncio, asyncio.gather).


-Строгая валидация данных: встроенная проверка корректности URL и параметров на уровне доменных моделей (models.py) 
с обработкой кастомных исключений.


-Надёжное хранение метрик: асинхронная запись логов проверок и статусов в PostgreSQL 18 через высокопроизводительный драйвер asyncpg.


-Целостность данных в БД: реляционная схема (schema.sql) с внешними ключами (FOREIGN KEY),
каскадными связями и гарантией уникальности сервисов (ON CONFLICT).


                                               
                                                  Технологический стек

																									
Language: Python 3.12+

Async Engine: asyncio

Database: PostgreSQL 18 + asyncpg

Architecture: Decoupled Architecture (Models / Database persistence / Orchestration)
