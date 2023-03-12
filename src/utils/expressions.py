import re
from typing import List


class ExpressionUtils:
    def __sanitize_expression(self, expression: str):
        return expression.replace(" ", "")

    def get_incognitas(self, expression: str):
        return re.findall("[a-z]", expression)

    def __is_duplicated(self, collection: List[int]) -> bool:
        return len(collection) != len(set(collection))

    def validate_incognitas(self, expression: str) -> None:
        """Verifica se existem incognitas repetidas"""

        incognitas = self.get_incognitas(expression)
        # data = re.split("\\+|\\-|<=", expr)

        if self.__is_duplicated(incognitas):
            raise TypeError("Existe incógnitas repetidas na expressão informada")

        if incognitas != sorted(incognitas):
            raise ValueError("Utilize incógnitas em sequência ordenada!")

    def get_algebraic_expressions(self, expression: str):
        pattern = ">=|\\+|\\-|<="
        splited = re.split(pattern, expression)
        return splited

    def __extract_numeric_value_from_monomial(self, monomial: str) -> str:
        if value := re.findall(r"-?\d+", monomial):
            return value[0]
        return "1"

    def convert_in_calculable_expression(self, expression: str) -> List[int]:
        """Converte a expressão em um padrão calculável pelo algoritmo"""
        expression = self.__sanitize_expression(expression)

        self.validate_incognitas(expression)

        algebraic_expressions = self.get_algebraic_expressions(expression)

        values = []

        for incognita in self.get_incognitas(expression):
            for monomial in algebraic_expressions:
                if incognita in monomial:
                    value = self.__extract_numeric_value_from_monomial(monomial)
                    values.append(value)
                else:
                    values.append("0")

        return list(map(int, values))


expression_util = ExpressionUtils()
