import asyncio
from typing import Any, Callable, Coroutine

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
        return self.__run(self.name)


def create_health_check(name: str, run: HealthCheckFunc) -> HealthChecker:
    return HealthChecker(name=name, run=run)


def create_health_check_with_timeout(name: str, timeout_seconds: int, run: HealthCheckFunc) -> HealthChecker:
    return HealthChecker(name=name, run=run, timeout_seconds=timeout_seconds)


async def run_checks(
    service_name: str,
    checks: list[HealthChecker],
) -> ServiceHealth:
    tasks: list[Any] = []
    for check in checks:
        if check.timeout_seconds == 0:
            tasks.append(asyncify(check.run)())
        else:
            task: Coroutine = asyncio.wait(
                [asyncio.create_task(asyncify(check.run)())],  # type: ignore
                timeout=check.timeout_seconds,
            )

            tasks.append(task)

    results = await asyncio.gather(*tasks)

    service_health = ServiceHealth(service_name=service_name)

    for i, result in enumerate(results):
        if type(result) is tuple:
            check = checks[i]
            service_health.add_result(HealthCheckResult.unhealthy(check.name, f"did not respond after {check.timeout_seconds} seconds"))
        elif type(result) is HealthCheckResult:
            service_health.add_result(result)
        else:
            check = checks[i]
            service_health.add_result(
                HealthCheckResult.unhealthy(
                    check.name,
                    "did not return a HealthCheckResult",
                )
            )

    return service_health
