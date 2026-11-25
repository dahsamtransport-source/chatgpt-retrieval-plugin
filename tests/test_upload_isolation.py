"""Synthetic upload tests: no datastore, credentials, or external APIs."""
import asyncio
from io import BytesIO
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, UploadFile
from starlette.datastructures import Headers
from services import file as service


def upload(payload, mime="text/plain"):
    return UploadFile(file=BytesIO(payload), filename="synthetic.txt",
                      headers=Headers({"content-type": mime}))


@pytest.mark.asyncio
async def test_concurrent_uploads_are_isolated():
    values = await asyncio.gather(*[
        service.extract_text_from_form_file(upload(f"synthetic-{i}".encode()))
        for i in range(20)
    ])
    assert values == [f"synthetic-{i}" for i in range(20)]


@pytest.mark.asyncio
async def test_oversized_input_is_rejected(monkeypatch):
    monkeypatch.setattr(service, "MAX_UPLOAD_BYTES", 4)
    with pytest.raises(HTTPException) as err:
        await service.extract_text_from_form_file(upload(b"12345"))
    assert err.value.status_code == 413


@pytest.mark.asyncio
async def test_unsupported_type_is_rejected():
    with pytest.raises(HTTPException) as err:
        await service.extract_text_from_form_file(upload(b"abc", "application/octet-stream"))
    assert err.value.status_code == 415


@pytest.mark.asyncio
async def test_parse_failure_is_sanitized(monkeypatch):
    monkeypatch.setattr(service, "run_in_threadpool", AsyncMock(side_effect=ValueError("synthetic secret")))
    with pytest.raises(HTTPException) as err:
        await service.extract_text_from_form_file(upload(b"abc"))
    assert err.value.status_code == 422
    assert err.value.detail == "Unable to parse document"
