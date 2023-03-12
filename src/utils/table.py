from typing import Any, Dict, List


class Table:
    @classmethod
    def _get_solution(cls, table: List[List[int]]) -> int:
        for row in table:
            if row[0] == 1:
                return row[-1]
        return 0

    @classmethod
    def show_table(cls, table: List[List[int]]):
        for row in range(len(table)):
            for column in range(len(table[row])):
                print(f"{table[row][column]}\t", end="")
            print()

    @classmethod
    def _get_basic_vars(cls, table: List[List[int]]) -> list:
        basics = []
        for i in range(len(table[0])):
            basic = 0
            for j in range(len(table)):
                basic += abs(table[j][i])

            if basic == 1:
                basics.append(i)

        return basics

    @classmethod
    def normalize_table(cls, objective_function, table: List[List[int]], column_b: List[int]):
        """Configura as variáveis para cada linha na tabela"""
        table.insert(0, objective_function)
        normal_size = len(objective_function)
        for row in table:
            if len(row) < normal_size:
                addition = normal_size - len(row)
                for _ in range(addition):
                    row.append(0)
        return list(map(lambda x, y: x + [y], table, column_b))

    @classmethod
    def get_results(
        cls, table: List[List[int]], incognitas: List[str]
    ) -> Dict[str, Any]:  # noqa: E501
        basic_variables = cls._get_basic_vars(table)

        metadata = {
            "solution": cls._get_solution(table),
        }

        basic_variables.remove(0)

        try:
            for index in basic_variables:
                incognita = incognitas[index - 1]
                for j in range(len(table)):
                    value = table[j][index]
                    if value == 1:
                        metadata[incognita] = table[j][-1]
                        break
        except Exception:
            pass

        for incognita in incognitas:
            if incognita not in metadata:
                metadata[incognita] = 0

        return metadata
