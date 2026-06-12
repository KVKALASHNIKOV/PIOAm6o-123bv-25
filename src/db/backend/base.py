from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple


class BaseDB(ABC):

    @abstractmethod
    def add_record(self, data: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    def get_all_records(self) -> List[Tuple[int, Dict[str, Any]]]:
        pass

    @abstractmethod
    def get_record(self, record_id: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def filter_records(
        self,
        filters: Dict[str, Any]
    ) -> List[Tuple[int, Dict[str, Any]]]:
        pass

    @abstractmethod
    def update_record(
        self,
        record_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete_record(self, record_id: int) -> Dict[str, Any]:
        pass
