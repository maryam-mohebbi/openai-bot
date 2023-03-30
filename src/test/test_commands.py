import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch
from services import commands as cmd


class TestCommands(IsolatedAsyncioTestCase):

    @patch('services.commands.bot.reply_text')
    async def test_start(self, mock_reply_text):
        mock_update = MagicMock()
        mock_context = MagicMock()

        await cmd.start(mock_update, mock_context)
        mock_reply_text.assert_called_once()

    @patch('services.commands.bot.reply_text')
    async def test_help(self, mock_reply_text):
        mock_update = MagicMock()
        mock_context = MagicMock()

        await cmd.help(mock_update, mock_context)
        mock_reply_text.assert_called_once()

    @patch('services.commands.bot.reply_text')
    async def test_chat(self, mock_reply_text):
        mock_update = MagicMock()
        mock_context = MagicMock()

        await cmd.chat(mock_update, mock_context)
        mock_reply_text.assert_called_once()

    @patch('services.commands.bot.reply_text')
    @patch('services.commands.mysql')
    @patch('services.commands.openai')
    async def test_handle_text(self, mock_openai, mock_mysql, mock_reply_text):
        # Set up mocks
        mock_update = MagicMock()
        mock_context = MagicMock()
        mock_update.message.chat.username = 'testuser'
        mock_openai.generate_response.return_value = {
            'tokens': {'completion_tokens': 10, 'prompt_tokens': 5},
            'content': 'test response',
        }

        # Test case when user does not exist
        mock_mysql.does_user_exist.return_value = False
        await cmd.handle_text(mock_update, mock_context)
        mock_reply_text.assert_called_with(
            mock_update, 'Oh, Sorry! You do not have access')

        # Test case when tokens count is False
        mock_mysql.does_user_exist.return_value = True
        mock_mysql.tokens_count.return_value = False
        await cmd.handle_text(mock_update, mock_context)
        mock_reply_text.assert_called_with(
            mock_update, 'Sorry, The sum of tokens has exceeded 1000.')

        # Test case when everything works as expected
        mock_mysql.tokens_count.return_value = True
        await cmd.handle_text(mock_update, mock_context)
        mock_reply_text.assert_called_with(
            mock_update, 'test response', mock_update.message.message_id)

        # Test case when an exception is raised
        mock_openai.generate_response.side_effect = Exception('test exception')
        await cmd.handle_text(mock_update, mock_context)
        mock_reply_text.assert_called_with(
            mock_update, 'Error encountered while chatting.')
