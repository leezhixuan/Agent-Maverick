class User:

    def __init__(self, chat_id:str, first_name:str, last_name:str) -> None:
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name

    def getInfo(self)->list:
        info = [self.chat_id, self.first_name, self.last_name]
        return info