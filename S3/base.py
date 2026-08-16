from abc import ABC, abstractmethod
from io import BytesIO


class Storage(ABC):
    @abstractmethod
    def upload(self, filename:str, file_data:BytesIO, lenght:int, content_type:str) ->str:
        pass


    @abstractmethod
    def delete(
        self,
        url:str
    ):
        pass


    