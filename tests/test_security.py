"""La API no debe arrancar con la contraseña de ejemplo de la base de datos."""

import pytest

from app.database import build_database_url


@pytest.mark.parametrize("password", ["", "change_this_password"])
def test_insecure_password_is_rejected(monkeypatch, password):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DB_PASSWORD", password)
    with pytest.raises(RuntimeError, match="DB_PASSWORD"):
        build_database_url()


def test_real_password_builds_postgres_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DB_PASSWORD", "S3gura-2026")
    assert build_database_url().startswith("postgresql://team_notes_user:S3gura-2026@")
