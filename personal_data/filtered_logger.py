#!/usr/bin/env python3
"""
function called filter_datum that returns the log message obfuscated
"""

import mysql.connector
import logging
import re
from typing import List
from os import getenv

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        returns the log message obfuscated from the record
        """
        filter_message = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        record.msg = filter_message
        return super().format(record)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Arguments:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating
        all fields in the log line (message)
    """
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    """
    get_logger: function that takes no arguments and
        returns a logging.Logger object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formater = RedactingFormatter(PII_FIELDS)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formater)

    logger.addHandler(streamHandler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    get_db: function that returns a connector to the database
        (mysql.connector.connection.MySQLConnection object).
    """
    connection_db = mysql.connector.connection.MySQLConnection(
        user=getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=getenv("PERSONAL_DATA_DB_PASSWORD", "root"),
        host=getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=getenv("PERSONAL_DATA_DB_NAME",)
    )

    return connection_db


def main():
    database = get_db()
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users")
    fields = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        string_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        logger.info(string_row.strip())

    cursor.close()
    database.close()


if __name__ == "__main__":
    main()
