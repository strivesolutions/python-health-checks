from time import sleep
from timeit import default_timer

import pytest

from strivehealthchecks import HealthCheckResult, run_checks
from strivehealthchecks.health_checker import HealthChecker


@pytest.mark.asyncio
async def test_run_checks():
    def passing_check(name: str) -> HealthCheckResult:
        return HealthCheckResult.ok(name)

    check = HealthChecker("test", passing_check)
    result = await run_checks("test_service", [check])
    assert result.healthy


@pytest.mark.asyncio
async def test_check_timeout():
    def slow_check(name: str) -> HealthCheckResult:
        sleep(3)
        return HealthCheckResult.ok(name)

    check = HealthChecker("slow", slow_check, timeout_seconds=1)

    start = default_timer()
    result = await run_checks("test_service", [check])
    end = default_timer()

    assert not result.healthy

    expected = 1
    actual = end - start

    assert actual == pytest.approx(expected, 0.1), f"Test took {end - start}s to complete (expected ~{expected}s)"


@pytest.mark.asyncio
async def test_check_throws_exception() -> HealthChecker:
    def failing_check(name: str) -> HealthCheckResult:
        raise Exception("test")

    check = HealthChecker("test", failing_check)
    result = await run_checks("test_service", [check])
    assert not result.healthy
    assert len(result.checks) == 1
