#!/usr/bin/env python3
"""Regex-ing module to obfuscate log messages"""

from typing import List
import json
import logging
import mysql.connector
import os
import re


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """A function used to obfuscate the log message"""
    for field in fields:
        message = re.sub(fr'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}',
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """The constructor method of the class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """The formatter method of the class"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """A function that creates a logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """A function that connects to a secure database"""
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", default="root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", default="")
    host = os.getenv("PERSONAL_DATA_DB_HOST", default="localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connection.MySQLConnection(user=user,
                                                      password=password,
                                                      host=host,
                                                      database=database)


def main():
    """Main function used to read and filter data"""
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor:
        filtered_row = filter_datum(PII_FIELDS,'***', str(row), ';')
        logger.info(filtered_row)
    
    cursor.close()
    db.close()

if __name__ == '__main__':
    main()
