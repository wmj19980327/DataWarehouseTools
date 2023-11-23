from typing import Iterable, List, Any
from MyException import LengthNotMatchToZipException, ElemTypeNotSameException, IndexIllegalException
from collections import Counter


class IteratorFactory:
    def __init__(self, input_iter: Iterable):
        """
        创建迭代器工厂对象, 方便处理迭代器类型的数据
        :param input_iter: 任意迭代器对象
        """
        self.__elem_list = [i for i in input_iter]
        self.__check_if_elem_one_type()
        self.__length = len(self.__elem_list)
        self.__elem_type = self.__get_elem_type()

    def __get_elem_type(self):
        """
        获取元素类型, 仅供内部使用
        :return: 元素类型
        """
        if self.__length == 0:
            return None
        else:
            return type(self.__elem_list[0])

    def __update_all_info(self) -> None:
        """
        更新迭代器工厂对象的所有信息(长度、元素类型)
        :return: None
        """
        self.__length = len(self.__elem_list)
        self.__elem_type = self.__get_elem_type()

    def __check_if_elem_one_type(self) -> None:
        """
        检查迭代器对象中, 元素类型是否保持一致
        :return: None
        """
        check_set = set()
        for elem in self.__elem_list:
            check_set.add(type(elem))
        if len(check_set) != 1:
            raise ElemTypeNotSameException(check_set)

    def if_have_same_elem(self) -> bool:
        """
        检查是否有重复元素
        :return: bool
        """
        return len(self.__elem_list) != len(set(self.__elem_list))

    def get_same_elem(self) -> List[Any]:
        """
        找到哪些元素是有重复值的
        :return: 装有结果的列表
        """
        result_list = []
        # 统计元素出现的次数
        counter = dict(Counter(self.__elem_list))
        for elem, num in counter.items():
            # 过滤出出现次数大于一的列名
            if num > 1:
                result_list.append(elem)
        return result_list

    def locate_elem(self, input_elem) -> List[int]:
        """
        定位元素位置
        :param input_elem: 要被定位的元素值
        :return: 装有位置索引的列表
        """
        result_list = []
        for i, elem in enumerate(self.__elem_list):
            if elem == input_elem:
                result_list.append(i)
        return result_list

    def update_elem(self, index, new_elem) -> None:
        """
        修改指定位置的元素值
        :param index: 位置
        :param new_elem: 新值
        :return: None
        """
        if index < 0:
            raise IndexIllegalException(f"传入的索引位置 {index} 不合法, 不能小于 0 !!!")
        elif index >= self.__length:
            raise IndexIllegalException(
                f"传入的索引位置 {index} 不合法, 不能超过迭代器工厂对象的最大长度 {self.__length} !!!")
        self.__elem_list[index] = new_elem

    def len(self) -> int:
        """
        获取迭代器工厂长度
        :return: 整数
        """
        return self.__length

    def map(self, func, inplace: bool = True):
        """
        实现类似原生 map 的方法
        :param func: lambda 表达式
        :param inplace: 是否原地修改
        :return: 迭代器工厂对象
        """
        result_list = [func(i) for i in self.__elem_list]
        # 是否原地修改
        if inplace:
            self.__elem_list = result_list
            self.__update_all_info()
            return self
        else:
            return IteratorFactory(input_iter=result_list)

    def zip(self, other_iter: Iterable, inplace: bool = True):
        """
        实现类似原生 zip 的方法
        :param other_iter:
        :param inplace:
        :return: 迭代器工厂对象
        """
        result_list = []
        other_list = [i for i in other_iter]
        # 长度不等, 不能 zip
        if len(other_list) != len(self.__elem_list):
            raise LengthNotMatchToZipException
        else:
            # 之前执行过一次 zip 的情况, 此时元素类 list 类型
            if isinstance(self.__elem_list[0], list):
                for i, elem in enumerate(self.__elem_list):
                    elem.append(other_list[i])
                    result_list.append(elem)
            # 之前没有执行过 zip 的情况
            else:
                for i, elem in enumerate(self.__elem_list):
                    result_list.append([elem, other_list[i]])
        # 原地修改
        if inplace:
            self.__elem_list = result_list
            self.__update_all_info()
            return self
        else:
            return IteratorFactory(input_iter=result_list)

    def join(self, delimiter: str) -> str:
        """
        实现类型原生的 join 方法
        :param delimiter: 分隔符
        :return: 字符串
        """
        return f"{delimiter}".join([str(i) for i in self.__elem_list])

    def to_list(self) -> List[Any]:
        """
        转为列表
        :return: 列表
        """
        return self.__elem_list

    def to_set(self) -> set:
        """
        转为集合并去重
        :return: 集合
        """
        return set(self.__elem_list)

    def __str__(self):
        acc = self.__Accumulator(_init_num=-1, _step=1)
        elem_info_str = '\n'.join([f"{acc.move_one_step()}|\t{i}" for i in self.__elem_list])
        return f"""索引\t值
{elem_info_str}
长度: {self.__length}
元素类型: {self.__elem_type}"""

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        self.__index += 1
        if self.__index >= len(self.__elem_list):
            raise StopIteration
        return self.__elem_list[self.__index]

    class __Accumulator:
        def __init__(self, _init_num, _step):
            self.init_num = _init_num
            self.step = _step

        def move_one_step(self):
            self.init_num += self.step
            return self.init_num


if __name__ == '__main__':
    my_list = IteratorFactory([1, 1, 2, 3, 4, 5, 6, 7, 8, 1])
    print(my_list)
    my_list.update_elem(6, 100)
    print(my_list)
