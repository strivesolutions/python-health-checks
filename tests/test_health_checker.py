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


@pytest.mark.asyncio
async def test_check_timeout_success():
    def slow_check(name: str) -> HealthCheckResult:
        sleep(3)
        return HealthCheckResult.ok(name)

    check = HealthChecker("slow", slow_check, timeout_seconds=5)

    start = default_timer()
    result = await run_checks("test_service", [check])
    end = default_timer()

    assert result.healthy

    expected = 3
    actual = end - start

    assert actual == pytest.approx(expected, 0.1), f"Test took {end - start}s to complete (expected ~{expected}s)"


@pytest.mark.asyncio
async def test_check_async_timeouts_dont_stack():
    def slow_check_1(name: str) -> HealthCheckResult:
        sleep(3)
        return HealthCheckResult.ok(name)

    def slow_check_2(name: str) -> HealthCheckResult:
        sleep(5)
        return HealthCheckResult.ok(name)

    check_1 = HealthChecker("slow", slow_check_1, timeout_seconds=1)
    check_2 = HealthChecker("slow", slow_check_2, timeout_seconds=3)

    start = default_timer()
    result = await run_checks("test_service", [check_1, check_2])
    end = default_timer()

    assert not result.healthy

    # This test should fail in about 3 seconds (longest timeout) - if the run checks runs synchronously, it will take longer
    expected = 3
    actual = end - start

    assert actual == pytest.approx(expected, 0.1), f"Test took {end - start}s to complete (expected ~{expected}s)"
