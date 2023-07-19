from dataclasses import dataclass, field

from .health_check_result import (
    HealthCheckResult,
    HealthCheckStatus,
)


@dataclass
class ServiceHealth:
    service_name: str
    checks: dict[str, HealthCheckResult] = field(default_factory=dict)

    @property
    def unhealthy(self) -> bool:
        if not self.checks:
            return False

        return any(result.status == HealthCheckStatus.unhealthy for result in self.checks.values())

    def add_result(self, result: HealthCheckResult) -> None:
        self.checks[result.check_name] = result

        if result.status == HealthCheckStatus.unhealthy and not self.unhealthy:
            self.unhealthy = True

    def to_dict(self) -> dict:
        return {
            "serviceName": self.service_name,
            "unhealthy": self.unhealthy,
            "checks": [check.to_dict() for check in self.checks.values()] if self.checks else [],
        }
