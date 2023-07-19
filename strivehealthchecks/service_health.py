from typing import Optional

from .health_check_result import (
    HealthCheckResult,
    HealthCheckStatus,
)


class ServiceHealth:
    def __init__(self, service_name: str, checks: Optional[dict[str, HealthCheckResult]] = None):
        self.service_name = service_name
        self.checks = checks or {}
        self.healthy = True

    def add_result(self, result: HealthCheckResult) -> None:
        self.checks[result.check_name] = result

        if result.status == HealthCheckStatus.unhealthy and self.healthy:
            self.healthy = False

    def to_dict(self) -> dict:
        return {
            "serviceName": self.service_name,
            "checks": [check.to_dict() for check in self.checks.values()] if self.checks else [],
        }
