from typing import Optional
import os

class PezzoConfig:
    _api_key: Optional[str]
    _project_id: Optional[str]
    _environment: Optional[str]
    _server_url: Optional[str]

    def __init__(self,
                 api_key: Optional[str] = None,
                 project_id: Optional[str] = None,
                 environment: Optional[str] = None,
                 server_url: Optional[str] = None
                 ):
        self._api_key = api_key
        self._project_id = project_id
        self._environment = environment
        self._server_url = server_url

    @property
    def api_key(self) -> Optional[str]:
        if (self._api_key is None):
            return os.environ.get("PEZZO_API_KEY")

        return self._api_key

    @api_key.setter
    def api_key(self, value: Optional[str]):
        self._api_key = value

    @property
    def project_id(self) -> Optional[str]:
        if (self._project_id is None):
            return os.environ.get("PEZZO_PROJECT_ID")

        return self._project_id

    @project_id.setter
    def project_id(self, value: Optional[str]):
        self._project_id = value

    @property
    def environment(self) -> Optional[str]:
        if (self._environment is None):
            return os.environ.get("PEZZO_ENVIRONMENT", "Production")
        return self._environment

    @environment.setter
    def environment(self, value: Optional[str]):
        self._environment = value

    @property
    def server_url(self) -> Optional[str]:
        if (self._server_url is None):
            return os.environ.get("PEZZO_SERVER_URL", "https://api.pezzo.ai")
        return self._server_url

    @server_url.setter
    def server_url(self, value: Optional[str]):
        self._server_url = value



pezzo_config = PezzoConfig()