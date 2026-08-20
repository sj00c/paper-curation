"""Filesystem adapters for Core curation persistence."""

from .configuration import FilesystemConfigWriter
from .filesystem import (
    FilesystemEvidenceVerifier,
    FilesystemPage,
    FilesystemReceipt,
    FilesystemSidecar,
    FilesystemStagedAttachment,
    FilesystemStagedReview,
)
from .workspace_ops import FilesystemWorkspaceOps

__all__ = [
    "FilesystemConfigWriter",
    "FilesystemEvidenceVerifier",
    "FilesystemPage",
    "FilesystemReceipt",
    "FilesystemSidecar",
    "FilesystemStagedAttachment",
    "FilesystemStagedReview",
    "FilesystemWorkspaceOps",
]
