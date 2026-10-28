"""Pruebas de error: entradas inválidas deben responder 400 y no guardarse."""

import pytest

NOTE = {"title": "Sprint 1", "content": "Revisar backlog", "author": "Camilo"}


@pytest.mark.parametrize(
    "payload",
    [
        {**NOTE, "title": "   "},
        {**NOTE, "author": "\t\n"},
        {**NOTE, "title": "x" * 201},
        {**NOTE, "author": "a" * 121},
        {**NOTE, "content": "c" * 5001},
        {**NOTE, "id": 99},
    ],
    ids=["titulo-espacios", "autor-espacios", "titulo-201", "autor-121", "contenido-5001", "campo-extra"],
)
def test_invalid_note_is_rejected(client, payload):
    r = client.post("/notes", json=payload)
    assert r.status_code == 400
    assert r.json()["detail"] == "Invalid data"
    assert client.get("/notes").json() == []


def test_values_are_trimmed(client):
    r = client.post("/notes", json={**NOTE, "title": "  Sprint 1  "})
    assert r.status_code == 201
    assert r.json()["title"] == "Sprint 1"


def test_update_with_invalid_data_keeps_note(client):
    note_id = client.post("/notes", json=NOTE).json()["id"]
    r = client.put(f"/notes/{note_id}", json={**NOTE, "title": ""})
    assert r.status_code == 400
    assert client.get(f"/notes/{note_id}").json()["title"] == "Sprint 1"
