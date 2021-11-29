import re
import string
import sys


class Table:

    @classmethod
    def _get_z(cls, table: list) -> int:
        for row in table:
            if row[0] == 1:
                return row[-1]
        return 0

    @classmethod
    def show_table(cls, table: list):
        for i in range(len(table)):
            for j in range(len(table[i])):
                print(f"{table[i][j]}\t", end="")
            print()

    @classmethod
    def _get_basic_vars(cls, table: list) -> list:
        basics = []
        for i in range(len(table[0])):
            basic = 0
            for j in range(len(table)):
                basic += abs(table[j][i])

            if basic == 1:
                basics.append(i)

        return basics

    @classmethod
    def get_results(cls, table: list, coefficients: list) -> (dict, dict):
        basics = cls._get_basic_vars(table)

        meta = {
            "solution": cls._get_z(table),
        }

        basics.remove(0)

        try:
            for index in basics:
                var = coefficients[index - 1]
                for j in range(len(table)):
                    value = table[j][index]
                    if value == 1:
                        meta[var] = table[j][-1]
                        break
        except Exception as e:
            pass

        for var in coefficients:
            if not var in meta:
                meta[var] = 0

        return meta


class Simplex:

    pivot_column_index = 0
    inserted = 0
    coefficients = []

    def __init__(self, fo: str, objective):
        self.table = []
        self.coefficients = re.findall("[a-z]", fo)
        row = list(map(lambda x: x * (-1), self.convert_expr(fo)))
        self.fo = [1] + row
        self.column_b = [0]
        self.objective = objective
        self.variables = list(string.ascii_lowercase)

    # Utilitários para a aplicação

    def is_valid_coefficients(self, expr: str):
        """ Verifica se existem coeficientes repetidos """
        expr = expr.replace(" ", "")

        coefficients = re.findall("[a-z]", expr)
        data = re.split("\\+|\\-|<=", expr)
        is_duplicated = lambda x: len(x) != len(set(x))

        if is_duplicated(coefficients):
            raise TypeError("Existe coeficientes repetidos na expressão informada")

        return True

    def convert_expr(self, expr: str):
        """ Converte a expressão em um padrão calculável pelo algoritmo """
        if self.is_valid_coefficients(expr):
            expr = expr.replace(" ", "")

            coefficients = re.findall("[a-z]", expr)

            if coefficients != sorted(coefficients):
                raise ValueError("Utilize variáveis em sequência ordenada!")

            pattern = ">=|\\+|\\-|<="
            separated_data = re.split(pattern, expr)

            values = []

            for coefficient in self.coefficients:
                contains = False
                for var in separated_data:
                    if coefficient in var:
                        value = re.findall(r"-?\d+", var)
                        values.append(value[0] if value else 1)
                        contains = True

                if not contains:
                    values.append(0)

            return list(map(int, values))

    def normalize_table(self):
        """ Configura as variáveis para cada linha na tabela """
        self.table.insert(0, self.fo)
        normal_size = len(self.fo)
        for row in self.table:
            if len(row) < normal_size:
                addition = normal_size - len(row)
                for i in range(addition):
                    row.append(0)
        self.table = list(map(lambda x, y: x + [y], self.table, self.column_b))

    ### Métodos relacionados ao simplex ###

    def add_constraints(self, expr: str):
        """ Adiciona restrição """
        delimiter = "<="
        default_format = True

        if not self.simplex_standard(expr):
            raise ValueError("Simplex Duas Fases não implementado!")

        expr_list = expr.split(delimiter)
        sa = [0] + self.convert_expr(expr_list[0])

        if not default_format:
            self.fo = self.fo + [0]

        sa = self.insert_slack_var(sa, default_format)
        self.column_b.append(int(expr_list[1]))
        self.table.append(sa)

    def insert_slack_var(self, row: list, default_format=True):
        """ Insere variável de folga na restrição """
        self.fo.append(0)

        if not self.table:
            row.append(1)
            self.inserted += 1
            return row

        loop = len(self.table[self.inserted - 1]) - len(row)
        for i in range(loop):
            row.append(0)

        if not default_format:
            row = row + [-1, 1]
        else:
            row.append(1)

        self.inserted += 1

        return row

    def simplex_standard(self, sa: str):
        """ Verifica se a restrição está no padrão do simplex """
        return "<=" in sa and self.objective == 0

    def is_optimal(self):
        """ Verifica se existe valores negativos na primeira linha da tabela: FO"""
        ocurrence = list(filter(lambda x: x < 0, self.table[0]))

        return False if ocurrence else True

    def get_entry_column(self):
        """ Define a coluna pivô """
        pivot_fo = min(self.table[0])  # menor valor negativo na linha 0 (F.O)
        self.pivot_column_index = self.table[0].index(pivot_fo)

        column = []
        for i in range(len(self.table)):
            column.append(self.table[i][self.pivot_column_index])

        return column

    def get_pivot_line(self, entry_column: list):
        """ identifica a linha que sai """
        meta = {}

        for i, row in enumerate(self.table):
            if i > 0:
                if entry_column[i] > 0:
                    meta[i] = row[-1] / entry_column[i]

        return min(meta, key=meta.get)

    def calculate_new_line(self, row: list, pivot_line: list):
        """
        Calcula a nova linha que será substituída na tabela
        row (list) -> linha que será trocada
        pivot_line (list) -> linha pivô
        """

        pivot = row[self.pivot_column_index] * -1

        result_line = [pivot * value for value in pivot_line]

        new_line = list(map(lambda x, y: x + y, result_line, row))

        return new_line

    def calculate(self):
        column = self.get_entry_column()
        # linha que vai sair
        first_exit_line = self.get_pivot_line(column)

        line = self.table[first_exit_line]
        # identificando o pivo da linha que vai sair
        pivot = line[self.pivot_column_index]

        # calculando nova linha pivô
        pivot_line = list(map(lambda x: x / pivot, line))

        # substituindo a linha que saiu pela nova linha pivô
        self.table[first_exit_line] = pivot_line

        stack = self.table.copy()

        line_reference = len(stack) - 1

        while stack:

            row = stack.pop()

            if line_reference != first_exit_line:

                new_line = self.calculate_new_line(row, pivot_line)

                self.table[line_reference] = new_line

            line_reference -= 1

    def solve(self):
        self.normalize_table()
        self.calculate()

        while not self.is_optimal():
            self.calculate()

        return Table.get_results(self.table, self.coefficients)
