"""Pruebas de error: fallos de la base de datos y errores inesperados."""

import logging

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.main import app
from app.repository import get_repository

NOTE = {"title": "Sprint 1", "content": "Revisar backlog", "author": "Camilo"}


class BrokenRepository:
    """Simula una base de datos caída."""

    def list(self):
        raise OperationalError("SELECT ...", {}, Exception("connection refused"))

    def get(self, note_id):
        raise OperationalError("SELECT ...", {}, Exception("connection refused"))

    def create(self, data):
        raise OperationalError("INSERT ...", {}, Exception("connection refused"))


class BuggyRepository(BrokenRepository):
    def list(self):
        raise RuntimeError("bug inesperado")


@pytest.fixture()
def client_with(client):
    def use(repo):
        app.dependency_overrides[get_repository] = lambda: repo
        return TestClient(app, raise_server_exceptions=False)

    return use


def test_database_down_returns_503(client_with, caplog):
    c = client_with(BrokenRepository())
    with caplog.at_level(logging.ERROR, logger="team_notes"):
        r = c.post("/notes", json=NOTE)
    assert r.status_code == 503
    assert r.json() == {"detail": "Database unavailable"}
    assert "connection refused" not in r.text
    assert "Database error on POST /notes" in caplog.text


def test_unexpected_error_is_logged_and_hidden(client_with, caplog):
    c = client_with(BuggyRepository())
    with caplog.at_level(logging.ERROR, logger="team_notes"):
        r = c.get("/notes")
    assert r.status_code == 500
    assert r.json() == {"detail": "Internal server error"}
    assert "bug inesperado" in caplog.text


def test_failed_commit_rolls_back(client, monkeypatch):

    calls = []

    def failing_commit(self):
        calls.append("commit")
        raise OperationalError("COMMIT", {}, Exception("disk full"))


    monkeypatch.setattr("sqlalchemy.orm.Session.commit", failing_commit)
    monkeypatch.setattr(
        "sqlalchemy.orm.Session.rollback", lambda self: calls.append("rollback")
    )
    r = TestClient(app, raise_server_exceptions=False).post("/notes", json=NOTE)
    assert r.status_code == 503
    assert calls == ["commit", "rollback"]
