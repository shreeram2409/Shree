from app import app

def test_homepage():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Python Web Security Lab" in response.data

def test_security_headers():
    client = app.test_client()
    response = client.get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "Content-Security-Policy" in response.headers

def test_output_is_escaped():
    client = app.test_client()
    response = client.post("/profile", data={"nickname": "<b>hello</b>"})
    assert b"&lt;b&gt;hello&lt;/b&gt;" in response.data
