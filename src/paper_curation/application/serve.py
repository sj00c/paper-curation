"""Planning contract for serving a pre-built local static site."""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass
from pathlib import Path

_HOSTNAME = re.compile(
    r"(?=.{1,253}\Z)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)*"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\Z"
)


def _validated_site_root(value: str | Path) -> Path:
    if not isinstance(value, (str, Path)):
        raise ValueError("site_root must be a filesystem path")
    raw = str(value)
    if not raw or "\x00" in raw:
        raise ValueError("site_root must be a non-empty filesystem path")
    try:
        root = Path(value).expanduser().resolve(strict=True)
    except FileNotFoundError as error:
        raise ValueError("site_root does not exist") from error
    if not root.is_dir():
        raise ValueError("site_root must be a directory")
    if not (root / "index.html").is_file():
        raise ValueError("site_root must contain index.html")
    return root


def _is_loopback_host(host: str) -> bool:
    if host.casefold() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _validated_host(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("host must be a string")
    host = value.strip()
    if not host or "\x00" in host or "/" in host or "\\" in host:
        raise ValueError("host is invalid")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if not _HOSTNAME.fullmatch(host):
            raise ValueError("host is invalid")
    return host


@dataclass(frozen=True, slots=True)
class ServeSiteRequest:
    """Explicit, validated inputs for a local static-site server."""

    site_root: str | Path
    host: str = "127.0.0.1"
    port: int = 8000
    allow_public_bind: bool = False

    def __post_init__(self) -> None:
        root = _validated_site_root(self.site_root)
        host = _validated_host(self.host)
        if isinstance(self.port, bool) or not isinstance(self.port, int) or not 0 <= self.port <= 65535:
            raise ValueError("port must be an integer from 0 through 65535")
        if not isinstance(self.allow_public_bind, bool):
            raise ValueError("allow_public_bind must be a boolean")
        if not _is_loopback_host(host) and not self.allow_public_bind:
            raise ValueError("refusing non-loopback bind without allow_public_bind")
        object.__setattr__(self, "site_root", root)
        object.__setattr__(self, "host", host)


@dataclass(frozen=True, slots=True)
class ServeSitePlan:
    """A side-effect-free serving plan for an already-built site."""

    site_root: Path
    host: str
    port: int
    allow_public_bind: bool


@dataclass(frozen=True, slots=True)
class ServeSite:
    """Validates a static serving request without binding a socket or writing files."""

    def plan(self, request: ServeSiteRequest) -> ServeSitePlan:
        return ServeSitePlan(
            site_root=request.site_root,
            host=request.host,
            port=request.port,
            allow_public_bind=request.allow_public_bind,
        )
