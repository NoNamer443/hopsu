"""自研语言Hopsu的解释器

Hopsu：语言解释器
HopsuError：语言报错
"""

import re
from collections.abc import Iterable
from typing import Self

__all__ = ("Hopsu",)
__version__ = "0.8.3"


class HopsuError(Exception):
    """Hopsu语言层面的错误"""

class HopsuStackError(HopsuError):
    """空栈或栈满"""

class HopsuSyntaxError(HopsuError):
    """Hopsu语言层面的语法错误"""


class Hopsu:
    """Hopsu语言的解释器"""

    __slots__ = (
        "__stack",
        "__max_size",
        "__input_buffer",
        "__output_buffer",
        "__weakref__"
    )

    rule: re.Pattern = re.compile(r"([0-9]+|[-+,.()^~?])")
    digit: re.Pattern = re.compile(r"[0-9]+")

    def __init__(self, /, max_size: int = 30000) -> None:
        if  not isinstance(max_size, int):
            raise TypeError(f"max_size must be int, not {type(max_size).__qualname__}")
        if max_size <= 0:
            raise ValueError("max_size <= 0")

        self.__stack = []
        self.__max_size = max_size
        self.__input_buffer: list[int] = []
        self.__output_buffer: list[int] = []

    @property
    def stack(self, /) -> list[int]:
        return self.__stack

    @property
    def max_size(self, /) -> int:
        return self.__max_size

    @property
    def input_buffer(self, /) -> list[int]:
        return self.__input_buffer

    @property
    def output_buffer(self, /) -> list[int]:
        return self.__output_buffer

    def check_match(self, /, tokens: Iterable[str]) -> dict[int, tuple[int, int]]:
        """检查语法，顺便返回转跳表"""
        loop: list[tuple[int, int]] = [] # 记录“(”的索引
        loop_keyword = 0 # 状态机，0未默认值，1为“~”，2为“~ X”
        jump: dict[int, tuple[int, int]] = {} # {转跳前序列: (转跳后序列, 转跳条件)}
        target: None | int = None # 循环条件，为run时转跳提供方便

        for i, token in enumerate(tokens):
            # 确保token有效
            if not self.rule.fullmatch(token):
                raise HopsuSyntaxError(f"{token!r} is not a right token (index {i})")

            # 匹配~ X (
            match loop_keyword:
                case 0 if token == "~":
                    loop_keyword += 1
                case 1 if self.digit.fullmatch(token):
                    # 确保结束条件理论可达成
                    if int(token) > self.max_size:
                        raise HopsuSyntaxError(f"unachievable stack height: {token} (index {i})")
                    target = int(token)
                    loop_keyword += 1
                case 1:
                    raise HopsuSyntaxError(f'it must be a digit after "~" (index {i})')
                case 2 if token == "(":
                    loop_keyword = 0
                    assert target is not None, "" # 确保target不是None，同时让Pylance闭嘴
                    loop.append((i, target))
                case 2:
                    raise HopsuSyntaxError(f'it must be "(" after "~" and a digit (index {i})')

            # 匹配右括号
            match token:
                case ")" if loop:
                    left, target = loop.pop()
                    jump[left] = (i, target)
                    jump[i] = (left, target)
                case ")":
                    raise HopsuSyntaxError(f'unmatched ")" (index {i})')

        # 检查循环结构
        match loop_keyword:
            case 1:
                raise HopsuSyntaxError('it must be a digit after "~" (index -1)')
            case 2:
                raise HopsuSyntaxError('it must be "(" after "~" and a digit (index -1)')
        # 检查括号配对
        if loop:
            raise HopsuSyntaxError(f'unmatched "(" (index {", ".join(map(str, loop))})')

        return jump

    def push(self, /, value: int) -> Self:
        """压栈"""
        if self.max_size and len(self.stack) < self.max_size:
            self.stack.append(value % 256)
        else:
            raise HopsuStackError("stack was full")
        return self

    def pop(self, /) -> int:
        """弹栈"""
        if not self.stack:
            raise HopsuStackError("stack was empty")
        return self.stack.pop()

    def cond_pop(self, /) -> Self:
        """当栈顶为0时弹栈"""
        if self.stack and self.stack[-1] == 0:
            self.pop()
        return self

    def add(self, /) -> Self:
        """弹栈并将现在的栈顶值加上原栈顶值"""
        value = self.pop()
        value += self.pop()
        value %= 256
        self.push(value)
        return self

    def sub(self, /) -> Self:
        """弹栈并将现在的栈顶值减去原栈顶值"""
        value = self.pop()
        value = self.pop() - value
        self.push(value)
        return self

    def input(self, /) -> Self:
        if not self.input_buffer:
            self.show_output() # 清空输出缓冲区
            try:
                self.input_buffer.extend(input().encode())
                self.input_buffer.append(10) # "\n"
            except EOFError:
                self.input_buffer.append(0)

        self.push(self.input_buffer.pop(0))

        return self

    def output(self, /) -> Self:
        """添加到缓冲区"""
        self.output_buffer.append(self.pop())
        if len(self.output_buffer) >= 128:
            self.show_output()
        return self

    def show_output(self, /) -> Self:
        """输出缓冲区，真正的输出"""
        print("".join(map(chr, self.output_buffer)), end="")
        self.output_buffer.clear()
        return self

    def clear_input_buffer(self, /) -> Self:
        self.input_buffer.clear()
        return self

    def run(self, /, code: str) -> None:
        tokens = code.split()
        jump = self.check_match(tokens)
        index = 0
        LENGTH = len(tokens)

        while index < LENGTH:
            token = tokens[index]

            match token:
                # 堆栈
                case _ if self.digit.fullmatch(token):
                    self.push(int(token))
                # 加法
                case "+":
                    self.add()
                # 减法
                case "-":
                    self.sub()
                case "^":
                    self.pop()
                case "?":
                    self.cond_pop()
                case ",":
                    self.input()
                case ".":
                    self.output()
                case "~":
                    index += 1
                case "(":
                    if len(self.stack) == jump[index][1]:
                        index = jump[index][0]
                case ")":
                    if len(self.stack) != jump[index][1]:
                        index = jump[index][0]

            index += 1

        self.show_output()
        self.clear_input_buffer()

    def clear(self, /) -> Self:
        self.input_buffer.clear()
        self.output_buffer.clear()
        self.stack.clear()
        return self


if __name__ == "__main__":
    a = Hopsu()
    a.run("10 33 100 108 114 111 119 32 44 111 108 108 101 72 ~ 0 ( . )")
    a.clear()
    a.run(", 10 - ? ~ 0 ( 22 - . , 10 - ? )")
