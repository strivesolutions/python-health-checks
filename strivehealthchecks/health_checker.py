import asyncio
from typing import Callable

from asyncer import asyncify

from .health_check_result import HealthCheckResult
from .service_health import ServiceHealth

HealthCheckFunc = Callable[[str], HealthCheckResult]


class HealthChecker:
    def __init__(self, name: str, run: HealthCheckFunc, timeout_seconds: int = 0):
        self.name = name
        self.__run = run
        self.timeout_seconds = timeout_seconds

    def run(self) -> HealthCheckResult:
        try:
            return self.__run(self.name)
        except Exception as e:
            return HealthCheckResult.unhealthy(self.name, str(e))


async def run_check_with_timeout(check: HealthChecker):
    try:
        result = await asyncio.wait_for(asyncify(check.run)(), check.timeout_seconds)
        return result if isinstance(result, HealthCheckResult) else None
    except asyncio.TimeoutError:
        return None


async def run_checks(
    service_name: str,
    checks: list[HealthChecker],
) -> ServiceHealth:
    tasks = []
    for check in checks:
        if check.timeout_seconds == 0:
            tasks.append(asyncify(check.run)())
        else:
            tasks.append(run_check_with_timeout(check))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    service_health = ServiceHealth(service_name=service_name)

    for check, result in zip(checks, results):
        if result is None or isinstance(result, Exception):
            service_health.add_result(
                HealthCheckResult.unhealthy(check.name, f"did not respond after {check.timeout_seconds} seconds" if result is None else "exception occurred")
            )
        else:
            service_health.add_result(result)

    return service_health
