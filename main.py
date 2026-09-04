import asyncio
import random
from models import ServiceTask, ServiceValidationError


async def check_service(task: ServiceTask) -> dict[str, str | float | bool]:
    """Имитирует асинхронный сетевой запрос к сервису."""
    print(f"[START] Проверка: {task.name} ({task.url})...")

    delay = random.uniform(0.2, 1.2)
    await asyncio.sleep(delay)

    is_active = random.choice([True, True, True, False])
    response_time_ms = delay * 1000

    print(f"[DONE] Сервис '{task.name}' ответил за {response_time_ms:.0f} ms")
    return task.get_report(is_active=is_active, response_time_ms=response_time_ms)


async def main() -> None:
    raw_services = [
        {"name": "Auth API", "url": "https://api.example.com/auth", "timeout": 1.5},
        {"name": "Billing Service", "url": "https://billing.example.com", "timeout": 2.0},
        {"name": "Broken Service", "url": "ftp://bad-url.com", "timeout": 1.0},
        {"name": "Database Proxy", "url": "http://db.internal", "timeout": 0.5},
    ]

    valid_tasks: list[ServiceTask] = []

    print("--- 1. ПРОВЕРКА И ВАЛИДАЦИЯ ДАННЫХ ---")
    for item in raw_services:
        try:
            task = ServiceTask(
                name=str(item["name"]),
                url=str(item["url"]),
                timeout=float(item["timeout"])
            )
            valid_tasks.append(task)
            print(f"[OK] Валидация успешна: {task.name}")
        except ServiceValidationError as err:
            print(f"[ОШИБКА ВАЛИДАЦИИ] {err}")

    print("\n--- 2. ПАРАЛЛЕЛЬНЫЙ АСИНХРОННЫЙ ЗАПУСК ---")
    results = await asyncio.gather(*[check_service(task) for task in valid_tasks])

    print("\n--- 3. ИТОГОВЫЕ РЕЗУЛЬТАТЫ В UTC ---")
    for report in results:
        print(report)


if __name__ == "__main__":
    asyncio.run(main())