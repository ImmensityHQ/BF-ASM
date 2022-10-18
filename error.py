from dataclasses import dataclass
import sys


@dataclass
class Position:
    filename: str
    lineno: int
    sidx: int
    eidx: int

    def get_line(self):
        with open(self.filename, "r") as file:
            return file.readlines()[self.lineno]

    def get_pointer_str(self):
        '''Creates a string that shows the line, and an arrow pointing to the sidx'''
        res = self.get_line()
        res += f"{' ' * self.sidx}^"
        return res


def throw(error_type: str, msg: str, pos: Position) -> None:
    res = f"Error on line {pos.lineno} in file {pos.filename}: "
    res += f"\n{pos.get_pointer_str()}\n"
    res += f"{error_type}: {msg}"
    print(res)
    sys.exit()


if __name__ == "__main__":
    pos = Position("test.asm", 0, 1, 3)
    throw("TestingError", "This is a test error.", pos)
