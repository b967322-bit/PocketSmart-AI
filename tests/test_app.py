def test_health(client):
    r=client.get("/health")
    assert r.status_code==200
    assert r.json()["status"]=="ok"

def test_register_login_and_home(client):
    r=client.post("/register",json={"email":"test@example.com","full_name":"Test User","password":"password123"})
    assert r.status_code==200
    r=client.post("/login",json={"email":"test@example.com","password":"password123"})
    assert r.status_code==200
    r=client.post("/generate-home",json={"budget":50000,"city":"Chennai","rooms":["Living Room"],"style":"Modern","items":{"lights":2}})
    assert r.status_code==200
    assert r.json()["id"]>0
    assert r.json()["recommendations"]

def test_protected_route_without_login(client):
    assert client.get("/history").status_code==401
