"""TLS context helpers for outbound network clients."""

import os
import ssl
import warnings
from collections.abc import Mapping

INSECURE_TLS_ENV = "PAPER_CURATION_INSECURE_TLS"


def _network_config(config):
    if not isinstance(config, Mapping):
        return {}
    network = config.get("network", {})
    if isinstance(network, Mapping):
        return network
    return {}


def _insecure_source(config):
    if os.environ.get(INSECURE_TLS_ENV) == "1":
        return f"environment variable {INSECURE_TLS_ENV}=1"

    network = _network_config(config)
    reason = network.get("insecure_tls_reason")
    if network.get("allow_insecure_tls") is True and isinstance(reason, str) and reason.strip():
        return "config network.allow_insecure_tls with network.insecure_tls_reason"

    return None


def _warning_message(purpose, source):
    return (
        f"WARNING: TLS certificate and hostname verification disabled for {purpose} by {source} opt-out. "
        "This is insecure and should only be temporary. Remediate by installing the proxy or CA certificate "
        "in the OS/Python trust store, or set SSL_CERT_FILE or REQUESTS_CA_BUNDLE to a trusted CA bundle."
    )


def create_ssl_context(*, purpose="default", config=None):
    """Return an outbound TLS context that verifies certificates by default.

    Insecure TLS is permitted only by the exact environment opt-out
    PAPER_CURATION_INSECURE_TLS=1, or by config with
    network.allow_insecure_tls true and a nonempty network.insecure_tls_reason.
    """
    ssl_purpose = purpose if isinstance(purpose, ssl.Purpose) else ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose=ssl_purpose)

    source = _insecure_source(config)
    if source is None:
        return context

    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    warnings.warn(_warning_message(purpose, source), RuntimeWarning, stacklevel=2)
    return context
