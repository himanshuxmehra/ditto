from abc import ABC, abstractmethod

class BaseAssistant(ABC):
    def __init__(self, user_info):
        self.user_info = user_info

    @abstractmethod
    def process_input(self, user_input):
        pass