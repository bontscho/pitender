from peewee import SqliteDatabase

db = SqliteDatabase('pitender.db', pragmas={'foreign_keys': 1})