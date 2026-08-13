"""Side-effect-free public foundation for Paper Curation."""

from .capabilities import Capabilities, detect_capabilities
from .config.loader import load_config
from .config.models import AppConfig
from .workspace import Workspace

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "AppConfig",
    "Capabilities",
    "Workspace",
    "detect_capabilities",
    "load_config",
]
