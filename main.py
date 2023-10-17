import numpy as np
from itertools import groupby


class NfaToDfa:

    def __init__(self):
        self.nfa_matrix = np.matrix(['main', 'end', 'value', 'is_end'])
        self.dfa_matrix = np.matrix(['main', 'end', 'value', 'is_end'])
        self.processes_count = 0
        self.directions = 0
        self.loop_count = 0

    def main(self):
        self.input_nfa_process()
        print(self.nfa_matrix)

    def change_nfa_to_dfa(self):
        for i in range(1, self.loop_count):
            pass

    def input_nfa_process(self) -> None:
        processes = int(input('How many Processes in your nfa: '))
        for process in range(processes):
            is_end = bool(int(input(f'Is q{process} final processing? (if yes put 1 if no put 0)')))
            directions = int(input(f'How many Direction in your nfa q{process}: '))
            self.directions += directions
            for direction in range(directions):
                which_process = self.check_process(processes)
                value = input('Put value: ')
                self.loop_count += 1
                self.nfa_matrix = np.insert(self.nfa_matrix, self.loop_count, (f'q{process}', which_process, value, is_end), axis=0)
        self.processes_count = processes

    @staticmethod
    def check_process(count_processes: int) -> str:
        is_process = False
        while not is_process:
            which_process = input('To which process? ')
            p_number = [int(''.join(i)) for is_digit, i in groupby(which_process, str.isdigit) if is_digit]
            if p_number[0] > count_processes - 1:
                print('This Process Invalid')
                continue
            return which_process
        return ''


if __name__ == '__main__':
    NfaToDfa().main()

