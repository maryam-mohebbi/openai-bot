import unittest
from unittest.mock import MagicMock, patch
from adapters import openai_adapter as ai


class OpenaiAdapterTest_setup(unittest.TestCase):
    def test_should_verify_global_variable_is_correctly_set_based_on_input(self):
        # prepare

        # run
        ai.setup('test_api_key')

        # assert
        self.assertEqual(
            ai.OPENAI_API_KEY, 'test_api_key')


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
        result = ai.generate_response('test_prompt', [])

        # assert
        self.assertEqual(result, {'content': 'test_content', 'tokens': {
                         'completion_tokens': 100, 'prompt_tokens': 50}})
        mock_create.assert_called_with(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': 'I need your help. I want to ask from you. Your answer should be simple but complete'},
                {'role': 'assistant', 'content': 'Sure, I will help you in my best'},
                {'role': 'user', 'content': 'test_prompt'}
            ],
            max_tokens=1024,
            n=1,
            temperature=1,
        )
