"""Retrieval integration ports and implementations."""

from paper_curation.retrieval.local import (
    LocalIndexCatalog,
    LocalLexicalRetriever,
    local_lexical_retrieval_use_case,
)

__all__ = [
    "LocalIndexCatalog",
    "LocalLexicalRetriever",
    "local_lexical_retrieval_use_case",
]
