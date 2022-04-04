"""Basic settings test."""
import os

import pytest
from pydantic import ValidationError

from pydantic_cloud_settings.cloud_base_settings import CloudBaseSettings


def test_basic_settings() -> None:
    """Basic settings test."""
    cloud_base_settings = CloudBaseSettings(
        settings_name="new_setting", settings_environment="local"
    )
    assert cloud_base_settings.settings_name == "new_setting"
    assert cloud_base_settings.settings_environment == "local"


def test_os_env_settings() -> None:
    """Os settings test."""
    os.environ["settings_name"] = "new_setting"
    os.environ["settings_environment"] = "local"
    cloud_base_settings = CloudBaseSettings()
    os.environ.clear()
    assert cloud_base_settings.settings_name == "new_setting"
    assert cloud_base_settings.settings_environment == "local"


def test_settings_name_not_present() -> None:
    """Missing settings test."""
    with pytest.raises(ValidationError) as err:
        CloudBaseSettings()

    settings_errors = err.value.errors()
    assert settings_errors[0].get("msg") == "field required"
    assert settings_errors[0].get("type") == "value_error.missing"
