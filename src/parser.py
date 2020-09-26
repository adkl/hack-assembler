import re
from typing import Optional

from src.enumerations import InstructionType


class Parser:
    LABEL_PATTERN = re.compile(r'^\((?P<label>.+)\)$')
    A_PATTERN = re.compile(r'^\s*@(?P<addr>\S+)')
    C_PATTERN = re.compile(r'^\s*((?P<dest>A?M?D?)=)?(?P<comp>(0|1|[ADM]?-[1ADM]{1}|![ADM]{1}|[ADM]?[\+\|\&]?[1ADM]{1}))(?P<jump>;(JMP|JGE|JLE|JNE|JGT|JLT|JEQ))?')

    def __init__(self, instruction: str):
        self.instruction = instruction.strip()

        self._decode_instruction_type()

    @property
    def address(self) -> str:
        return self._address

    @property
    def comp(self) -> str:
        return self._comp

    @property
    def dest(self) -> str:
        return self._dest

    @property
    def instruction_type(self) -> Optional[InstructionType]:
        return self._instruction_type

    @property
    def jump(self) -> str:
        return self._jump

    @property
    def label(self):
        return self._label

    def _decode_instruction_type(self):
        self._instruction_type = None

        match_a = self.A_PATTERN.match(self.instruction)
        match_c = self.C_PATTERN.match(self.instruction)
        match_label = self.LABEL_PATTERN.match(self.instruction)

        if match_a:
            self._instruction_type = InstructionType.a_instruction
            self._address = match_a.group(1)

        elif match_c:
            self._instruction_type = InstructionType.c_instruction
            self._dest = match_c.group(self.C_PATTERN.groupindex['dest'])
            self._comp = match_c.group(self.C_PATTERN.groupindex['comp'])
            self._jump = match_c.group(self.C_PATTERN.groupindex['jump'])

        elif match_label:
            self._instruction_type = InstructionType.label
            self._label = match_label.group(1)

        else:
            self._instruction_type = None
