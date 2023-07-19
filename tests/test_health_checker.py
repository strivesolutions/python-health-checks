from time import sleep
from timeit import default_timer

import pytest

from strivehealthchecks import HealthCheckResult, ServiceHealth, create_health_check, create_health_check_with_timeout, run_checks


@pytest.mark.asyncio
async def test_run_checks():
    def passing_check(name: str) -> HealthCheckResult:
        return HealthCheckResult.ok(name)

    check = create_health_check("test", passing_check)
    service_health = ServiceHealth(serviceName="test")
    await run_checks(service_health, [check])
    assert not service_health.unhealthy


@pytest.mark.asyncio
async def test_check_timeout():
    def slow_check(name: str) -> HealthCheckResult:
        sleep(3)
        return HealthCheckResult.ok(name)

    check = create_health_check_with_timeout("slow", 1, slow_check)

    service_health = ServiceHealth(serviceName="test")
    start = default_timer()
    await run_checks(service_health, [check])
    end = default_timer()

    assert service_health.unhealthy

    expected = 1
    actual = end - start

    assert actual == pytest.approx(expected, 0.1), f"Test took {end - start}s to complete (expected ~{expected}s)"
