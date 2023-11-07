"""Test Parameters."""

from collections import namedtuple

import factory  # type: ignore


Parameter = namedtuple("Parameter", ["name", "description", "type", "value"])

application_environments = ["dev", "dev2", "dev3"]
application_names = ["cloud-app", "another-app"]
value_types = ["String", "SecureString"]




class ParameterFactory(factory.Factory):    # type: ignore
    """Factory creating parameters."""

    class Meta:
        """Extra information for creation of parameters."""

        model = Parameter
        exclude = (
            "environment_name",
            "application_name",
            "application_setting",
            "test_value",
            "faker",
        )

    environment_name = factory.Faker("word", ext_word_list=application_environments)
    application_name = factory.Faker("word", ext_word_list=application_names)
    application_setting = factory.Faker("word")
    name = factory.LazyAttribute(
        lambda n: f"/environments/{n.environment_name}/{n.application_name}/{n.application_setting}"
    )
    description = factory.Faker("text", max_nb_chars=60)
    type = factory.Faker("word", ext_word_list=value_types)
    value = factory.Faker("pystr")
