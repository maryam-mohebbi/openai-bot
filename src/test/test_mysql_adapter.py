import unittest
from unittest.mock import MagicMock, patch, call
import src.adapters.mysql_adapter
from src.adapters.mysql_adapter import sql_setup, insert_message, does_user_exist, update_message_tokens


class MySqlAdapterTest_sql_setup(unittest.TestCase):
    @patch('mysql.connector.connect')
    def test_should_verify_global_variable_is_correctly_set_based_on_input(self, mock_connect):
        # prepare
        mock_connect.return_value = MagicMock()

        # run
        result = sql_setup('test_host', 'test_port',
                           'test_user', 'test_password', 'test_database')

        # assert
        mock_connect.assert_called_with(
            host='test_host',
            port='test_port',
            user='test_user',
            password='test_password',
            database='test_database'
        )
        self.assertEqual(src.adapters.mysql_adapter.cnx,
                         mock_connect.return_value)


class MySqlAdapterTest_insert_message(unittest.TestCase):
    @patch.object(src.adapters.mysql_adapter, 'cnx')
    def test_should_insert_message_correctly(self, mock_cnx):
        # prepare
        mock_cursor = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        # run
        insert_message('chat_id', 'username', 'datetime',
                       'message_id', 'text', 'reply_message_id')

        # assert
        mock_cnx.cursor.assert_called_once()
        mock_cursor.execute.assert_called_with(
            'INSERT INTO MESSAGES (CHAT_ID, USERNAME, DATETIME, MESSAGE_ID, TEXT, REPLY_MESSAGE_ID) VALUES (%s, %s, %s, %s, %s, %s)',
            ('chat_id', 'username', 'datetime',
             'message_id', 'text', 'reply_message_id')
        )
        mock_cnx.commit.assert_called_once()


class MySqlAdapterTest_does_user_exist(unittest.TestCase):
    @patch.object(src.adapters.mysql_adapter, 'cnx')
    def test_should_return_true_when_user_exists(self, mock_cnx):
        # prepare
        mock_cursor = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('test_user',)

        # run
        result = does_user_exist('test_user')

        # assert
        self.assertTrue(result)
        mock_cursor.execute.assert_called_with(
            'SELECT USERNAME FROM USERS WHERE USERNAME = %s',
            ('test_user',)
        )
        mock_cnx.commit.assert_called_once()

    @patch.object(src.adapters.mysql_adapter, 'cnx')
    def test_should_return_false_when_user_does_not_exist(self, mock_cnx):
        # prepare
        mock_cursor = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        # run
        result = does_user_exist('test_user')

        # assert
        self.assertFalse(result)
        mock_cursor.execute.assert_called_with(
            'SELECT USERNAME FROM USERS WHERE USERNAME = %s',
            ('test_user',)
        )
        mock_cnx.commit.assert_called_once()


class MySqlAdapterTest_update_message_tokens(unittest.TestCase):
    @patch.object(src.adapters.mysql_adapter, 'cnx')
    def test_should_update_message_tokens_correctly(self, mock_cnx):
        # prepare
        mock_cursor = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        # run
        update_message_tokens(
            'message_id', 'completion_tokens', 'prompt_tokens')

        # assert
        mock_cnx.cursor.assert_called_once()
        mock_cursor.execute.assert_called_with(
            'UPDATE MESSAGES SET COMPLETION_TOKENS=%s, PROMPT_TOKENS=%s WHERE MESSAGE_ID = %s',
            ('completion_tokens', 'prompt_tokens', 'message_id')
        )
        mock_cnx.commit.assert_called_once()
