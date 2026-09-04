from datetime import datetime, timezone


class ServiceValidationError(Exception):
    """Кастомное исключение для ошибок валидации."""
    pass


class ServiceTask:
    """Класс, который хранит данные о сайте/сервисе и проверяет их корректность."""

    def __init__(self, name: str, url: str, timeout: float = 2.0) -> None:
        self.name: str = name
        self.url: str = url
        self.timeout: float = timeout
        self.created_at_utc: datetime = datetime.now(timezone.utc)
        self.validate()

    def validate(self) -> None:
        """Метод проверки входных данных."""
        try:
            if not self.name or not isinstance(self.name, str):
                raise ValueError("Имя сервиса должно быть непустой строкой.")

            if not self.url.startswith(("http://", "https://")):
                raise ValueError(f"Некорректный URL '{self.url}'. Забыли http:// или https://")

            if self.timeout <= 0:
                raise ValueError("Таймаут должен быть больше 0 секунд.")

        except ValueError as err:
            raise ServiceValidationError(f"Ошибка в сервисе '{self.name}': {err}")

    def get_report(self, is_active: bool, response_time_ms: float) -> dict[str, str | float | bool]:
        """Формирует готовый отчет с меткой времени UTC."""
        return {
            "service_name": self.name,
            "url": self.url,
            "is_active": is_active,
            "response_time_ms": round(response_time_ms, 2),
            "created_at_utc": self.created_at_utc.isoformat(),
        }