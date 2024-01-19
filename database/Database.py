from datetime import datetime


class Database:
    current_session_id = 0

    def __init__(self):
        self.__sessions: list[SessionModel] = []

    def create_session(self):
        self.current_session_id += 1
        session = SessionModel()
        self.__sessions.append(session)
        return session

    def get_last_session(self):
        return self.__sessions[-1]


class SessionModel:

    def __init__(self):
        self.__name = datetime.now().strftime("%d/%m/%Y %hh:%mm %p")
        self.__messages = []
        self.__id = Database.current_session_id

    def add_message(self, message):
        self.__messages.append(message)

    def get_messages(self):
        return self.__messages
