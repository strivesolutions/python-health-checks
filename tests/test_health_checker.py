from time import sleep
from timeit import default_timer

import pytest

from strivehealthchecks import HealthCheckResult, create_health_check, create_health_check_with_timeout, run_checks


@pytest.mark.asyncio
async def test_run_checks():
    def passing_check(name: str) -> HealthCheckResult:
        return HealthCheckResult.ok(name)

    check = create_health_check("test", passing_check)
    _, healthy = await run_checks("test_service", [check])
    assert healthy


@pytest.mark.asyncio
async def test_check_timeout():
    def slow_check(name: str) -> HealthCheckResult:
        sleep(3)
        return HealthCheckResult.ok(name)

    check = create_health_check_with_timeout("slow", 1, slow_check)

    start = default_timer()
    _, healthy = await run_checks("test_service", [check])
    end = default_timer()

    assert not healthy

    expected = 1
    actual = end - start

    assert actual == pytest.approx(expected, 0.1), f"Test took {end - start}s to complete (expected ~{expected}s)"
