"""Pruebas de comportamiento normal: deben pasar antes y después de refactorizar."""

NOTE = {"title": "Sprint 1", "content": "Revisar backlog", "author": "Santiago"}


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_get_note(client):
    r = client.post("/notes", json=NOTE)
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Sprint 1"
    assert "created_at" in body

    r = client.get(f"/notes/{body['id']}")
    assert r.status_code == 200
    assert r.json()["author"] == "Santiago"


def test_list_notes(client):
    client.post("/notes", json=NOTE)
    client.post("/notes", json={**NOTE, "title": "Sprint 2"})
    r = client.get("/notes")
    assert r.status_code == 200
    assert [n["title"] for n in r.json()] == ["Sprint 1", "Sprint 2"]


def test_update_note(client):
    note_id = client.post("/notes", json=NOTE).json()["id"]
    r = client.put(f"/notes/{note_id}", json={**NOTE, "content": "Backlog revisado"})
    assert r.status_code == 200
    assert r.json()["content"] == "Backlog revisado"


def test_delete_note(client):
    note_id = client.post("/notes", json=NOTE).json()["id"]
    assert client.delete(f"/notes/{note_id}").status_code == 204
    assert client.get(f"/notes/{note_id}").status_code == 404


def test_not_found_returns_404(client):
    for method in ("get", "delete"):
        r = getattr(client, method)("/notes/999")
        assert r.status_code == 404
        assert r.json()["detail"] == "Note not found"
    r = client.put("/notes/999", json=NOTE)
    assert r.status_code == 404


def test_missing_fields_returns_400(client):
    r = client.post("/notes", json={"title": "Sin contenido"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Invalid data"
