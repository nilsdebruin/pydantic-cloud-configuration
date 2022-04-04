"""Pytest fixtures."""
import os
from typing import Generator
from unittest import mock

import boto3  # type: ignore
import pytest
from factory import random  # type: ignore
from moto import mock_ssm  # type: ignore

from .parameters import ParameterFactory


RANDOM_SEED = "pydantic-cloud-settings"
BATCH_SIZE = 15

random.reseed_random(RANDOM_SEED)


@pytest.fixture
def aws_credentials() -> None:
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing1"  # noqa: S105
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing2"  # noqa: S105
    os.environ["AWS_SECURITY_TOKEN"] = "testing3"  # noqa: S105
    os.environ["AWS_SESSION_TOKEN"] = "testing4"  # noqa: S105
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"  # noqa: S105


@pytest.fixture
def ssm_mock(aws_credentials) -> Generator:  # type: ignore
    """Create a ssm mock."""
    parameters = ParameterFactory.create_batch(BATCH_SIZE)
    with mock_ssm():
        client = boto3.client("ssm")
        for parameter in parameters:
            client.put_parameter(
                Name=parameter.name,
                Description=parameter.description,
                Value=parameter.value,
                Type=parameter.type,
            )
        yield


@pytest.fixture
def mock_settings_env_vars() -> Generator[None, None, None]:
    """Set env vars."""
    with mock.patch.dict(
        os.environ, {"SETTINGS_NAME": "cloud-app", "SETTINGS_ENVIRONMENT": "dev"}
    ):
        yield
