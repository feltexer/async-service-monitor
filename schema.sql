-- 1. ТРАНЗАКЦИЯ: Создаем структуру (сохранится «вместе или никак»)
BEGIN;

-- Таблица 1: Сервисы (содержит ограничение UNIQUE для URL)
CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(255) UNIQUE NOT NULL
);

-- Таблица 2: Логи проверок (связана через ВНЕШНИЙ КЛЮЧ / FOREIGN KEY)
CREATE TABLE IF NOT EXISTS check_logs (
    id SERIAL PRIMARY KEY,
    service_id INT REFERENCES services(id) ON DELETE CASCADE,
    is_active BOOLEAN NOT NULL,
    response_time_ms NUMERIC(7, 2) NOT NULL,
    checked_at_utc TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMIT;

-- 2. Наполнение данными
INSERT INTO services (name, url) VALUES 
    ('Auth API', 'https://api.example.com/auth'),
    ('Billing Service', 'https://billing.example.com');

INSERT INTO check_logs (service_id, is_active, response_time_ms) VALUES 
    (1, true, 319.21),
    (1, true, 280.50),
    (2, true, 970.21);

-- 3. КРИТЕРИЙ ГОТОВНОСТИ: Связывание таблиц через JOIN и фильтрация WHERE
SELECT 
    s.name AS service_name,
    s.url,
    l.is_active,
    l.response_time_ms,
    l.checked_at_utc
FROM check_logs l
JOIN services s ON l.service_id = s.id
WHERE l.is_active = true;