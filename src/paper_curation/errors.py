"""Errors raised while parsing local configuration."""


class ConfigError(ValueError):
    """Base class for configuration errors that never exposes secret values."""

    def __init__(self, path: str, message: str) -> None:
        self.path = path
        super().__init__(f"Invalid configuration at {path}: {message}")


class ConfigTypeError(ConfigError):
    """A configuration value has the wrong JSON shape."""


class ConfigValidationError(ConfigError):
    """A configuration value has an invalid value."""


class ConfigFileError(ConfigError):
    """A configuration file cannot be read or decoded."""
