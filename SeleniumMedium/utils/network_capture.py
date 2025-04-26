import json
import os

def capture_api_calls(driver, filename="api_logs/api_calls.json"):
    logs = driver.get_log("performance")
    api_calls = []

    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
            log["method"] == "Network.requestWillBeSent"
            and "request" in log["params"]
            and log["params"]["request"]["url"].startswith("https://")
        ):
            api_url = log["params"]["request"]["url"]
            method = log["params"]["request"].get("method", "GET")
            api_calls.append({"method": method, "url": api_url})

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w") as f:
        json.dump(api_calls, f, indent=2)

    print(f"📋 API Calls captured and saved to {filename}")
