from dataclasses import dataclass, field

from .health_check_result import (
    HealthCheckResult,
    HealthCheckStatus,
)


@dataclass
class ServiceHealth:
    service_name: str
    checks: dict[str, HealthCheckResult] = field(default_factory=dict)
    healthy: bool = True

    def add_result(self, result: HealthCheckResult) -> None:
        self.checks[result.check_name] = result

        if result.status == HealthCheckStatus.unhealthy and self.healthy:
            self.healthy = False

    def to_dict(self) -> dict:
        return {
            "serviceName": self.service_name,
            "checks": [check.to_dict() for check in self.checks.values()] if self.checks else [],
        }
