"""Concrete adapters for explicitly selected Core providers."""

from paper_curation.integrations.providers.review import (
    AnthropicAPIReviewAdapter,
    ClaudeCodeOAuthReviewAdapter,
    LocalModelReviewAdapter,
    REQUIRED_REVIEW_SECTIONS,
    ReviewProviderError,
    build_review_prompt,
)

__all__ = (
    "AnthropicAPIReviewAdapter",
    "ClaudeCodeOAuthReviewAdapter",
    "LocalModelReviewAdapter",
    "REQUIRED_REVIEW_SECTIONS",
    "ReviewProviderError",
    "build_review_prompt",
)
