import numpy as np
import pandas as pd
import datetime as dt

from sqlalchemy import create_engine, text
from sqlalchemy.dialects.mysql import insert as insert_mysql
from sqlalchemy import table, column
from psycopg2.extras import execute_values

from helpers import getLogger

logger = getLogger(__name__)


class Database:

    def __init__(self,
                 database_name,
                 endpoint,
                 username,
                 password,
                 port,
                 type
                 ):
        self.database_name = database_name
        self.database_type = type

        if type == 'mysql':
            self.connection_string = 'mysql+pymysql://' + username + ':' + password + '@' + endpoint + ':' + str(
                port) + '/' + database_name
        elif type == 'postgres':
            self.connection_string = 'postgresql+psycopg2://' + username + ':' + password + '@' + endpoint + ':' + str(
                port) + '/' + database_name

        self.engine = create_engine(self.connection_string)

    def open(self):
        # Test connection
        try:
            self.engine = create_engine(self.connection_string)
            result = pd.read_sql("SELECT * FROM INFORMATION_SCHEMA.TABLES", self.engine)
        except Exception as e:
            logger.info("Can't open DB")
            raise e

    def close(self):
        self.engine.dispose()

    def query(self, query):
        """
        Exceptions are handled on a case by case basis in the code calling this function.
        :param query:
        :return:
        """
        try:
            return pd.read_sql(query, self.engine).replace('NULL', np.nan)
        except Exception as e:
            self.close()
            raise e

    def getTableNames(self):
        return self.query("SELECT * FROM information_schema.tables WHERE table_schema = '" + self.database_name + "'")[
            'TABLE_NAME'].values

    def upsert(self,
               df,
               table_name,
               primary_key=None,
               including_insert_timestamp=True,
               **kwargs):

        if type(primary_key) == str:
            primary_key = [primary_key]
        if including_insert_timestamp is True:
            df['insert_timestamp'] = dt.datetime.now(dt.timezone.utc)


        if self.database_type == 'mysql':
            data_iter = [tuple(val.values()) for i, val in enumerate(df.to_dict('records'))]
            columns = [column(c) for c in df.columns]
            mytable = table(table_name, *columns)
            insert_stmt = insert_mysql(mytable).values(data_iter)
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(insert_stmt.inserted)
            return self.engine.execute(on_duplicate_key_stmt)

        elif self.database_type == 'postgres':

            with self.engine.connect() as connection:
                raw_connection = connection.connection
                cursor = raw_connection.cursor()
                insert_stmt = (
                    f"INSERT INTO {table_name} ({','.join(df.columns)}) VALUES %s ON CONFLICT ({','.join(primary_key)}) DO UPDATE SET {','.join([f'{col}=excluded.{col}' for col in df.columns if col not in primary_key])}"
                )
                data = [tuple(row) for row in df.itertuples(index=False)]
                execute_values(cursor, insert_stmt, data)
                raw_connection.commit()

        logger.info(f"Upserted {len(df)} rows into {table_name}")


    def insert(self, df, table_name, **kwargs):
        """
        Exceptions are handled on a case by case basis in the code calling this function.
        :param query:
        :return:
        """
        try:
            df.to_sql(name=table_name,
                      con=self.engine,
                      index=False,
                      chunksize=5000,
                      method='multi',
                      **kwargs)
            self.close()
        except Exception as e:
            self.close()
            raise e
