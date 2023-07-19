# Strive Health Checks

A simple framework for running health checks.  This library provides classes which serialize to Strive's preferred data contract, as well as a means of running checks asynchronously.

## Output format

```
{
    "serviceName": "Your service",
    "checks": [
        {
            "checkName": "check one",
            "status": "ok"
        },
        {
            "checkName": "check two",
            "status": "unhealthy",
            "errorDetails": "Failed to connect."
        }
    ]
}
```

## Creating health checks

A health check is configured by creating an instance of the HealthChecker class and providing a name for the check (string), a run function (see below), and if desired, a timeout in seconds (integer).

To invoke health checks, pass the name of the service and a list of health checkers to the run_checks function and await the result.  The result will be a ServiceHealth instance, which contains the results from all checks along with a healthy flag (bool).  If any check is unhealthy, the entire response will be considered unhealthy.

If a timeout is provided, the check will be considered unhealthy if it does not complete in less than the provided timeout value.

### Run function
The run function is a function which takes the name of the check as string for the only argument, and returns a HealthCheckResult instance.

You can do anything you like inside the function prior to returning the result, eg: checking database connectivity, checking disk space, etc.

You do not need to worry about timeouts or exceptions; both can be handled by the run_checks function.


## Example usage in a FastAPI service

```
from time import sleep

from fastapi import FastAPI, Response
from fastapi.params import Depends
from strivehealthchecks import HealthChecker, HealthCheckResult, create_health_check, create_health_check_with_timeout, run_checks

app = FastAPI()


def create_health_checks() -> list[HealthChecker]:
    return [
        check_one(),
        check_two(),
    ]


def check_one() -> HealthChecker:
    def run(name: str) -> HealthCheckResult:
        return HealthCheckResult.ok(name)

    return HealthChecker(name="one", run=run)


# this check will fail because it takes 3 seconds to return a successful result, but the timeout is 1 second
def check_two() -> HealthChecker:
    def slow_check(name: str) -> HealthCheckResult:
        sleep(3)
        return HealthCheckResult.ok(name)

    return HealthChecker(name="two", timeout_seconds=1, run=slow_check)


@app.get("/healthz")
async def health_handler(response: Response, checks: list[HealthChecker] = Depends(create_health_checks)):
    result = await run_checks("sample", checks)

    response.status_code = 200 if result.healthy else 500
    return result.to_dict()
```

**Expected result from above example:**

```
{
    "serviceName": "sample",
    "checks": [        
        {
            "checkName": "one",
            "status": "ok"
        },
        {
            "checkName": "two",
            "status": "unhealthy",
            "errorDetails": "did not respond after 1 seconds"
        }
    ]
}
```
