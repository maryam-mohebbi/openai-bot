import unittest
from unittest.mock import MagicMock, patch, call
from mysql.connector import pooling
from adapters import mysql_adapter as mysql


class MySqlAdapterTest_sql_setup(unittest.TestCase):
    @patch('mysql.connector.pooling.MySQLConnectionPool')
    def test_should_verify_global_variable_is_correctly_set_based_on_input(self, mock_connection_pool):
        # prepare
        mock_connection_pool.return_value = MagicMock()

        # run
        result = mysql.sql_setup('test_host', 'test_port',
                                 'test_user', 'test_password', 'test_database')

        # assert
        mock_connection_pool.assert_called_with(pool_name="pynative_pool",
                                                pool_size=20,
                                                pool_reset_session=True,
                                                host='test_host',
                                                port='test_port',
                                                user='test_user',
                                                password='test_password',
                                                database='test_database')
        self.assertEqual(mysql.connection_pool,
                         mock_connection_pool.return_value)


class MySqlAdapterTest_insert_message(unittest.TestCase):
    @patch.object(mysql, 'connection_pool')
    def test_should_insert_message_correctly(self, mock_connection_pool):
        # prepare
        mock_connection_object = MagicMock()
        mock_cursor = MagicMock()
        mock_connection_pool.get_connection.return_value = mock_connection_object
        mock_connection_object.cursor.return_value = mock_cursor

        # run
        mysql.insert_message('chat_id', 'username', 'datetime',
                             'message_id', 'text', 'reply_message_id')

        # assert
        mock_connection_pool.get_connection.assert_called_once()
        mock_connection_object.cursor.assert_called_once()
        mock_cursor.execute.assert_called_with(
            'INSERT INTO MESSAGES (CHAT_ID, USERNAME, DATETIME, MESSAGE_ID, TEXT, REPLY_MESSAGE_ID) VALUES (%s, %s, %s, %s, %s, %s)',
            ('chat_id', 'username', 'datetime',
             'message_id', 'text', 'reply_message_id')
        )
        mock_connection_object.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection_object.close.assert_called_once()


class MySqlAdapterTest_does_user_exist(unittest.TestCase):
    @patch.object(mysql, 'connection_pool')
    def test_should_return_true_when_user_exists(self, mock_connection_pool):
        # prepare
        mock_connection_object = MagicMock()
        mock_cursor = MagicMock()
        mock_connection_pool.get_connection.return_value = mock_connection_object
        mock_connection_object.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('test_user',)

        # run
        result = mysql.does_user_exist('test_user')

        # assert
        self.assertTrue(result)
        mock_cursor.execute.assert_called_with(
            'SELECT USERNAME FROM USERS WHERE USERNAME = %s',
            ('test_user',)
        )
        mock_connection_pool.get_connection.assert_called_once()
        mock_connection_object.cursor.assert_called_once()

    @patch.object(mysql, 'connection_pool')
    def test_should_return_false_when_user_does_not_exist(self, mock_connection_pool):
        # prepare
        mock_connection_object = MagicMock()
        mock_cursor = MagicMock()
        mock_connection_pool.get_connection.return_value = mock_connection_object
        mock_connection_object.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        # run
        result = mysql.does_user_exist('test_user')

        # assert
        self.assertFalse(result)
        mock_cursor.execute.assert_called_with(
            'SELECT USERNAME FROM USERS WHERE USERNAME = %s',
            ('test_user',)
        )
        mock_connection_pool.get_connection.assert_called_once()
        mock_connection_object.cursor.assert_called_once()


class MySqlAdapterTest_update_message_tokens(unittest.TestCase):
    @patch.object(mysql, 'connection_pool')
    def test_should_update_message_tokens_correctly(self, mock_connection_pool):
        # prepare
        mock_connection_object = MagicMock()
        mock_cursor = MagicMock()
        mock_connection_pool.get_connection.return_value = mock_connection_object
        mock_connection_object.cursor.return_value = mock_cursor
        # run
        mysql.update_message_tokens(
            'message_id', 'completion_tokens', 'prompt_tokens')

        # assert
        mock_connection_pool.get_connection.assert_called_once()
        mock_connection_object.cursor.assert_called_once()
        mock_cursor.execute.assert_called_with(
            'UPDATE MESSAGES SET COMPLETION_TOKENS=%s, PROMPT_TOKENS=%s WHERE MESSAGE_ID = %s',
            ('completion_tokens', 'prompt_tokens', 'message_id')
        )
        mock_connection_pool.get_connection.assert_called_once()
        mock_connection_object.cursor.assert_called_once()


class MySqlAdapterTest_token_count(unittest.TestCase):
    @patch.object(mysql, 'connection_pool')
    def test_tokens_count(self, mock_connection_pool):
        # Mock the cursor and its methods
        mock_connection_object = MagicMock()
        mock_cursor = MagicMock()
        mock_connection_pool.get_connection.return_value = mock_connection_object
        mock_connection_object.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [
            (0,),  # user_count
            (10, 20),  # result_token
            (50,),  # result_limitation
        ]

        # Test case when user_count == 0
        result = mysql.tokens_count('testuser')
        self.assertTrue(result)

        # Test case when total tokens < token limitation
        mock_cursor.fetchone.side_effect = [
            (1,),  # user_count
            (10, 20),  # result_token
            (50,),  # result_limitation
        ]
        result = mysql.tokens_count('testuser')
        self.assertTrue(result)

        # Test case when total tokens >= token limitation
        mock_cursor.fetchone.side_effect = [
            (1,),  # user_count
            (25, 30),  # result_token
            (50,),  # result_limitation
        ]
        result = mysql.tokens_count('testuser')
        self.assertFalse(result)
