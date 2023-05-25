import dataclasses
import re

class String:
    def __init__(self, string:any):
        if type(string) is not str:
            string = str(string)
        self.string:str = string
    def end_with(self, var:str) -> bool:
        return self.string.endswith(var)
    def __str__(self) -> str:
        return self.string
    def replaceAll(self, bereplaced:str, replace: str) -> str:
        self.string = self.string.replace(bereplaced, replace)
        return self.string
    def replaceFirst(self, pattern, replacement) -> str:
        self.string = re.sub(pattern, replacement, self.string, count=1)
        return self.string
    def replaceEnd(self, pattern, replacement) -> str:
        self.string = re.sub(pattern + '$', replacement, self.string)
        return self.string
    def count(self, c: str) -> int:
        return self.string.count(c)
    def replaceAt(self, index: int, bereplaced: str, replace: str) -> str:
        pattern = re.escape(bereplaced)
        count = 0
        def replace_match(match):
            nonlocal count
            count += 1
            if count == index:
                return replace
            else:
                return match.group()
        self.string = re.sub(pattern, replace_match, self.string, count=index)
        return self.string
    def has_digits(self) -> bool:
        return any(char.isdigit() for char in self.string)
    def spilit(self, sp: str) -> str:
        self.string = sp.join(self.string.split(sp))
        return self.string
    def __setattr__(self, name, value):
        if name == 'string':
            # 如果赋值给 '_str' 属性，则直接赋值给内部存储的字符串变量
            value = str(value)
            object.__setattr__(self, 'string', value)
        else:
            # 对于其他属性的赋值，保持默认行为
            object.__setattr__(self, name, value)
    def __add__(self, value):
        if isinstance(value, str):
            self.string = self.string + value
            return self
        elif isinstance(value, String):
            self.string = self.string + value.string
            return self
        raise TypeError("Unsupported operand type: +")