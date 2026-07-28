"""Fail-closed TLS context helper for outbound network clients."""

import os
import ssl
from collections.abc import Mapping

INSECURE_TLS_ENV = "PAPER_CURATION_INSECURE_TLS"


def _insecure_requested(config):
    if os.environ.get(INSECURE_TLS_ENV):
        return True
    if not isinstance(config, Mapping):
        return False
    network = config.get("network")
    return isinstance(network, Mapping) and (
        "allow_insecure_tls" in network or "insecure_tls_reason" in network
    )


def create_ssl_context(*, purpose="default", config=None):
    """Return a certificate- and hostname-verifying TLS context.

    Disabling verification is not a supported runtime mode. Any legacy
    environment or config request for insecure TLS fails before a connection.
    """
    if _insecure_requested(config):
        raise ValueError(
            "insecure TLS is unsupported; install the trusted CA in the OS/Python "
            "trust store or configure SSL_CERT_FILE/REQUESTS_CA_BUNDLE"
        )
    ssl_purpose = purpose if isinstance(purpose, ssl.Purpose) else ssl.Purpose.SERVER_AUTH
    return ssl.create_default_context(purpose=ssl_purpose)
