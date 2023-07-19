from strivehealthchecks import HealthCheckResult, ServiceHealth


def test_healthy_to_dict():
    result = ServiceHealth(
        serviceName="test_service",
        checks={"test_check": HealthCheckResult.ok(check_name="test_check")},
    )

    assert result.to_dict() == {
        "serviceName": "test_service",
        "unhealthy": False,
        "checks": [
            {
                "checkName": "test_check",
                "status": "ok",
            }
        ],
    }


def test_unhealthy_to_dict():
    result = ServiceHealth(
        service_name="test_service",
        checks={"test_check": HealthCheckResult.unhealthy(check_name="test_check", error_details="error_details")},
    )

    d = result.serialize()
    assert d == {
        "serviceName": "test_service",
        "unhealthy": True,
        "checks": [
            {
                "checkName": "test_check",
                "status": "unhealthy",
                "errorDetails": "error_details",
            }
        ],
    }


def test_can_create_service_health_without_checks():
    ServiceHealth(serviceName="test")
    assert True


def test_can_add_result_to_service_health():
    service_health = ServiceHealth(serviceName="test")
    service_health.add_result(HealthCheckResult.ok(check_name="test_check"))
    assert True
