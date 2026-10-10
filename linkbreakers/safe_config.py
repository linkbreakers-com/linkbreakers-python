"""
Type-safe configuration for Linkbreakers SDK

This module provides a type-safe Configuration class that prevents the common
mistake of using `api_key` instead of `access_token`.

✅ CORRECT: Use `access_token` for Bearer token authentication
❌ INCORRECT: Using `api_key` is not supported and will raise an error

For more information, see:
https://linkbreakers.com/help/article/api-authentication-accesstoken-vs-apikey
"""

from typing import Optional
import warnings


class LinkbreakersConfiguration:
    """
    Type-safe configuration class that only accepts Bearer token authentication

    This wrapper prevents you from accidentally using the wrong authentication
    parameter. The Linkbreakers API requires Bearer token authentication via
    the `access_token` parameter.

    Args:
        access_token: Your Linkbreakers API token (Bearer token)
                     Get this from: https://app.linkbreakers.com/settings/api
        host: API base URL (default: https://api.linkbreakers.com)

    Example:
        >>> config = LinkbreakersConfiguration(
        ...     access_token='your-api-token',
        ...     host='https://api.linkbreakers.com'
        ... )

    Raises:
        ValueError: If you try to pass `api_key` instead of `access_token`
    """

    def __init__(
        self,
        access_token: str,
        host: str = 'https://api.linkbreakers.com',
        **kwargs
    ):
        """
        Initialize Linkbreakers configuration

        Args:
            access_token: Your Linkbreakers API token (Bearer token)
            host: API base URL (optional, defaults to production)
            **kwargs: Additional parameters (for internal use)

        Raises:
            ValueError: If `api_key` is passed instead of `access_token`
        """
        # Explicitly check for the wrong parameter
        if 'api_key' in kwargs:
            raise ValueError(
                "❌ INCORRECT: Do not use `api_key`. "
                "Use `access_token` instead for Bearer token authentication.\n"
                "See: https://linkbreakers.com/help/article/api-authentication-accesstoken-vs-apikey"
            )

        # Store configuration
        self.access_token = access_token
        self.host = host
        self._extra_kwargs = kwargs

    def to_openapi_config(self):
        """
        Convert to OpenAPI Generator Configuration object

        Returns:
            Configuration: OpenAPI Generator configuration object
        """
        from linkbreakers.configuration import Configuration as OpenAPIConfiguration

        return OpenAPIConfiguration(
            access_token=self.access_token,
            host=self.host,
            **self._extra_kwargs
        )


# Monkey-patch warning for direct Configuration usage
def _create_safe_configuration_class():
    """Create a Configuration class that warns about unsafe usage"""
    from linkbreakers.configuration import Configuration as OriginalConfiguration

    class SafeConfiguration(OriginalConfiguration):
        """
        Safe Configuration wrapper with validation

        This class extends the auto-generated Configuration to add validation
        that prevents common authentication mistakes.
        """

        def __init__(self, *args, **kwargs):
            # Check if user is trying to use api_key dictionary
            if 'api_key' in kwargs and isinstance(kwargs.get('api_key'), dict):
                warnings.warn(
                    "⚠️  Using `api_key={'ApiKeyAuth': '...'}` is deprecated. "
                    "Please use `access_token='your-token'` instead for Bearer authentication. "
                    "See: https://linkbreakers.com/help/article/api-authentication-accesstoken-vs-apikey",
                    DeprecationWarning,
                    stacklevel=2
                )

            # Check if they passed access_token - this is correct
            if 'access_token' not in kwargs and 'api_key' not in kwargs:
                raise ValueError(
                    "❌ Missing authentication parameter. "
                    "You must provide `access_token='your-token'` for Bearer authentication.\n"
                    "See: https://linkbreakers.com/help/article/api-authentication-accesstoken-vs-apikey"
                )

            super().__init__(*args, **kwargs)

    return SafeConfiguration


# Export the safe Configuration class as the default
Configuration = _create_safe_configuration_class()

__all__ = ['LinkbreakersConfiguration', 'Configuration']
