import unittest
from unittest.mock import MagicMock, patch
import src.adapters.openai_adapter
from src.adapters.openai_adapter import setup, generate_response


class OpenaiAdapterTest_setup(unittest.TestCase):
    def test_should_verify_global_variable_is_correctly_set_based_on_input(self):
        # prepare

        # run
        setup('test_api_key')

        # assert
        self.assertEqual(
            src.adapters.openai_adapter.OPENAI_API_KEY, 'test_api_key')


class OpenaiAdapterTest_generate_response(unittest.TestCase):
    @patch('openai.ChatCompletion.create')
    def test_should_generate_response_correctly(self, mock_create):
        # prepare
        mock_create.return_value = MagicMock(
            choices=[
                MagicMock(message=MagicMock(content='test_content'))
            ],
            usage=MagicMock(completion_tokens=100, prompt_tokens=50)
        )

        # run
        result = generate_response('test_prompt')

        # assert
        self.assertEqual(result, {'content': 'test_content', 'tokens': {
                         'completion_tokens': 100, 'prompt_tokens': 50}})
        mock_create.assert_called_with(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': 'test_prompt'}],
            max_tokens=1024,
            n=1,
            temperature=1,
        )
