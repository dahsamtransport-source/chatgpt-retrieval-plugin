"""Encode data as scalar literals instead of concatenating expression syntax."""
import json
from models.models import DocumentMetadataFilter
from services.date import to_unix_timestamp


def string_literal(value: str) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def primary_key_literal(value, schema_version: str) -> str:
    return str(int(value)) if schema_version == "V1" else string_literal(value)


def metadata_expression(metadata: DocumentMetadataFilter) -> str:
    conditions = []
    for field, value in metadata.dict().items():
        if value is None:
            continue
        if field == "start_date":
            conditions.append(f"(created_at >= {to_unix_timestamp(value)})")
        elif field == "end_date":
            conditions.append(f"(created_at <= {to_unix_timestamp(value)})")
        elif field in ("document_id", "source", "source_id", "author"):
            conditions.append(f"({field} == {string_literal(value.value if field == 'source' else value)})")
        else:
            raise ValueError("Unsupported metadata filter")
    return " and ".join(conditions)
