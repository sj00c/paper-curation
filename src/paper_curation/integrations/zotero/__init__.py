"""Read-only Zotero adapters for paper curation."""

from paper_curation.integrations.zotero.api import (
    ZoteroStorageAttachmentPort,
    ZoteroStorageSource,
)
from paper_curation.integrations.zotero.local import (
    ZoteroLocalAttachmentPort,
    ZoteroLocalSource,
)

__all__ = (
    "ZoteroLocalAttachmentPort",
    "ZoteroLocalSource",
    "ZoteroStorageAttachmentPort",
    "ZoteroStorageSource",
)
