from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class HealthCheckStatus(str, Enum):
    ok = "ok"
    unhealthy = "unhealthy"


@dataclass
class HealthCheckResult:
    checkName: str
    status: HealthCheckStatus
    errorDetails: Optional[str] = None

    def to_dict(self) -> dict:
        d = {
            "checkName": self.checkName,
            "status": self.status.value,
        }

        if self.errorDetails:
            d["errorDetails"] = self.errorDetails

        return d

    @staticmethod
    def ok(check_name: str) -> HealthCheckResult:
        return HealthCheckResult(checkName=check_name, status=HealthCheckStatus.ok)

    @staticmethod
    def unhealthy(check_name: str, error_details: str) -> HealthCheckResult:
        return HealthCheckResult(
            checkName=check_name,
            status=HealthCheckStatus.unhealthy,
            errorDetails=error_details,
        )
