import sys
from typing import List

from src.encoder import Encoder
from src.parser import Parser
from src.enumerations import InstructionType


class Assembler:
    MEM_START_ADDR = 16

    def __init__(self, asm_file_path: str):
        self.asm_file_path = asm_file_path

        self.hack_file_path = asm_file_path.replace(asm_file_path.split('.')[-1], 'hack')

        self.__build_symbol_table()

    def run(self):
        file = open(file=self.asm_file_path, mode='r')
        file_lines = file.readlines()

        self.hack_file = open(self.hack_file_path, 'w')

        self.first_pass(file_lines)

        self.second_pass(file_lines)

        file.close()
        self.hack_file.close()

    def first_pass(self, file_lines: List):
        instruction_counter = 0

        for line in file_lines:
            parser = Parser(instruction=line)

            if parser.instruction_type == InstructionType.label:
                self.symbol_table[parser.label] = instruction_counter

            elif parser.instruction_type in (InstructionType.a_instruction, InstructionType.c_instruction):
                instruction_counter += 1

    def second_pass(self, file_lines):
        memory_address = self.MEM_START_ADDR
        for line in file_lines:
            parser = Parser(instruction=line)
            encoder = Encoder(instruction_type=parser.instruction_type)

            if parser.instruction_type == InstructionType.c_instruction:
                hack_line = encoder.encode(dest=parser.dest, comp=parser.comp, jump=parser.jump)

            elif parser.instruction_type == InstructionType.a_instruction:
                try:
                    integer_address = int(parser.address)
                except ValueError:
                    if self.symbol_table.get(parser.address) is None:
                        self.symbol_table[parser.address] = memory_address
                        memory_address += 1

                    integer_address = self.symbol_table.get(parser.address)

                hack_line = encoder.encode(address=integer_address)

            else:
                continue

            self.hack_file.write(hack_line + '\r\n')

    def __build_symbol_table(self):
        self.symbol_table = {
            **{f'R{i}': i for i in range(0, 16)},
            'SCREEN': 16384,
            'KEYBOARD': 24576,
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4
        }


if __name__ == '__main__':
    Assembler(sys.argv[1]).run()
