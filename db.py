import asyncpg

# Параметры подключения к PostgreSQL
DB_CONFIG = {
    "user": "postgres",
    "password": "postgres", 
    "database": "postgres",
    "host": "127.0.0.1",
    "port": 5432,
}


async def save_check_result(
    service_name: str, 
    url: str, 
    is_active: bool, 
    response_time_ms: float
) -> None:
    # Открываем соединение
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        # 1. Записываем сервис (или берём существующий id, если URL уже занесён)
        service_id = await conn.fetchval(
            """
            INSERT INTO services (name, url) 
            VALUES ($1, $2)
            ON CONFLICT (url) DO UPDATE SET name = EXCLUDED.name
            RETURNING id;
            """,
            service_name, url
        )
        
        # 2. Записываем логи проверок, привязываясь к service_id
        await conn.execute(
            """
            INSERT INTO check_logs (service_id, is_active, response_time_ms)
            VALUES ($1, $2, $3);
            """,
            service_id, is_active, response_time_ms
        )
    finally:
        # Всегда закрываем подключение к базе
        await conn.close()