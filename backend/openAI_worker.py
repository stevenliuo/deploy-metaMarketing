import logging
from openai import OpenAI, RateLimitError
from openai.types.chat.chat_completion import ChatCompletion
from retry import retry

from server.settings import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)


class OpenAIWorker:
    """ Class for working with OpenAI API"""

    def __init__(self):
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        self._model = OPENAI_MODEL

    @retry(RateLimitError, tries=10, delay=10, jitter=10)
    def _get_completion(self, model: str, messages: list[dict]) -> ChatCompletion:
        completion = self._client.chat.completions.create(model=model, messages=messages)

        return completion

    def get_answer_from_gpt(self, user_message: str, sys_message: str) -> str:
        logger.info(f"Asks GPT: {user_message}")

        messages = [
            {"role": "system", "content": sys_message},
            {"role": "user", "content": user_message},
        ]

        completion = self._get_completion(self._model, messages)

        answer = completion.choices[0].message.content

        logger.info(f"Got answer: {answer}")

        return answer
