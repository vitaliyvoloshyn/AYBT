from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel


class AbstractRepository(ABC):
    @abstractmethod
    def add_obj(self, *args, **kwargs) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def get_obj(self, *args, **kwargs) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, *args, **kwargs) -> List[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError
