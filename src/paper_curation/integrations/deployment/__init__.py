"""Deployment adapters."""

from paper_curation.integrations.deployment.cloudflare import CloudflareDeployment, DeploymentError

__all__ = ("CloudflareDeployment", "DeploymentError")
