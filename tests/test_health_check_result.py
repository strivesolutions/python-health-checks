from strivehealthchecks.health_check_result import HealthCheckResult, HealthCheckStatus


def test_to_dict():
    result = HealthCheckResult(
        checkName="test_check",
        status=HealthCheckStatus.ok,
        errorDetails="error_details",
    )

    assert result.to_dict() == {
        "checkName": "test_check",
        "status": "ok",
        "errorDetails": "error_details",
    }
