
def run_test(device, test_plan):
    results = []

    for step in test_plan["steps"]:
        response = device.handle_command({
            "name": "GET_TELEMETRY"
        })

        measurement = step["measurement"]
        actual = response.get(measurement)

        if actual is None:
            verdict = "ERROR"
        elif not step["min"] <= actual <= step["max"]:
            verdict = "FAIL"
        elif response.get("status") != "READY":
            verdict = "FAIL"
        else:
            verdict = "PASS"

        results.append({
            "step": step["name"],
            "measurement": measurement,
            "actual": actual,
            "minimum": step["min"],
            "maximum": step["max"],
            "verdict": verdict
        })

    overall = (
        "PASS"
        if all(result["verdict"] == "PASS" for result in results)
        else "FAIL"
    )

    return {
        "test_name": test_plan["test_name"],
        "verdict": overall,
        "steps": results
    }
