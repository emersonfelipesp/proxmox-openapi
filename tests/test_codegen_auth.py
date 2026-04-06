import os
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from proxmox_openapi.routes.codegen import router

app = FastAPI()
app.include_router(router, prefix="/codegen")

client = TestClient(app)


def test_codegen_generate_missing_api_key_env():
    with patch.dict(os.environ, clear=True):
        response = client.post("/codegen/generate")
        assert response.status_code == 403
        assert "CODEGEN_API_KEY environment variable must be set" in response.json()["detail"]


def test_codegen_generate_missing_auth_header():
    with patch.dict(os.environ, {"CODEGEN_API_KEY": "secret-key"}):
        response = client.post("/codegen/generate")
        assert response.status_code == 401
        assert "Invalid or missing API key" in response.json()["detail"]


def test_codegen_generate_invalid_auth_header():
    with patch.dict(os.environ, {"CODEGEN_API_KEY": "secret-key"}):
        response = client.post(
            "/codegen/generate", headers={"Authorization": "Bearer wrong-key"}
        )
        assert response.status_code == 401
        assert "Invalid or missing API key" in response.json()["detail"]


@pytest.mark.asyncio
async def test_codegen_generate_valid_auth_header():
    with patch.dict(os.environ, {"CODEGEN_API_KEY": "secret-key"}):
        # We won't actually run the generate pipeline, just test the auth bypass
        # But wait, calling /codegen/generate will try to run Playwright.
        # We can just check if auth passes by mocking the pipeline function.
        with patch("proxmox_openapi.routes.codegen.generate_proxmox_codegen_bundle_async") as mock_generate:
            mock_generate.return_value.capture = {}
            mock_generate.return_value.source_url = "test"
            mock_generate.return_value.version_tag = "test"
            mock_generate.return_value.generated_at = "test"
            mock_generate.return_value.endpoint_count = 0
            mock_generate.return_value.operation_count = 0
            
            response = client.post(
                "/codegen/generate", headers={"Authorization": "Bearer secret-key"}
            )
            assert response.status_code == 200
            assert response.json()["message"] == "Generation completed"
