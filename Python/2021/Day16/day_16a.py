from typing import Any

import numpy as np


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if testing:
        if len(inputs) == 0:
            file_to_read = 'test.txt'
        else:
            return inputs
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        line = file.read().splitlines()[0]
        return np.array(list(f'{int("0x" + line, 16):0>{len(line) * 4}b}'), dtype=int)


def bin2dec(*digits: int):
    num = ''.join([str(i) for i in digits])
    return int(f'0b{num}', 2)


class Parser:
    def __init__(self, bits: np.ndarray):
        self.bits = bits
        self.instruction: list[str | int] = ['version']
        self.version_list = []

    def parse(self):
        while np.any(self.bits):
            self.generic_parse()

    def parse_operator_0(self, bit_count):
        bit_counter = 0
        while bit_counter != bit_count:
            parsed_bits, parsed_packets = self.generic_parse()
            bit_counter += parsed_bits

    def parse_operator_1(self, packet_count) -> int:
        packet_counter = 0
        bit_counter = 0
        while packet_counter != packet_count:
            parsed_bits, parsed_packets = self.generic_parse()
            packet_counter += parsed_packets
            bit_counter += parsed_bits
        return bit_counter

    def generic_parse(self):
        parsed_packets = 0
        match self.instruction:
            case ['version']:
                packet_version, self.bits = bin2dec(*self.bits[:3]), self.bits[3:]
                self.version_list.append(packet_version)
                self.instruction = ['id']
                parsed_bits = 3
            case ['id']:
                packet_id, self.bits = bin2dec(*self.bits[:3]), self.bits[3:]
                if packet_id == 4:
                    self.instruction = ['literal']
                    parsed_bits = 3
                else:
                    self.instruction = ['operator']
                    operator_type, self.bits = self.bits[0], self.bits[1:]
                    self.instruction.append(operator_type)
                    parsed_bits = 4
            case ['literal']:
                literal_prefix, num, self.bits = self.bits[0], self.bits[1:5], self.bits[5:]
                if not literal_prefix:
                    self.instruction = ['version']
                    parsed_packets += 1
                parsed_bits = 5
            case ['operator', length_type]:
                if not length_type:
                    parsed_bits, self.bits = bin2dec(*self.bits[:15]), self.bits[15:]
                    self.instruction.append(parsed_bits)
                    parsed_bits = 15
                else:
                    packet_count, self.bits = bin2dec(*self.bits[:11]), self.bits[11:]
                    self.instruction.append(packet_count)
                    parsed_bits = 11
            case ['operator', 0, bit_count]:
                self.instruction = ['version']
                self.parse_operator_0(bit_count)
                parsed_packets += 1
                parsed_bits = bit_count
            case ['operator', 1, packet_count]:
                self.instruction = ['version']
                parsed_bits = self.parse_operator_1(packet_count)
                parsed_packets += 1
            case e:
                raise NotImplementedError(e)
        return parsed_bits, parsed_packets


def solver(bits: np.ndarray) -> Any:
    bits_parser = Parser(bits)
    bits_parser.parse()
    return sum(bits_parser.version_list)


def display(version_sum) -> None:
    print(version_sum)


if __name__ == '__main__':
    answer = solver(parser(
        file_name='day_16.txt',
        testing=False))
    display(answer)
