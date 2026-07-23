"""Versioned metadata contract for local Deep Research search embeddings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

INDEX_SCHEMA_VERSION = 1
EMBEDDING_PROVIDER = "google"
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_TASK_TYPE = "RETRIEVAL_DOCUMENT"
EMBEDDING_DIMENSION = 768
EMBEDDING_QUANTIZATION = "int8-l2norm"
CHUNK_HASH_BASIS = "sha256(model + '\\n' + text)"
SIDECAR_FORMAT_VERSION = 1
CACHE_FORMAT_VERSION = 1
PROVENANCE_STATUS = "local-current"
EMBEDDING_SIDECAR_FILE = "_search_index_emb.bin"

KEY_INDEX_SCHEMA_VERSION = "index_schema_version"
KEY_EMBEDDING_PROVIDER = "embedding_provider"
KEY_EMBEDDING_MODEL = "embedding_model"
KEY_EMBEDDING_TASK_TYPE = "embedding_task_type"
KEY_EMBEDDING_DIMENSION = "embedding_dimension"
KEY_EMBEDDING_QUANTIZATION = "embedding_quantization"
KEY_CHUNK_HASH_BASIS = "chunk_hash_basis"
KEY_SIDECAR_FORMAT_VERSION = "sidecar_format_version"
KEY_CACHE_FORMAT_VERSION = "cache_format_version"
KEY_SOURCE_PROVENANCE_APPROVAL_STATUS = "source_provenance_approval_status"

REBUILD_GUIDANCE = (
    "Rebuild the local search index with pipeline/build_search_index.py; "
    "validation never rebuilds automatically."
)

_CANONICAL_CONTRACT_KEYS = frozenset({
    KEY_INDEX_SCHEMA_VERSION,
    KEY_EMBEDDING_PROVIDER,
    KEY_EMBEDDING_MODEL,
    KEY_EMBEDDING_TASK_TYPE,
    KEY_EMBEDDING_DIMENSION,
    KEY_EMBEDDING_QUANTIZATION,
    KEY_CHUNK_HASH_BASIS,
    KEY_SIDECAR_FORMAT_VERSION,
    KEY_CACHE_FORMAT_VERSION,
    KEY_SOURCE_PROVENANCE_APPROVAL_STATUS,
})

_LEGACY_CONTRACT_KEY_MAP = {
    "model": KEY_EMBEDDING_MODEL,
    "dim": KEY_EMBEDDING_DIMENSION,
    "quant": KEY_EMBEDDING_QUANTIZATION,
}
_LEGACY_CONTRACT_KEYS = frozenset(_LEGACY_CONTRACT_KEY_MAP)
_SHORTENED_VERSIONED_CONTRACT_KEYS = frozenset({
    "schema_version",
    "provider",
    "task_type",
    "provenance_status",
})
_SHARED_CONTRACT_KEYS = _CANONICAL_CONTRACT_KEYS.intersection(_LEGACY_CONTRACT_KEYS)
_CANONICAL_ONLY_CONTRACT_KEYS = _CANONICAL_CONTRACT_KEYS - _SHARED_CONTRACT_KEYS
_LEGACY_ONLY_CONTRACT_KEYS = _LEGACY_CONTRACT_KEYS - _SHARED_CONTRACT_KEYS
_VERSIONED_SHARED_CONTRACT_KEYS = frozenset({
    KEY_CHUNK_HASH_BASIS,
    KEY_SIDECAR_FORMAT_VERSION,
    KEY_CACHE_FORMAT_VERSION,
})


def _expected_contract_keys(expected: Mapping[str, Any]) -> frozenset[str]:
    return frozenset(expected) - {"emb_file"}


def _contract_shape_error(payload: Mapping[str, Any], expected: Mapping[str, Any]) -> str | None:
    """Reject mixed/partial versioned metadata before value validation."""
    if not isinstance(payload, Mapping):
        return None

    expected_keys = _expected_contract_keys(expected)
    canonical_only_hits = (_CANONICAL_ONLY_CONTRACT_KEYS & expected_keys).intersection(payload)
    legacy_only_hits = _LEGACY_ONLY_CONTRACT_KEYS.intersection(payload)
    shared_hits = (_VERSIONED_SHARED_CONTRACT_KEYS & expected_keys).intersection(payload)
    shortened_versioned_hits = _SHORTENED_VERSIONED_CONTRACT_KEYS.intersection(payload)
    canonical_complete = expected_keys.issubset(payload)

    if shortened_versioned_hits:
        return "shortened versioned metadata is not known-safe legacy"
    if canonical_only_hits and legacy_only_hits:
        return "mixed canonical and legacy metadata is not known-safe legacy"
    if canonical_only_hits and not canonical_complete:
        return "partial canonical metadata is not known-safe legacy"
    if shared_hits and not canonical_complete:
        return "partial versioned metadata is not known-safe legacy"
    return None


@dataclass(frozen=True)
class MetadataValidationResult:
    """Operator-facing metadata validation result."""

    ok: bool
    errors: tuple[str, ...] = ()
    is_legacy: bool = False

    def require(self) -> None:
        """Raise ValueError with rebuild guidance when validation failed."""
        if not self.ok:
            raise ValueError("; ".join(self.errors))


def current_index_metadata(model: str = EMBEDDING_MODEL) -> dict[str, Any]:
    """Return authoritative metadata fields for a newly written index."""
    return {
        KEY_INDEX_SCHEMA_VERSION: INDEX_SCHEMA_VERSION,
        KEY_EMBEDDING_PROVIDER: EMBEDDING_PROVIDER,
        KEY_EMBEDDING_MODEL: model,
        KEY_EMBEDDING_TASK_TYPE: EMBEDDING_TASK_TYPE,
        KEY_EMBEDDING_DIMENSION: EMBEDDING_DIMENSION,
        KEY_EMBEDDING_QUANTIZATION: EMBEDDING_QUANTIZATION,
        KEY_CHUNK_HASH_BASIS: CHUNK_HASH_BASIS,
        KEY_SIDECAR_FORMAT_VERSION: SIDECAR_FORMAT_VERSION,
        KEY_CACHE_FORMAT_VERSION: CACHE_FORMAT_VERSION,
        KEY_SOURCE_PROVENANCE_APPROVAL_STATUS: PROVENANCE_STATUS,
        "emb_file": EMBEDDING_SIDECAR_FILE,
    }


def current_cache_metadata(model: str = EMBEDDING_MODEL) -> dict[str, Any]:
    """Return authoritative metadata fields for a newly written embedding cache."""
    return {
        KEY_CACHE_FORMAT_VERSION: CACHE_FORMAT_VERSION,
        KEY_EMBEDDING_PROVIDER: EMBEDDING_PROVIDER,
        KEY_EMBEDDING_MODEL: model,
        KEY_EMBEDDING_TASK_TYPE: EMBEDDING_TASK_TYPE,
        KEY_EMBEDDING_DIMENSION: EMBEDDING_DIMENSION,
        KEY_EMBEDDING_QUANTIZATION: EMBEDDING_QUANTIZATION,
        KEY_CHUNK_HASH_BASIS: CHUNK_HASH_BASIS,
        KEY_SOURCE_PROVENANCE_APPROVAL_STATUS: PROVENANCE_STATUS,
    }


def canonicalize_index_metadata(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy whose recognized legacy metadata keys are canonicalized."""
    return _canonicalize_metadata(payload)


def canonicalize_cache_metadata(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy whose recognized legacy metadata keys are canonicalized."""
    return _canonicalize_metadata(payload)


def metadata_dimension(payload: Mapping[str, Any]) -> int:
    """Return the canonical embedding dimension, with explicit legacy fallback."""
    return int(payload.get(KEY_EMBEDDING_DIMENSION) or payload.get("dim") or 0)


def format_validation_errors(asset_name: str, result: MetadataValidationResult) -> str:
    """Format validation errors with explicit, non-automatic rebuild guidance."""
    if result.ok:
        return ""
    return f"{asset_name} metadata is incompatible: {'; '.join(result.errors)}"


def validate_index_metadata(
    payload: Mapping[str, Any],
    *,
    model: str = EMBEDDING_MODEL,
    allow_legacy: bool = True,
) -> MetadataValidationResult:
    """Validate index metadata for cache seeding and vector compatibility."""
    expected = current_index_metadata(model)
    shape_error = _contract_shape_error(payload, expected)
    if shape_error:
        return MetadataValidationResult(ok=False, errors=(_with_guidance(shape_error),))
    current_errors = _validate_fields(payload, expected, "index")
    if not current_errors:
        return MetadataValidationResult(ok=True)
    if allow_legacy:
        legacy = validate_known_safe_legacy_index(payload, model=model)
        if legacy.ok:
            return legacy
    return MetadataValidationResult(ok=False, errors=tuple(current_errors))


def validate_cache_metadata(
    payload: Mapping[str, Any],
    *,
    model: str = EMBEDDING_MODEL,
    allow_legacy: bool = True,
) -> MetadataValidationResult:
    """Validate embedding cache metadata before accepting cache hits."""
    expected = current_cache_metadata(model)
    shape_error = _contract_shape_error(payload, expected)
    if shape_error:
        return MetadataValidationResult(ok=False, errors=(_with_guidance(shape_error),))
    current_errors = _validate_fields(payload, expected, "cache")
    if not current_errors:
        return MetadataValidationResult(ok=True)
    if allow_legacy:
        legacy = validate_known_safe_legacy_cache(payload, model=model)
        if legacy.ok:
            return legacy
    return MetadataValidationResult(ok=False, errors=tuple(current_errors))


def validate_known_safe_legacy_index(
    payload: Mapping[str, Any],
    *,
    model: str = EMBEDDING_MODEL,
) -> MetadataValidationResult:
    """Accept only complete known-safe legacy index metadata shapes."""
    return _validate_known_safe_legacy(payload, current_index_metadata(model), "index")


def validate_known_safe_legacy_cache(
    payload: Mapping[str, Any],
    *,
    model: str = EMBEDDING_MODEL,
) -> MetadataValidationResult:
    """Accept only complete known-safe legacy cache metadata shapes."""
    result = _validate_known_safe_legacy(payload, current_cache_metadata(model), "cache")
    if result.ok and not isinstance(payload.get("emb"), Mapping):
        return MetadataValidationResult(
            ok=False,
            errors=(_with_guidance("emb must be a mapping"),),
            is_legacy=True,
        )
    return result


def _validate_known_safe_legacy(
    payload: Mapping[str, Any],
    expected: Mapping[str, Any],
    asset: str,
) -> MetadataValidationResult:
    if not isinstance(payload, Mapping):
        return MetadataValidationResult(
            ok=False,
            errors=(_with_guidance("metadata missing"),),
            is_legacy=True,
        )

    expected_keys = _expected_contract_keys(expected)
    canonical_hits = (_CANONICAL_ONLY_CONTRACT_KEYS & expected_keys).intersection(payload)
    legacy_hits = _LEGACY_ONLY_CONTRACT_KEYS.intersection(payload)
    shared_hits = (_VERSIONED_SHARED_CONTRACT_KEYS & expected_keys).intersection(payload)
    shortened_versioned_hits = _SHORTENED_VERSIONED_CONTRACT_KEYS.intersection(payload)
    if shortened_versioned_hits:
        return MetadataValidationResult(
            ok=False,
            errors=(_with_guidance("shortened versioned metadata is not known-safe legacy"),),
            is_legacy=True,
        )
    if canonical_hits and legacy_hits:
        return MetadataValidationResult(
            ok=False,
            errors=(_with_guidance("mixed canonical and legacy metadata is not known-safe legacy"),),
            is_legacy=True,
        )
    if canonical_hits:
        return MetadataValidationResult(
            ok=False,
            errors=(_with_guidance("partial canonical metadata is not known-safe legacy"),),
            is_legacy=True,
        )
    if shared_hits:
        return MetadataValidationResult(
            ok=False,
            errors=(_with_guidance("partial versioned metadata is not known-safe legacy"),),
            is_legacy=True,
        )

    errors: list[str] = []
    if payload.get("model") != expected[KEY_EMBEDDING_MODEL]:
        errors.append(_err("model", expected[KEY_EMBEDDING_MODEL], payload.get("model")))
    if asset == "index":
        if payload.get("dim") != EMBEDDING_DIMENSION:
            errors.append(_err("dim", EMBEDDING_DIMENSION, payload.get("dim")))
        if payload.get("quant") != EMBEDDING_QUANTIZATION:
            errors.append(_err("quant", EMBEDDING_QUANTIZATION, payload.get("quant")))
        emb_file = payload.get("emb_file")
        if emb_file not in (None, EMBEDDING_SIDECAR_FILE):
            errors.append(_err("emb_file", EMBEDDING_SIDECAR_FILE, emb_file))
    else:
        emb = payload.get("emb")
        if not isinstance(emb, Mapping):
            errors.append("emb must be a mapping")
        elif "count" in payload and payload.get("count") != len(emb):
            errors.append(_err("count", len(emb), payload.get("count")))
        if any(key in payload for key in ("dim", "quant")):
            if payload.get("dim") != EMBEDDING_DIMENSION:
                errors.append(_err("dim", EMBEDDING_DIMENSION, payload.get("dim")))
            if payload.get("quant") != EMBEDDING_QUANTIZATION:
                errors.append(_err("quant", EMBEDDING_QUANTIZATION, payload.get("quant")))
    if errors:
        return MetadataValidationResult(ok=False, errors=tuple(_with_guidance(e) for e in errors), is_legacy=True)
    return MetadataValidationResult(ok=True, is_legacy=True)


def _canonicalize_metadata(payload: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(payload)
    for legacy_key, canonical_key in _LEGACY_CONTRACT_KEY_MAP.items():
        if legacy_key in out and legacy_key != canonical_key:
            out[canonical_key] = out[legacy_key]
            del out[legacy_key]
    return out


def _validate_fields(payload: Mapping[str, Any], expected: Mapping[str, Any], asset: str) -> list[str]:
    errors: list[str] = []
    for key, want in expected.items():
        got = payload.get(key)
        if got != want:
            errors.append(_with_guidance(_err(key, want, got)))
    if asset == "index" and payload.get("emb_file") != EMBEDDING_SIDECAR_FILE:
        errors.append(_with_guidance(_err("emb_file", EMBEDDING_SIDECAR_FILE, payload.get("emb_file"))))
    return errors


def _err(key: str, expected: Any, actual: Any) -> str:
    return f"{key} expected {expected!r}, got {actual!r}"


def _with_guidance(message: str) -> str:
    return f"{message}. {REBUILD_GUIDANCE}"
