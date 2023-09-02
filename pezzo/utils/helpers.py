import os
from datetime import datetime, timezone
from typing import Any, Dict, List, TypeVar, Tuple

TArgs = TypeVar('TArgs', bound=Tuple)  # Simulating 'TArgs extends unknown[]'

# Instead of interfaces, Python uses type hinting with dictionaries.
PezzoInjectedContext = Dict[str, Any]
PezzoExtendedArgs = TypeVar('PezzoExtendedArgs', bound=Tuple)  # Simulating 'PezzoExtendedArgs<TArgs>'

class ExtractedPezzoFromArgsResult:
    def __init__(self, pezzo: PezzoInjectedContext, original_args: TArgs):
        self.pezzo = pezzo
        self.original_args = original_args

def extract_pezzo_from_args(args: PezzoExtendedArgs) -> ExtractedPezzoFromArgsResult:
    pezzo = args[0].get('pezzo', {})
    original_args_0 = {k: v for k, v in args[0].items() if k != 'pezzo'}
    original_args = (original_args_0, *args[1:])

    return ExtractedPezzoFromArgsResult(pezzo, original_args)

T = TypeVar('T', bound=Dict[str, Any])

def merge(*args: T) -> T:
    result = {}
    for arg in args:
        result.update(arg)
    return result

def get_client_version() -> str:
    current_path = os.path.dirname(os.path.realpath(__file__))
    version_path = os.path.join(current_path, "../version.txt")
    with open(version_path, "r") as f:
        return f.read().strip()
    
def get_timestamp() -> str:
    timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    return timestamp