from unittest import TestCase
from unittest.mock import patch, MagicMock
from telegram.ext import CommandHandler, MessageHandler, filters
from src.adapters.telegram_adapter import (
    setup,
    add_command_handler,
    add_message_handler,
    reply_text,
    start,
)


class TelegramAdapterTest_setup(TestCase):
    @patch('src.adapters.telegram_adapter.ApplicationBuilder')
    def test_should_create_application_builder_correctly(self, mock_application_builder):
        mock_application_builder.return_value.build.return_value = MagicMock()

        result = setup('test_token')

        mock_application_builder.assert_called_with()
        self.assertIsInstance(result, MagicMock)


class TelegramAdapterTest_add_command_handler(TestCase):
    @patch('src.adapters.telegram_adapter.CommandHandler')
    def test_should_add_command_handler_correctly(self, mock_command_handler):
        mock_builder = MagicMock()
        mock_fn = MagicMock()

        add_command_handler(mock_builder, 'test_command', mock_fn)

        mock_command_handler.assert_called_with('test_command', mock_fn)
        mock_builder.add_handler.assert_called_with(
            mock_command_handler.return_value)


class TelegramAdapterTest_add_message_handler(TestCase):
    @patch('src.adapters.telegram_adapter.MessageHandler')
    def test_should_add_message_handler_correctly(self, mock_message_handler):
        mock_builder = MagicMock()
        mock_fn = MagicMock()

        add_message_handler(mock_builder, mock_fn)

        mock_builder.add_handler.assert_called_with(
            mock_message_handler.return_value)


class TelegramAdapterTest_reply_text(TestCase):
    async def test_should_reply_text_correctly(self):
        mock_update = MagicMock()
        mock_message = MagicMock()
        mock_update.message = mock_message

        await reply_text(mock_update, 'test_text', 'test_message_id')

        mock_message.reply_text.assert_called_with(
            text='test_text', reply_to_message_id='test_message_id')


class TelegramAdapterTest_start(TestCase):
    def test_should_start_application_builder(self):
        mock_builder = MagicMock()

        start(mock_builder)

        mock_builder.run_polling.assert_called_once()
