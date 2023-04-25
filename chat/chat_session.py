from datetime import datetime, timedelta

from llm.agent import agent_executor


# Define ChatSession class
class ChatSession:
    def __init__(self,
                 session_id,
                 ):
        self.session_id = session_id
        self.start_time = datetime.now()
        self.last_activity_time = datetime.now()
        self.history_list = []

    def is_active(self):
        return (datetime.now() - self.last_activity_time) < timedelta(minutes=30)

    def query(self, question):
        answer = agent_executor(input=question)
        self.history_list.append((question, answer))
        return answer
