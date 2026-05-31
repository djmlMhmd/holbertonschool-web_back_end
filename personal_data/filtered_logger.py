#!/usr/bin/env python3
"""
Module providing utilities to obfuscate PII fields in log messages
and securely retrieve user data from a MySQL database.
"""

import mysql.connector
import logging
import re
from typing import List
from os import getenv

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """Formatter that redacts sensitive PII fields from log records."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with the list of fields to redact."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record, obfuscating all configured PII fields."""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Return the log message with the given fields replaced by redaction."""
    pattern = r'({})=[^{}]*'.format('|'.join(fields), re.escape(separator))
    return re.sub(pattern, r'\1=' + redaction, message)


def get_logger() -> logging.Logger:
    """Create and return a logger named 'user_data' with PII redaction."""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Return a MySQL connection built from environment variables."""
    return mysql.connector.connection.MySQLConnection(
        user=getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=getenv("PERSONAL_DATA_DB_NAME")
    )


def main():
    """Fetch all users from the database and log each row with PII redacted."""
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
