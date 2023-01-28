from dataclasses import dataclass


DIGITS = "0123456789"
CHARACTERS = "abcdefghijklmnopqrstuvwxyz"
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
class CharToken:
    value: str

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"CharToken: {self.value}"


@dataclass
class StringToken:
    value: str

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"StringToken: {self.value}"


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
class NegToken:
    def __str__(self):
        return "~"

    def __repr__(self) -> str:
        return "NegToken: ~"


@dataclass
class AndToken:
    def __str__(self):
        return "&"

    def __repr__(self) -> str:
        return "AndToken: &"


@dataclass
class OrToken:
    def __str__(self):
        return "|"

    def __repr__(self) -> str:
        return "OrToken: |"


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


@dataclass
class OSBToken:
    def __str__(self):
        return "["

    def __repr__(self) -> str:
        return "OSBToken: ["


@dataclass
class CSBToken:
    def __str__(self):
        return "]"

    def __repr__(self) -> str:
        return "CSBToken: ]"


@dataclass
class CommaToken:
    def __str__(self):
        return ","

    def __repr__(self) -> str:
        return "CommaToken: ,"


@dataclass
class SemiColonToken:
    def __str__(self):
        return ";"

    def __repr__(self) -> str:
        return "SemiColonToken: ;"


class Tokenizer:
    def __init__(self, string: str):
        self.string = string.lower()
        self._string_iterator = iter(self.string)
        self._current_character = self._advance_string()

    def _advance_string(self):
        try:
            return next(self._string_iterator)
        except StopIteration:
            return None

    def generate_tokens(self):
        while self._current_character is not None:
            if self._current_character == "+":
                yield AddToken

            elif self._current_character == "-":
                yield SubToken

            elif self._current_character == "*":
                yield MulToken

            elif self._current_character == "/":
                yield DivToken

            elif self._current_character == "^":
                yield PowToken

            elif self._current_character == "~":
                yield NegToken

            elif self._current_character == "&":
                yield AndToken

            elif self._current_character == "|":
                yield OrToken

            elif self._current_character == "(":
                yield OPToken

            elif self._current_character == ")":
                yield CPToken

            elif self._current_character in CHARACTERS:
                yield self._generate_string()
                continue

            elif self._current_character in DIGITS or self._current_character == ".":
                yield self._generate_number()
                continue

            elif self._current_character in IGNORE:
                self._current_character = self._advance_string()
                continue

            else:
                raise SyntaxError(
                    f"Could not tokenize the input text: {self._current_character}"
                )

            self._current_character = self._advance_string()

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
                number = number + self._current_character if number != "" else "0."
            else:
                break

            self._current_character = self._advance_string()

        if is_decimal:
            return DecimalToken(float(number))
        return IntegerToken(int(number))

    def _generate_string(self):
        string = ""

        while self._current_character is not None:
            if self._current_character in CHARACTERS:
                string += self._current_character
            else:
                break
            self._current_character = self._advance_string()

        if len(string) > 1:
            return StringToken(string)
        return CharToken(string)


if __name__ == "__main__":
    print(list(Tokenizer(input("math > ")).generate_tokens()))
