import asyncpg
from typing import ByteString


class Database:
    def __init__(self, url):
        """
        Initialize the database

        :param str url: Database URL
        """
        self.url = url
        self._cursor = None
        self._connection_pool = None
        self.con = None

    async def connect(self):
        """
        Create a connection to the database
        """
        if not self._connection_pool:
            try:
                self._connection_pool = await asyncpg.create_pool(
                    min_size=1,
                    max_size=20,
                    command_timeout=60,
                    dsn=self.url,
                )
                print("Database pool connection opened")
            except Exception as e:
                print(e)

    async def fetch(self, query):
        """
        SQL query execution

        :param str query: SQL query string
        :return: Query result
        :rtype: ByteString
        """
        if not self._connection_pool:
            await self.connect()
        else:
            con = await self._connection_pool.acquire()
            try:
                result = await con.fetchval(query)
                return result
            except Exception as e:
                print(e)
            finally:
                await self._connection_pool.release(con)

    async def close(self):
        """
        Close a connection to the database

        """
        if not self._connection_pool:
            try:
                await self._connection_pool.close()
                print("Database pool connection closed")
            except Exception as e:
                print(e)
