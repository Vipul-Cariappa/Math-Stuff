from dataclasses import dataclass


DIGITS = "0123456789"
IGNORE = " \n\t\r"


@dataclass
class IntegerToken:
    value: int

    def __str__(self):
        return str(self.value)

    def __repr__(self) -> str:
        return f"IntegerToken: {self.value}"


@dataclass
class DecimalToken:
    value: float

    def __str__(self):
        return str(self.value)

    def __repr__(self) -> str:
        return f"DecimalToken: {self.value}"


@dataclass
class AddToken:
    def __str__(self):
        return "+"

    def __repr__(self) -> str:
        return "AddToken: +"


@dataclass
class SubToken:
    def __str__(self):
        return "-"

    def __repr__(self) -> str:
        return "SubToken: -"


@dataclass
class MulToken:
    def __str__(self):
        return "*"

    def __repr__(self) -> str:
        return "MulToken: *"


@dataclass
class DivToken:
    def __str__(self):
        return "/"

    def __repr__(self) -> str:
        return "DivToken: /"


@dataclass
class PowToken:
    def __str__(self):
        return "^"

    def __repr__(self) -> str:
        return "PowToken: ^"


@dataclass
class OPToken:
    def __str__(self):
        return "("

    def __repr__(self) -> str:
        return "OPToken: ("


@dataclass
class CPToken:
    def __str__(self):
        return ")"

    def __repr__(self) -> str:
        return "CPToken: )"


# TODO: add the following tokens: | & ~


class Tokenizer:
    def __init__(self, string: str):
        self.string = string
        self._string_iterator = iter(self.string)
        self._current_character = self._advance_string()

    def _advance_string(self):
        try:
            return next(self._string_iterator)
        except StopIteration:
            return None

    def generate_tokens(self):
        while self._current_character is not None:
            if self._current_character in IGNORE:
                self._current_character = self._advance_string()
            elif self._current_character == "+":
                yield AddToken
                self._current_character = self._advance_string()
            elif self._current_character == "-":
                yield SubToken
                self._current_character = self._advance_string()
            elif self._current_character == "*":
                yield MulToken
                self._current_character = self._advance_string()
            elif self._current_character == "/":
                yield DivToken
                self._current_character = self._advance_string()
            elif self._current_character == "^":
                yield PowToken
                self._current_character = self._advance_string()
            elif self._current_character == "(":
                yield OPToken
                self._current_character = self._advance_string()
            elif self._current_character == ")":
                yield CPToken
                self._current_character = self._advance_string()
            elif self._current_character in DIGITS or self._current_character == ".":
                yield self._generate_number()
            else:
                raise SyntaxError(
                    f"Could not tokenize the input text: {self._current_character}"
                )

    def _generate_number(self):
        is_decimal = False
        number = ""

        while self._current_character is not None:
            if self._current_character in DIGITS:
                number += self._current_character

            elif self._current_character == ".":
                if is_decimal is True:
                    raise SyntaxError("Found 2 decimal points in the number")

                is_decimal = True
                number = self._current_character if number != "" else "0."
            else:
                if is_decimal:
                    return DecimalToken(float(number))
                return IntegerToken(int(number))

            self._current_character = self._advance_string()

        if is_decimal:
            return DecimalToken(float(number))
        return IntegerToken(int(number))


if __name__ == "__main__":
    print(list(Tokenizer(input("math > ")).generate_tokens()))
