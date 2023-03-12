from typing import List

from src.utils.expressions import expression_util
from src.utils.objects import Objective
from src.utils.table import Table


class Simplex:
    def __init__(self, literal_objective_function: str, objective):
        self.pivot_column_index = 0
        self.literal_objective_function = literal_objective_function
        self.inserted = 0
        self.table: List[List[int]] = []
        self.column_b = [0]
        self.objective = objective
        self.objective_function = self._build_objective_function(literal_objective_function)

    def _build_objective_function(self, objective_function: str):
        row = list(
            map(
                lambda value: value * (-1),
                expression_util.convert_in_calculable_expression(objective_function),
            )
        )
        return [1] + row

    def add_constraints(self, expression: str):
        """Adiciona restrição"""
        delimiter = "<="
        default_format = True

        if not self.is_simplex_standard(expression):
            raise ValueError("Simplex Duas Fases não implementado!")

        splitted_expression = expression.split(delimiter)
        constraint = [0] + expression_util.convert_in_calculable_expression(
            splitted_expression[0]
        )

        if not default_format:
            self.objective_function += [0]

        constraint = self.insert_slack_var(constraint, default_format)
        self.column_b.append(int(splitted_expression[1]))
        self.table.append(constraint)

    def insert_slack_var(self, row: List[int], default_format=True) -> List[int]:
        """Insere variável de folga na restrição"""
        self.objective_function.append(0)

        if not self.table:
            row.append(1)
            self.inserted += 1
            return row

        limit = len(self.table[self.inserted - 1]) - len(row)

        for _ in range(limit):
            row.append(0)

        if not default_format:
            row = row + [-1, 1]
        else:
            row.append(1)

        self.inserted += 1

        return row

    def is_simplex_standard(self, constraint: str) -> bool:
        """Verifica se a restrição está no padrão do simplex"""
        return "<=" in constraint and self.objective == Objective.MAX.value

    def is_optimal(self) -> bool:
        """Verifica se existe valores negativos na primeira linha da tabela: FO"""
        if list(filter(lambda value: value < 0, self.table[0])):
            return False
        return True

    def get_entry_column(self) -> List[int]:
        """Define a coluna pivô"""
        pivot_fo = min(self.table[0])  # menor valor negativo na linha 0 (F.O)
        self.pivot_column_index = self.table[0].index(pivot_fo)

        return [
            self.table[index][self.pivot_column_index] for index in range(len(self.table))
        ]

    def get_pivot_line(self, entry_column: List[int]) -> List[int]:
        """identifica a linha que sai"""
        metadata: dict = {}

        for index, row in enumerate(self.table):
            if index > 0 and entry_column[index] > 0:
                metadata[index] = row[-1] / entry_column[index]

        return min(metadata, key=metadata.get)

    def calculate_new_line(self, row: List[int], pivot_line: List[int]) -> List[int]:
        """
        Calcula a nova linha que será substituída na tabela
        row (list) -> linha que será trocada
        pivot_line (list) -> linha pivô
        """

        pivot = row[self.pivot_column_index] * -1

        result_line = [pivot * value for value in pivot_line]

        new_line = list(map(lambda x, y: x + y, result_line, row))

        return new_line

    def calculate(self, table: List[List[int]]) -> None:
        column = self.get_entry_column()
        # linha que vai sair
        first_exit_line = self.get_pivot_line(column)

        line = table[first_exit_line]
        # identificando o pivo da linha que vai sair
        pivot = line[self.pivot_column_index]

        # calculando nova linha pivô
        pivot_line = list(map(lambda x: x / pivot, line))

        # substituindo a linha que saiu pela nova linha pivô
        table[first_exit_line] = pivot_line

        stack = table.copy()

        line_reference = len(stack) - 1

        while stack:
            row = stack.pop()

            if line_reference != first_exit_line:
                new_line = self.calculate_new_line(row, pivot_line)

                table[line_reference] = new_line

            line_reference -= 1

    def solve(self):
        self.table = Table.normalize_table(self.objective_function, self.table, self.column_b)
        self.calculate(self.table)

        while not self.is_optimal():
            self.calculate(self.table)

        incognitas = expression_util.get_incognitas(self.literal_objective_function)

        return Table.get_results(self.table, incognitas)
