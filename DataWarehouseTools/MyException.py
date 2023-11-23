from typing import Iterable


class LengthNotMatchToZipException(Exception):
    def __init__(self, _len1: int, _len2: int):
        self.len1 = _len1
        self.len2 = _len2

    def __str__(self):
        return f"传入的迭代器对象和迭代器工厂对象长度不匹配({self.len1}≠{self.len2}), 不能进行 zip !!!"


class ElemTypeNotSameException(Exception):
    def __init__(self, _type_iter: Iterable):
        self.type_iter = _type_iter

    def __str__(self):
        return f"迭代器工厂对象中元素存在不一样的类型{self.type_iter} !!!"


class IndexIllegalException(Exception):
    def __init__(self, _content: str):
        self.content = _content

    def __str__(self):
        return self.content


class SqlTypeNotSupportException(Exception):
    def __init__(self, _sql_type):
        self.sql_type = _sql_type

    def __str__(self):
        return f"不支持 {self.sql_type} 这种类型的 sql 语法 !!!"


class MissImportantTableInfoException(Exception):
    def __init__(self, _context: str):
        self.context = _context

    def __str__(self):
        return self.context


class TableColumnNameCanNotBeSameException(Exception):
    def __str__(self):
        return f"表的列名不可以存在重复值 !!!"
