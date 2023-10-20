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
        self.next_move()
        self.check_end_dfa()
        self.is_end()
        self.insert_none_dfa()
        print(self.nfa_matrix)
        print('\n')
        print(self.dfa_matrix)
        print('\n')
        print(self.nfa_status_matrix)
        print('\n')
        print(self.dfa_status_matrix)

    def check_end_dfa(self) -> None:
        count = 0
        while len(self.dfa_matrix) != count:
            count = len(self.dfa_matrix)
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
            for value in values:
                for x in self.nfa_matrix:
                    if x.item(0) == '_____main_____':
                        continue
                    if x.item(0) == value:
                        self.append_list_data(value_0, value_1, x)
            value_0 = [None] if len(value_0) == 0 else list(set(value_0))
            value_1 = [None] if len(value_1) == 0 else list(set(value_1))
            value_0 = self.list_to_str(value_0)
            value_1 = self.list_to_str(value_1)
            if 0 not in np.where(self.dfa_matrix == i.item(1))[1]:
                self.insert_data('dfa', i.item(1), value_0, '0')
                self.insert_data('dfa', i.item(1), value_1, '1')
                self.insert_status('dfa', i.item(1), 'False')

    def append_list_data(self, value_0, value_1, x):
        if x.item(2) == '0':
            value_0.append(x.item(1))
            self.loop_next_none_insert(x, value_0)
        elif x.item(2) == '1':
            value_1.append(x.item(1))
            self.loop_next_none_insert(x, value_1)
        else:
            self.loop_for_none(x, value_0, value_1)

    def loop_next_none_insert(self, x, value):
        find_nfa = np.where(self.nfa_matrix == x.item(1))
        for v in range(len(find_nfa)):
            if 0 not in find_nfa[1] and find_nfa[1][v] != 0:
                break
            find_nfa_data = self.nfa_matrix.item(find_nfa[0][v], find_nfa[1][v])
            data = 'None'
            while data == 'None':
                for m in self.nfa_matrix:
                    if m.item(0) == '_____main_____':
                        continue
                    if m.item(0) == find_nfa_data or m.item(1) == find_nfa_data:
                        if m.item(2) == 'None':
                            if m.item(1) in value:
                                data = 'Break'
                                continue
                            value.append(m.item(1))
                            find_nfa_data = m.item(1)
                            data = 'None'
                        else:
                            data = 'Break'

    def loop_for_none(self, x, value_0, value_1) -> None:
        find_nfa = np.where(self.nfa_matrix == x.item(1))
        for v in range(len(find_nfa)):
            if 0 not in find_nfa[1] and find_nfa[1][v] != 0:
                break
            find_nfa_data = self.nfa_matrix.item(find_nfa[0][v], find_nfa[1][v])
            data = x.item(2)
            while data == 'None':
                for m in self.nfa_matrix:
                    if m.item(0) == '_____main_____':
                        continue
                    if m.item(0) == find_nfa_data:
                        if m.item(2) == '0':
                            value_0.append(m.item(1))
                            data = 'Break'
                        elif m.item(2) == '1':
                            value_1.append(m.item(1))
                            data = 'Break'
                        else:
                            data = m.item(2)
                            find_nfa_data = m.item(1)

    def get_q0_move(self) -> None:
        value_0 = []
        value_1 = []
        for i in self.nfa_matrix:
            if i.item(0) == '_____main_____':
                continue
            if i.item(0) == 'q0':
                self.append_list_data(value_0, value_1, i)
        value_0 = [None] if len(value_0) == 0 else list(set(value_0))
        value_1 = [None] if len(value_1) == 0 else list(set(value_1))
        find_q0 = np.where(self.nfa_status_matrix == 'q0')
        is_end = 'True' if self.nfa_status_matrix.item(int(find_q0[0][0]), 1) == 'True' else 'False'
        value_0 = self.list_to_str(value_0)
        value_1 = self.list_to_str(value_1)
        self.insert_data('dfa', 'q0', value_0, '0')
        self.insert_data('dfa', 'q0', value_1, '1')
        self.insert_status('dfa', 'q0', is_end)

    def insert_none_dfa(self) -> None:
        if 0 not in np.where(self.dfa_matrix == 'None')[1] and len(np.where(self.dfa_matrix == 'None')[0]) > 0:
            self.insert_data('dfa', 'None', 'None', '0')
            self.insert_data('dfa', 'None', 'None', '1')
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

    def is_end(self):
        for value in self.dfa_status_matrix:
            is_end_main = []
            if value.item(0) == '_____main_____' or value.item(0) == 'q0' or value.item(0) == 'None':
                continue
            value_list = self.open_str(value.item(0))
            for i in value_list:
                find_q0 = np.where(self.nfa_status_matrix == i)
                is_end = 1 if self.nfa_status_matrix.item(int(find_q0[0][0]), 1) == 'True' else 0
                is_end_main.append(is_end)
            is_end_main = any(is_end_main)
            np.put(value, [1], is_end_main)

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
