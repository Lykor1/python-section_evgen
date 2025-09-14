import enum
from dataclasses import dataclass
from typing import Dict, Any


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: Dict[str, Any]


@dataclass
class ParsedMessage:
    user: str
    text: str
    timestamp: str


class BaseParser:
    def parse(self, message: JsonMessage) -> ParsedMessage:
        raise NotImplementedError


class TelegramParser(BaseParser):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        return ParsedMessage(
            user=message.payload.get('user', 'unknown'),
            text=message.payload.get('text', ''),
            timestamp=message.payload.get('date', ''),
        )


class SlackParser(BaseParser):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        return ParsedMessage(
            user=message.payload.get('user', 'unknown'),
            text=message.payload.get('text', ''),
            timestamp=message.payload.get('date', ''),
        )


class MattermostParser(BaseParser):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        return ParsedMessage(
            user=message.payload.get('user', 'unknown'),
            text=message.payload.get('text', ''),
            timestamp=message.payload.get('date', ''),
        )


class ParserFactory:
    _parser = {
        MessageType.TELEGRAM: TelegramParser(),
        MessageType.MATTERMOST: MattermostParser(),
        MessageType.SLACK: SlackParser(),
    }

    @classmethod
    def get_parser(cls, message_type: MessageType) -> BaseParser:
        parser = cls._parser.get(message_type)
        if not parser:
            raise ValueError(f'Нет типа парсера {message_type}.')
        return parser


if __name__ == '__main__':
    raw_message = JsonMessage(
        message_type=MessageType.TELEGRAM,
        payload={'user': 'Evgen', 'text': 'Hello World', 'date': '2025-09-14'}
    )
    parser = ParserFactory.get_parser(raw_message.message_type)
    parsed = parser.parse(raw_message)
    print(parsed)
