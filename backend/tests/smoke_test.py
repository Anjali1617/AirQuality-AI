"""
End-to-end smoke test verifying live API endpoints and frontend responsiveness.
"""

import urllib.request
import urllib.error
import json
import sys


def test_endpoint(url, method="GET", data=None):
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data else None,
        headers=headers,
        method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.status
            body = response.read().decode("utf-8")
            return status, json.loads(body) if "json" in response.headers.get("Content-Type", "") else body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return e.code, body
    except Exception as e:
        return 0, str(e)


def run_smoke_tests():
    print("=== LIVE SERVICE SMOKE TEST SUITE ===")
    
    # 1. Health check
    status, body = test_endpoint("http://127.0.0.1:8000/health")
    print(f"[1] GET /health -> Status {status}")
    assert status == 200 and body.get("status") == "healthy", f"Health check failed: {body}"
    print(f"    Project: {body.get('project')}, Model loaded: {body.get('model_loaded')}")

    # 2. Dashboard summary
    status, body = test_endpoint("http://127.0.0.1:8000/api/dashboard/summary")
    print(f"[2] GET /api/dashboard/summary -> Status {status}")
    assert status == 200 and "stat_cards" in body, "Dashboard summary failed"
    print(f"    Cards returned: {len(body['stat_cards'])}, 72h trend points: {len(body['trend_data'])}")

    # 3. Create prediction
    sample_payload = {
        "PT08.S1(CO)": 1150.0,
        "PT08.S2(NMHC)": 980.0,
        "PT08.S3(NOx)": 920.0,
        "PT08.S4(NO2)": 1500.0,
        "PT08.S5(O3)": 1100.0,
        "T": 16.5,
        "RH": 52.0,
        "AH": 0.85,
        "Hour": 15,
        "DayOfWeek": 3
    }
    status, body = test_endpoint("http://127.0.0.1:8000/api/predictions", method="POST", data=sample_payload)
    print(f"[3] POST /api/predictions -> Status {status}")
    assert status == 201 and "predicted_concentration" in body, f"Prediction failed: {body}"
    print(f"    Predicted {body['target']}: {body['predicted_concentration']} {body['unit']} ({body['risk_category']})")

    # 4. History check
    status, body = test_endpoint("http://127.0.0.1:8000/api/history?limit=5")
    print(f"[4] GET /api/history -> Status {status}")
    assert status == 200 and isinstance(body, list) and len(body) > 0, "History retrieval failed"
    print(f"    Recent history count: {len(body)}, Latest ID: #{body[0]['id']}")

    # 5. Historical data paginated
    status, body = test_endpoint("http://127.0.0.1:8000/api/historical-data?page=1&page_size=5")
    print(f"[5] GET /api/historical-data -> Status {status}")
    assert status == 200 and body.get("total_records") == 9357, "Historical data count mismatch"
    print(f"    Total records: {body['total_records']}, Records in page: {len(body['records'])}")

    # 6. Model info
    status, body = test_endpoint("http://127.0.0.1:8000/api/model-info")
    print(f"[6] GET /api/model-info -> Status {status}")
    assert status == 200 and "model_name" in body, "Model info failed"
    print(f"    Model: {body['model_name']}, Test R²: {body['evaluation']['test_r2']}, Test MAE: {body['evaluation']['test_mae']}")

    # 7. Frontend check
    status, body = test_endpoint("http://127.0.0.1:5173/")
    print(f"[7] GET http://127.0.0.1:5173/ -> Status {status}")
    assert status == 200, f"Frontend did not return 200: {status}"
    print("    Frontend index.html successfully served")

    print("\nALL 7 SMOKE TESTS PASSED!")


if __name__ == "__main__":
    run_smoke_tests()
