"""Test settings."""
from typing import Any
from typing import List
from typing import Tuple

from pydantic_cloud_configuration.aws.parameter_store import (  # noqa: E402
    AwsParameterStore,
)
from pydantic_cloud_configuration.aws.parameter_store import (  # noqa: E402
    aws_parameter_settings,
)
from pydantic_cloud_configuration.cloud_base_settings import (  # noqa: E402
    CloudBaseSettings,
)
from pydantic_cloud_configuration.cloud_settings import CloudSettings


def return_config_class(
    aws_parameter_locations: bool = True,
) -> CloudSettings:
    """Return an inherited config class."""
    if aws_parameter_locations:
        CloudSettingsTest = CloudSettings(  # noqa: N806
            aws_parameter_locations=[
                AwsParameterStore(
                    name="store",
                    output_prefix="prefix_test",
                )
            ]
        )
    else:
        CloudSettingsTest = CloudSettings(aws_parameter_locations=[])  # noqa: N806

    class AWSSettings(CloudSettingsTest):  # type: ignore
        test: str = "Cool"
        prefix_test_store: str = ""

    return AWSSettings()


def return_base_settings() -> CloudBaseSettings:
    """Return a complete config class."""

    class Settings(CloudBaseSettings):
        """Test Settings class."""

        test: str
        extra_test: str = "test_setting"

        class Config:
            """Config class for test settings."""

            aws_secret_locations: List[AwsParameterStore] = []
            application_base_settings = CloudBaseSettings()
            aws_parameter_locations = [
                AwsParameterStore(
                    name="config",
                    output_prefix="prefix_test",
                )
            ]

            extra = "ignore"

            @classmethod
            def customise_sources(  # type: ignore
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
            ) -> Tuple[Any, ...]:
                """Define order of sources."""
                return (
                    init_settings,
                    env_settings,
                    file_secret_settings,
                    aws_parameter_settings,
                )

    return Settings()


def return_bad_config_class() -> CloudSettings:
    """Return a wrongly configured cloud config class."""
    CloudSettingsTest = CloudSettings(  # noqa: N806
        aws_parameter_locations=[
            AwsParameterStore(
                name="storesss",
                output_prefix="prefix_testsss",
            )
        ]
    )

    class AWSSettings(CloudSettingsTest):  # type: ignore
        test: str = "Cool"
        prefix_test_store: str = ""

    return AWSSettings()


def return_bad_parameter_config() -> CloudSettings:
    """Return a wrongly configured cloud config class."""
    CloudSettingsTest = CloudSettings(  # noqa: N806
        settings_order=[
            "init_settings",
            "aws_parameter_setting",
            "file_secret_settings",
            "env_settings",
        ]
    )  # noqa: N806

    class AWSSettings(CloudSettingsTest):  # type: ignore
        test: str = "Cool"
        prefix_test_store: str = ""

    return AWSSettings()
