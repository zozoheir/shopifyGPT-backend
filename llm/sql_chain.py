from langchain import OpenAI, SQLDatabase, SQLDatabaseChain, PromptTemplate
from scraping.database import Database


heroku_db = Database(database_name='',
                     endpoint='',
                     username='',
                     password='',
                     port='',
                     type='')

db = SQLDatabase(engine=heroku_db.engine)
llm = OpenAI(temperature=0)

_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database.

Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

When you use JOIN, use the following syntax for all columns: SELECT table_name.columns_name FROM ...

Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the tables listed below.

{table_info}

Question: {input}"""

SQL_CHAIN_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect", "top_k"],
    template=_DEFAULT_TEMPLATE,
)

db_chain = SQLDatabaseChain(llm=llm,
                            database=db,
                            verbose=True,
                            prompt=SQL_CHAIN_PROMPT)

