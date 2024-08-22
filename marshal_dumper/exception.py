# пусть буит
class VersionError(Exception):
    def __init__(self, expected_version: str, parsed_version: str) -> None:
        super().__init__(f"Expected version - {expected_version}, got - {parsed_version}")


class TypeNotSupportedError(Exception):
    def __init__(self, passed_type: str | type):
        super().__init__(f"{passed_type} type is not supported in current version")
        