from dataclasses import dataclass
from src.backend.PacketEnums import Variable, Command
from typing import Optional, Tuple

@dataclass
class Ability:
    name: str
    cost: int
    trigger: Optional[Tuple[Optional[Command], Optional[Variable]]]
    # team target command variable value
    packets: list[tuple]
