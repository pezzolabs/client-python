import re
from typing import Any, Dict, Union, List

def interpolate_variables(text: str, variables: Dict[str, Union[bool, int, str]]) -> str:
    def replace_match(match):
        key = match.group(1).strip()
        return str(variables.get(key, match.group(0)))

    return re.sub(r"{\s*(\w+)\s*}", replace_match, text)

def interpolate_variables_recursively(obj: Dict[str, Any], variables: Dict[str, Union[bool, int, str]]) -> Dict[str, Any]:
    def process_value(value: Any) -> Any:
        if isinstance(value, str):
            return interpolate_variables(value, variables)
        elif isinstance(value, list):
            return [process_value(v) for v in value]
        elif isinstance(value, dict):
            return process_obj(value)
        else:
            return value

    def process_obj(object: Dict[str, Any]) -> Dict[str, Any]:
        return {key: process_value(value) for key, value in object.items()}

    return process_value(obj)
