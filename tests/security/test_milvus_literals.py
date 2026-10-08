import json
import pytest
from models.models import DocumentMetadataFilter, Source
from services.milvus_filters import metadata_expression, primary_key_literal, string_literal


@pytest.mark.parametrize("value", ['x\") or author != (\"', 'a\\\"b', 'quote"\n\tend', 'دواء', ""])
def test_string_payload_is_one_literal(value):
    # Decoder must consume the entire literal, leaving no injected expression.
    decoded, end = json.JSONDecoder().raw_decode(string_literal(value))
    assert decoded == value
    assert end == len(string_literal(value))


@pytest.mark.parametrize("field", ["document_id", "source_id", "author"])
def test_metadata_text_cannot_escape_its_literal(field):
    value = 'x") or author != "'
    expression = metadata_expression(DocumentMetadataFilter(**{field: value}))
    literal = expression[len(f"({field} == "):-1]
    assert json.loads(literal) == value


def test_source_enum_dates_empty_filter_and_primary_keys():
    assert metadata_expression(DocumentMetadataFilter()) == ""
    assert metadata_expression(DocumentMetadataFilter(source=Source.file)) == '(source == "file")'
    assert metadata_expression(DocumentMetadataFilter(start_date="2024-01-01", end_date="2024-01-02")) == '(created_at >= 1704067200) and (created_at <= 1704153600)'
    assert primary_key_literal(123, "V1") == "123"
    with pytest.raises(ValueError):
        primary_key_literal('1] or pk > 0', "V1")
    assert json.loads(primary_key_literal('x"\\', "V2")) == 'x"\\'
