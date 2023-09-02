from dataclasses import dataclass
from typing import Any, Optional, Union, List, Literal

@dataclass
class PromptMetadata:
    promptId: str
    promptVersionSha: str
    type: Literal['Prompt', 'Chat']
    isTestPrompt: Optional[bool] = None

@dataclass
class ChatPromptContentMessage:
    role: Literal['user', 'assistant']
    content: str

@dataclass
class PromptChatContent:
    messages: List["ChatPromptContentMessage"]

@dataclass
class PromptBasicContent:
    prompt: str

@dataclass
class Prompt:
    metadata: PromptMetadata
    settings: Any
    content: Union["PromptBasicContent", "PromptChatContent"]