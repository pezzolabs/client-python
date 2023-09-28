import requests
from typing import Union, Dict, Any
from .classes import Prompt
from pezzo.config import pezzo_config

class Pezzo:
    def __init__(self):
        self.options = pezzo_config
        
    def get_prompt(self, prompt_name: str) -> Dict[str, Prompt]:
        url = f"{self.options.server_url}/api/prompts/v2/deployment"
        params = {
            "name": prompt_name,
            "environmentName": self.options.environment,
            "projectId": self.options.project_id
        }
        headers = {
            "Content-Type": "application/json",
            "x-pezzo-api-key": self.options.api_key,
            "x-pezzo-project-id": self.options.project_id
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if not response.ok:
            raise Exception(data.get("message", f"Error fetching prompt {prompt_name} for environment {self.options.environment} ({data.get('statusCode')})."))

        pezzoPrompt = Prompt(
            metadata={
                "promptId": data.get("promptId"),
                "promptVersionSha": data.get("promptVersionSha"),
                "type": data.get("type"),
            },
            settings=data.get("settings"),
            content=data.get("content")
        )
        return pezzoPrompt

    def report_prompt_execution(self, dto: Dict[str, Any]):
        url = f"{self.options.server_url}/api/reporting/v2/request"
        headers = {
            "Content-Type": "application/json",
            "x-pezzo-api-key": self.options.api_key,
            "x-pezzo-project-id": self.options.project_id
        }

        response = requests.post(url, headers=headers, json=dto)
        if not response.ok:
            print(f"Could not report prompt execution: {response.json()}")

    def fetch_cached_request(self, request: Dict[str, Any]) -> Union[Dict[str, Any], None]:
        url = f"{self.options.server_url}/api/cache/v1/request/retrieve"
        headers = {
            "Content-Type": "application/json",
            "x-pezzo-api-key": self.options.api_key,
            "x-pezzo-project-id": self.options.project_id
        }
        response = requests.post(url, headers=headers, json={"request": request})
        if not response.ok:
            print(f"Could not fetch request from cache: {response.json()}")
            return None

        return response.json()

    def cache_request(self, request: Dict[str, Any], _response: Dict[str, Any]):
        url = f"{self.options.server_url}/api/cache/v1/request/save"
        headers = {
            "Content-Type": "application/json",
            "x-pezzo-api-key": self.options.api_key,
            "x-pezzo-project-id": self.options.project_id
        }
        response = requests.post(url, headers=headers, json={"request": request, "response": _response})
        if not response.ok:
            print(f"Could not cache request: {response.json()}")

pezzo = Pezzo()