from dataclasses import dataclass, field
from enum import Enum
from typing import List

from symbol_table.scope.scope import Scope


class TokenSuperType(Enum):
    DELIMITER = "delimitador"
    RESERVED_WORD = "palavra reservada"
    PUNCTUATION = "pontuação"
    OPERATION = "operação"
    NON_TRIVIAL = "não-trivial"


@dataclass
class Occurrence:
    line: int
    column: int


@dataclass
class Symbol:
    token_type: str
    super_type: TokenSuperType
    word: str
    scope: Scope = None
    occurrences: List[Occurrence] = field(default_factory=list)

