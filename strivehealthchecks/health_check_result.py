from __future__ import annotations

from enum import Enum
from typing import Optional


class HealthCheckStatus(str, Enum):
    ok = "ok"
    unhealthy = "unhealthy"


class HealthCheckResult:
    def __init__(self, check_name: str, status: HealthCheckStatus, error_details: Optional[str] = None):
        self.check_name = check_name
        self.status = status
        self.error_details = error_details

    def to_dict(self) -> dict:
        d = {
            "checkName": self.check_name,
            "status": self.status.value,
        }

        if self.error_details:
            d["errorDetails"] = self.error_details

        return d

    @staticmethod
    def ok(check_name: str) -> HealthCheckResult:
        return HealthCheckResult(check_name=check_name, status=HealthCheckStatus.ok)

    @staticmethod
    def unhealthy(check_name: str, error_details: str) -> HealthCheckResult:
        return HealthCheckResult(
            check_name=check_name,
            status=HealthCheckStatus.unhealthy,
            error_details=error_details,
        )
