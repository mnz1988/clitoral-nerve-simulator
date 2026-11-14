"""Error type for configuration problems."""


class ConfigError(ValueError):
    """A configuration file or value is invalid. The message says which field and why."""
