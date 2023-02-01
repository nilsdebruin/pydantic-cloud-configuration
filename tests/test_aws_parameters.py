"""Test AWS parameters."""
import os
import sys
from unittest import mock

import boto3  # type: ignore # noqa: F401
import pytest
from pydantic import ValidationError

from pydantic_cloud_configuration.aws.parameter_store import AwsParameterStore
from tests.settings.settings import return_bad_config_class
from tests.settings.settings import return_bad_parameter_config
from tests.settings.settings import return_base_settings
from tests.settings.settings import return_config_class
from tests.settings.settings import return_config_class_without_prefix


def test_settings_file_without_base_settings() -> None:
    """Basic test, without base settings."""
    with pytest.raises(ValidationError) as err:
        return_base_settings()

    assert "3 validation errors for Settings" in str(err.value)


def test_boto3_not_present(mock_settings_env_vars) -> None:  # type: ignore
    """Test when boto3 is not present and AWS is used."""
    with mock.patch.dict(sys.modules, {"boto3": None}):
        with pytest.raises(ModuleNotFoundError) as err:
            return_base_settings()
    assert "Boto3 is not installed!" in str(err.value)


@mock.patch.dict(os.environ, {"test": "test"})
def test_settings_file(mock_settings_env_vars) -> None:  # type: ignore
    """Test using a settings file."""
    settings = return_base_settings()

    assert settings.settings_name == "cloud-app"
    assert settings.test == "test"  # type: ignore


def test_mock(ssm_mock, mock_settings_env_vars) -> None:  # type: ignore
    """Test ssm mock."""
    settings = return_config_class()

    assert settings.prefix_test_store == "ENHcYRmDTElyAeLXwzcB"  # type: ignore

    settings_without_locations = return_config_class(aws_parameter_locations=False)

    assert settings_without_locations.prefix_test_store != "ENHcYRmDTElyAeLXwzcB"  # type: ignore

    bad_settings = return_bad_config_class()

    assert bad_settings.prefix_test_store != "ENHcYRmDTElyAeLXwzcB"  # type: ignore

    more_bad_settings = return_bad_parameter_config()

    assert more_bad_settings.prefix_test_store != "ENHcYRmDTElyAeLXwzcB"  # type: ignore

    settings_without_prefix = return_config_class_without_prefix()

    assert settings_without_prefix.store == "ENHcYRmDTElyAeLXwzcB"  # type: ignore

    settings_without_prefix_and_locations = return_config_class_without_prefix(
        aws_parameter_locations=False
    )

    assert settings_without_prefix_and_locations.store != "ENHcYRmDTElyAeLXwzcB"  # type: ignore


def test_parameter_creation(mock_settings_env_vars) -> None:  # type: ignore
    """Test the creation of parameters to be used in settings."""
    aws_parameter = AwsParameterStore(name="Setting", check_settings=True)

    assert aws_parameter.name == "Setting"

    with mock.patch.dict(os.environ, {"SETTINGS_NAME": "", "SETTINGS_ENVIRONMENT": ""}):
        with pytest.raises(ValueError):
            AwsParameterStore(name="Setting", check_settings=True)

        aws_parameter_2 = AwsParameterStore(name="Setting")
        assert aws_parameter_2.name == "Setting"
        assert aws_parameter_2.location == "/environments/Setting"

        aws_parameter_3 = AwsParameterStore(name="Setting", location="/def")
        assert aws_parameter_3.location == "/def"

        aws_parameter_4 = AwsParameterStore(name="Setting", location_path="/def")
        assert aws_parameter_4.location_path == "/def"
        assert aws_parameter_4.location == "/def/Setting"
