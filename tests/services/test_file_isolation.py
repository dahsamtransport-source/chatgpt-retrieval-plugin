import asyncio
from io import BytesIO
from threading import Barrier
from unittest.mock import Mock, patch

import pytest
from fastapi import UploadFile
from starlette.datastructures import Headers
from services.file import extract_text_from_file, extract_text_from_form_file


def upload(text, mime="text/plain"):
    return UploadFile(filename="same.txt", file=BytesIO(text.encode()),
                      headers=Headers({"content-type": mime}))


@pytest.mark.asyncio
async def test_overlapping_parsers_only_read_their_own_request():
    barrier = Barrier(2, timeout=5)
    parser = extract_text_from_file
    def overlap(stream, mime):
        barrier.wait()
        return parser(stream, mime)
    files = [upload("first private document"), upload("second private document")]
    try:
        with patch("services.file.extract_text_from_file", side_effect=overlap):
            result = await asyncio.gather(*(extract_text_from_form_file(f) for f in files))
        assert result == ["first private document", "second private document"]
    finally:
        for f in files:
            await f.close()


@pytest.mark.asyncio
async def test_failed_parser_does_not_damage_next_upload():
    bad, good = upload("bad", "application/unknown"), upload("good")
    try:
        with pytest.raises(ValueError, match="Unsupported file type"):
            await extract_text_from_form_file(bad)
        assert await extract_text_from_form_file(good) == "good"
    finally:
        await bad.close()
        await good.close()


@pytest.mark.asyncio
async def test_upload_is_rewound_and_kept_owned_by_request():
    f = upload("complete")
    await f.read(3)
    try:
        assert await extract_text_from_form_file(f) == "complete"
        assert not f.file.closed
    finally:
        await f.close()


def test_pdf_without_text_does_not_crash_join():
    reader = Mock(pages=[Mock(extract_text=Mock(return_value=None)),
                         Mock(extract_text=Mock(return_value="text"))])
    with patch("services.file.PdfReader", return_value=reader):
        assert extract_text_from_file(BytesIO(), "application/pdf") == " text"
