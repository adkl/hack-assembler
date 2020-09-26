from enum import Enum


class InstructionType(Enum):
    a_instruction = 1
    c_instruction = 2
    label = 3
    rest = 4
