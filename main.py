import numpy as np
from itertools import groupby


class NfaToDfa:

    def __init__(self):
        self.nfa_matrix = np.matrix(['_____main_____', '_____end_____', '_____value_____'])
        self.dfa_matrix = np.matrix(['_____main_____', '_____end_____', '_____value_____'])
        self.nfa_status_matrix = np.matrix(['_____main_____', '_____is_end_____'])
        self.dfa_status_matrix = np.matrix(['_____main_____', '_____is_end_____'])
        self.nfa_count = 1
        self.dfa_count = 1
        self.nfa_status_count = 1
        self.dfa_status_count = 1

    def main(self):
        self.input_nfa_process()
        self.get_q0_move()
        # self.insert_none_dfa()
        self.next_move()
        self.check_end_dfa()
        print(self.nfa_matrix)
        print('\n')
        print(self.dfa_matrix)
        print('\n')
        print(self.nfa_status_matrix)
        print('\n')
        print(self.dfa_status_matrix)

    def check_end_dfa(self) -> None:
        for i in self.dfa_matrix:
            if i.item(0) == '_____main_____' or i.item(1) == 'None':
                continue
            if 0 not in np.where(self.dfa_matrix == i.item(1))[1]:
                self.next_move()

    def next_move(self) -> None:
        for i in self.dfa_matrix:
            if i.item(0) == '_____main_____':
                continue
            values = self.open_str(i.item(1))
            value_0 = []
            value_1 = []
            is_end_main = []
            for value in values:
                find_q0 = np.where(self.nfa_status_matrix == value)
                is_end = 1 if self.nfa_status_matrix.item(int(find_q0[0][0]), 1) == 'True' else 0
                is_end_main.append(is_end)

                for x in self.nfa_matrix:
                    if x.item(0) == '_____main_____':
                        continue
                    if x.item(0) == value:
                        if x.item(2) == '0':
                            value_0.append(x.item(1))
                        else:
                            value_1.append(x.item(1))
                if value == i.item(0):
                    break
            value_0 = [None] if len(value_0) == 0 else list(set(value_0))
            value_1 = [None] if len(value_1) == 0 else list(set(value_1))
            print(value_0)
            is_end_main = any(is_end_main)
            value_0 = self.list_to_str(value_0)
            value_1 = self.list_to_str(value_1)
            if 0 not in np.where(self.dfa_matrix == i.item(1))[1]:
                self.insert_data('dfa', i.item(1), value_0, '0')
                self.insert_data('dfa', i.item(1), value_1, '1')
                self.insert_status('dfa', i.item(1), is_end_main)

    def get_q0_move(self):
        value_0 = []
        value_1 = []
        for i in self.nfa_matrix:
            if i.item(0) == '_____main_____':
                continue
            if i.item(0) == 'q0':
                if i.item(2) == '0':
                    value_0.append(i.item(1))
                else:
                    value_1.append(i.item(1))
        value_0 = [None] if len(value_0) == 0 else value_0
        value_1 = [None] if len(value_1) == 0 else value_1
        find_q0 = np.where(self.nfa_status_matrix == 'q0')
        is_end = 'True' if self.nfa_status_matrix.item(int(find_q0[0][0]), 1) == 'True' else 'False'
        value_0 = self.list_to_str(value_0)
        value_1 = self.list_to_str(value_1)
        self.insert_data('dfa', 'q0', value_0, '0')
        self.insert_data('dfa', 'q0', value_1, '1')
        self.insert_status('dfa', 'q0', is_end)
        return value_0, value_1

    def insert_none_dfa(self) -> None:
        if len(np.where(self.dfa_matrix)[0]) > 0:
            self.insert_data('dfa', 'None', 'None', '0')
            self.insert_data('dfa', 'None', 'None', '1')
            self.insert_status('dfa', 'None', 'False')
            self.insert_status('dfa', 'None', 'False')

    def input_nfa_process(self) -> None:
        processes = int(input('How many Processes in your nfa: '))
        for process in range(processes):
            is_end = bool(int(input(f'Is q{process} final processing? (if yes put 1 if no put 0)')))
            directions = int(input(f'How many Direction in your nfa q{process}: '))
            for direction in range(directions):
                which_process = self.check_process(processes)
                value = input('Put value: ')
                self.insert_data('nfa', f'q{process}', which_process, value)
            self.insert_status('nfa', f'q{process}', is_end)

    def insert_data(self, nfa_or_dfa, process, which_process, value) -> None:
        if nfa_or_dfa == 'nfa':
            self.nfa_matrix = np.insert(self.nfa_matrix, self.nfa_count, (process, which_process, value), axis=0)
            self.nfa_count += 1
        else:
            self.dfa_matrix = np.insert(self.dfa_matrix, self.dfa_count, (process, which_process, value), axis=0)
            self.dfa_count += 1

    def insert_status(self, nfa_or_dfa, process, is_end):
        if nfa_or_dfa == 'nfa':
            self.nfa_status_matrix = np.insert(self.nfa_status_matrix, self.nfa_status_count, (process, is_end), axis=0)
            self.nfa_status_count += 1
        else:
            self.dfa_status_matrix = np.insert(self.dfa_status_matrix, self.dfa_status_count, (process, is_end), axis=0)
            self.dfa_status_count += 1

    @staticmethod
    def list_to_str(value):
        value.sort()
        return f'{",".join(str(e) for e in value)}'

    @staticmethod
    def open_str(value) -> list:
        return value.split(",")

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
