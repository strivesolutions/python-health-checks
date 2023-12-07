from strivehealthchecks import HealthCheckResult, HealthCheckStatus


def test_to_dict():
    result = HealthCheckResult(
        check_name="test_check",
        status=HealthCheckStatus.ok,
        error_details="error_details",
    )

    assert result.to_dict() == {
        "checkName": "test_check",
        "status": "ok",
        "errorDetails": "error_details",
    }
