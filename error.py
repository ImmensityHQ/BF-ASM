from dataclasses import dataclass
import sys


@dataclass
class Position:
    filename: str
    lineno: int
    sidx: int
    eidx: int

    def get_line(self) -> str:
        with open(self.filename, "r") as file:
            return file.readlines()[self.lineno]

    def __str__(self) -> str:
        '''Creates a string that shows the line, and an arrow pointing to the sidx'''
        res = self.get_line()
        res += f"{' ' * self.sidx}"
        if self.sidx == self.eidx:
            res += "^"
        else:
            # absolute value just in case, it shouldn't be necessary
            res += "^" + "~" * abs(self.eidx - self.sidx)
        return res


def throw(error_type: str, msg: str, pos: Position) -> None:
    res = f"Error on line {pos.lineno + 1} in file {pos.filename}: "
    res += f"\n{pos.__str__()}\n"
    res += f"{error_type}: {msg}"
    print(res)
    sys.exit()


if __name__ == "__main__":
    pos = Position("test.asm", 0, 0, 23)
    throw("TestError", "This is a test error.", pos)
