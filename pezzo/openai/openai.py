import os
import openai
from pezzo.client import pezzo
from pezzo.utils.interpolate_variables import interpolate_variables_recursively
from pezzo.utils.helpers import merge, get_client_version, get_timestamp

class PezzoOpenAI:
    def __init__(self):
        openai.api_key = os.environ.get('OPENAI_API_KEY')

        if not openai.api_key:
            raise Exception('OPENAI_API_KEY is not set')

        self.openai = openai
        self.ChatCompletion = ChatCompletion(pezzo, self.openai)

class ChatCompletion:
    def __init__(self, pezzo, openai):
        self.pezzo = pezzo
        self.openai = openai

    def create(self, **args):
        pezzo_prompt = args.get('pezzo_prompt', None)
        pezzo_options = args.get('pezzo_options', None)
        native_options = {**args}
        native_options.pop('pezzo_prompt', None)
        native_options.pop('pezzo_options', None)

        managed_messages = []

        if pezzo_prompt:
            if pezzo_prompt.content.get('prompt'):
                managed_messages = [{'role': 'user', 'content': pezzo_prompt.content['prompt']}]
            if pezzo_prompt.content.get('messages'):
                managed_messages = pezzo_prompt.content['messages']

        request_body = {
            'messages': managed_messages,
            **native_options,
            **(pezzo_prompt.settings if pezzo_prompt else {}),
        }

        if pezzo_options and pezzo_options.get('variables'):
            messages = interpolate_variables_recursively(request_body['messages'], pezzo_options['variables'])
            request_body['messages'] = messages

        response, error, report_payload = None, None, None

        base_metadata = {
            'environment': self.pezzo.options.environment,
            'provider': 'OpenAI',
            'type': 'ChatCompletion',
            'client': 'pezzo-python',
            'clientVersion': get_client_version(),
        }

        request_timestamp = get_timestamp()
        merged_metadata = merge(base_metadata, pezzo_prompt.metadata if pezzo_prompt and pezzo_prompt.metadata else merge(base_metadata))

        base_report = {
            'metadata': merged_metadata,
            'cacheEnabled': False,
            'cacheHit': None,
            'request': {
                'timestamp': request_timestamp,
                'body': request_body
            }
        }

        if (pezzo_options and pezzo_options.get('properties')):
            base_report['properties'] = pezzo_options['properties']

        if pezzo_options and pezzo_options.get('cache'):
            base_report['cacheEnabled'] = True
            cached_request = self.pezzo.fetch_cached_request(request_body)

            base_report['cacheHit'] = cached_request['hit'];

            if cached_request['hit']:
                base_report['cacheHit'] = True
                response = {
                    **cached_request['data'],
                    'usage': {
                        'prompt_tokens': 0,
                        'completion_tokens': 0,
                        'total_tokens': 0,
                    }
                }
                report_payload = {
                    **base_report,
                    'response': {
                        'timestamp': request_timestamp,
                        'body': response,
                        'status': 200,
                    }
                }

        if not (pezzo_options and pezzo_options.get('cache') and base_report['cacheHit']):
            try:
                response = self.openai.ChatCompletion.create(**request_body)
                report_payload = {
                    **base_report,
                    'response': {
                        'timestamp': get_timestamp(),
                        'body': response,
                        'status': 200,
                    }
                }
            except Exception as err:
                error = err
                report_payload = {
                    **base_report,
                    'response': {
                        'timestamp': get_timestamp(),
                        'body': err.json_body,
                        'status': err.http_status,
                    }
                }

        should_write_to_cache = pezzo_options and pezzo_options.get('cache') and report_payload and report_payload['cacheHit'] == False and report_payload['response']['status'] == 200
        
        self.pezzo.report_prompt_execution(report_payload)

        if should_write_to_cache and error == None:
            self.pezzo.cache_request(request_body, response)

        if error:
            raise error

        return response

pezzo_open_ai = PezzoOpenAI()