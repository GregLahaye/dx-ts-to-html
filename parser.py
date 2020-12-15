from constants import example

from enum import Enum


class ParseMode(Enum):
    NONE = 0
    KEY = 1
    VALUE = 2


class Parser():
    def __init__(self, root: str):
        self.root = root
        self.mode = ParseMode.KEY
        self.array = False
        self.depth = 0
        self.tags = []
        self.open = True

    def parse(self):
        self.print("<dx-my-type")
        while self.root:
            self._parse()
        self.print("</dx-my-type>")

    def print(self, s: str):
        print(s, end="")

    def _print_opening_tag(self):
        if self.open:
            self.print(">\n")

        self.open = True
        self.print(f"<dxo-{self.tags[-1]}")

    def _print_closing_tag(self):
        if self.open:
            self.print(">\n")

        self.open = False
        if len(self.tags):
            tag = self.tags.pop()
            self.print(f"</dxo-{tag}>\n")

            if self.array and self.depth == 0:
                self.tags.append(tag)

    def _parse(self):
        c = self.root[0]
        while c.isspace():
            self.root = self.root[1:]
            if not self.root:
                return

            c = self.root[0]

        if c == "{":
            self.root = self.root[1:]
            self.mode = ParseMode.KEY
            if self.array and self.depth == 0:
                self._print_opening_tag()
            self.depth += 1
        elif c == "}":
            self.depth -= 1
            self._print_closing_tag()
            self.root = self.root[1:]
        elif c == "[":
            self.root = self.root[1:]
            self.mode = ParseMode.KEY
            self.array = True
            self.depth = 0
        elif c == "]":
            self.root = self.root[1:]
            self.array = False
            self.tags.pop()
        elif c == "\"":
            string = self._parse_string()
            self.print(f"\"{string}\" ")
        elif c.isalpha():
            variable = self._parse_variable()
            variable = variable.replace("this.", "")
            if self.mode == ParseMode.KEY:
                if self.root[2] == "{":
                    self.tags.append(self._camel_to_kebab(variable))
                    self._print_opening_tag()
                elif self.root[2] == "[":
                    self.tags.append(self._camel_to_kebab(variable))
                    self.array = True
                else:
                    if self.root[2] == "\"":
                        self.print(f" {variable}=")
                    else:
                        self.print(f" [{variable}]=")
            else:
                self.print(f"\"{variable}\" ")
        elif c.isnumeric():
            number = self._parse_number()
            self.print(f"\"{number}\" ")
        elif c == ":":
            self.root = self.root[1:]
            self.mode = ParseMode.VALUE
        elif c == ",":
            self.root = self.root[1:]
            self.mode = ParseMode.KEY
        elif c == ";":
            self.root = self.root[1:]
        else:
            raise Exception("Invalid Character")

    def _remove_array(self):
        while self.root[0] != "]":
            self.root = self.root[1:]

    def _parse_string(self):
        string = ""

        self.root = self.root[1:]

        c = self.root[0]
        while c != "\"":
            string += c
            self.root = self.root[1:]
            c = self.root[0]

        self.root = self.root[1:]

        return string

    def _parse_variable(self):
        variable = ""

        c = self.root[0]
        while c.isalpha() or c == ".":
            variable += c
            self.root = self.root[1:]
            c = self.root[0]

        return variable

    def _parse_number(self):
        string = ""

        c = self.root[0]
        while c.isnumeric():
            string += c
            self.root = self.root[1:]
            c = self.root[0]

        return string

    def _camel_to_kebab(self, camel: str):
        kebab = ""
        while camel:
            c = camel[0]
            if c.islower():
                kebab += c
            else:
                kebab += "-"
                kebab += c.lower()

            camel = camel[1:]

        return kebab


def main():
    parser = Parser(example)
    parser.parse()


main()
