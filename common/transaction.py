import copy
from dataclasses import dataclass

from specific_import import import_file

TransactionType = import_file('enums.py').TransactionType


@dataclass
class Transaction:
    transaction_type: TransactionType
    to_address: str
    from_address: str
    signature: str
    amount: int

    def as_dict(self):
        return copy.deepcopy(self.__dict__)
