"""Tests for the FastAPI endpoints."""

from fastapi.testclient import TestClient

from cli_file_processor.api import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_scan_default_returns_txt_files() -> None:
    response = client.get("/scan")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "files" in data
    assert isinstance(data["files"], list)


def test_scan_with_extension_filter() -> None:
    response = client.get("/scan?extension=.txt&input_dir=data/input")
    assert response.status_code == 200
    data = response.json()
    for f in data["files"]:
        assert f["extension"] == ".txt"


def test_scan_nonexistent_dir_returns_404() -> None:
    response = client.get("/scan?input_dir=/nonexistent/path/xyz")
    assert response.status_code == 404
    assert "не найдена" in response.json()["detail"]


def test_scan_file_as_dir_returns_400(tmp_path: object) -> None:
    import tempfile

    with tempfile.NamedTemporaryFile() as f:
        response = client.get(f"/scan?input_dir={f.name}")
        assert response.status_code == 400
        assert "не папка" in response.json()["detail"]


def test_scan_recursive_param_accepted() -> None:
    response = client.get("/scan?recursive=true&input_dir=data/input")
    assert response.status_code == 200


def test_scan_file_info_fields() -> None:
    response = client.get("/scan?extension=.txt&input_dir=data/input")
    assert response.status_code == 200
    files = response.json()["files"]
    if files:
        f = files[0]
        assert "name" in f
        assert "path" in f
        assert "size" in f
        assert "extension" in f
