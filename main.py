import asyncio
import time
from models import ServiceTask, ServiceValidationError
from db import save_check_result  # <-- Новый импорт


async def check_service(task: ServiceTask) -> dict:
    start_time = time.perf_counter()
    await asyncio.sleep(0.3)  # Имитация сетевого запроса
    response_time_ms = (time.perf_counter() - start_time) * 1000
    
    is_active = True
    report = task.get_report(is_active=is_active, response_time_ms=response_time_ms)
    
    # Сохраняем в PostgreSQL!
    await save_check_result(
        service_name=report["service_name"],
        url=report["url"],
        is_active=report["is_active"],
        response_time_ms=report["response_time_ms"]
    )
    
    return report


async def main():
    raw_services = [
        {"name": "Auth API", "url": "https://api.example.com/auth", "timeout": 1.5},
        {"name": "Billing Service", "url": "https://billing.example.com", "timeout": 2.0},
        {"name": "Notifications", "url": "https://notify.example.com", "timeout": 1.0},
        {"name": "Broken Service", "url": "ftp://bad-url.com", "timeout": 1.0},
    ]

    valid_tasks: list[ServiceTask] = []

    for item in raw_services:
        try:
            task = ServiceTask(
                name=str(item["name"]),
                url=str(item["url"]),
                timeout=float(item["timeout"])
            )
            valid_tasks.append(task)
        except ServiceValidationError as err:
            print(f"[ОШИБКА ВАЛИДАЦИИ] {err}")

    print("\n--- Запуск асинхронной проверки и сохранения в БД ---")
    results = await asyncio.gather(*[check_service(task) for task in valid_tasks])

    print("\n[УСПЕХ] Все результаты успешно сохранены в PostgreSQL:")
    for report in results:
        print(f" - {report['service_name']}: {report['response_time_ms']} мс")


if __name__ == "__main__":
    asyncio.run(main())