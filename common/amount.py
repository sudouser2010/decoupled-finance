import copy
from dataclasses import dataclass


@dataclass
class Amount:
    amount: int
    address: str

    def as_dict(self) -> dict:
        """
        Returns this object but as a dictionary
        :return:
        """
        return copy.deepcopy(self.__dict__)
