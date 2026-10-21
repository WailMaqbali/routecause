from app import app

def test_diagnose_returns_trace():
    client = app.test_client()
    resp = client.post("/diagnose", data={"scope": "one", "symptom": "no_internet", "change": "new_device"})
    assert resp.status_code == 200
    assert b"DHCP/IP conflict" in resp.data      # top diagnosis shown
    assert b"R30" in resp.data                   # trace shows the rule that fired