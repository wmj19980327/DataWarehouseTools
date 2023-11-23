from datetime import datetime
from typing import Iterable, List


def get_today() -> str:
    """
    获取今天的日期
    :return: 日期字符串
    """
    return str(datetime.today().date())


def save_as_file(path: str, content: str, mode: str = 'w', encoding: str = 'utf8') -> None:
    """
    将字符串内容保存到文件
    :param path: 文件路径
    :param content: 写入内容
    :param mode: 追加还是覆盖
    :param encoding: 编码类型
    :return: None
    """
    with open(file=path, mode=mode, encoding=encoding) as f:
        f.write(content)


def print_iter_with_index(input_iter: Iterable):
    for i, elem in enumerate(input_iter):
        print(f"{i}.{elem}")


def print_iter(input_iter: Iterable):
    for elem in input_iter:
        print(f"{elem}")


def remove_all_symbol(input_str: str) -> str:
    """
    去除常见的中英文标点符号
    :param input_str: 要被去除标点的字符串
    :return: 去除标点后的字符串
    """
    return input_str.replace('_', "").replace("(", "").replace(")", "")


def split_num_letter_chinese_character(input_str: str) -> List[str]:
    """
    分离字符串中的数字、字母、汉字
    :param input_str: 字符串
    :return: 分离后装有字符串的列表
    """
    temp_str = ""  # 用来存放中间临时字符串的变量
    result_list = []
    flag_list = []  # 用来标记这个位置是汉字、字母还是数字
    # 标记每个位置上的是汉字、字母还是数字
    for elem in input_str:
        if elem in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            flag_list.append(0)
        elif elem in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                      't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                      'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
            flag_list.append(1)
        else:
            flag_list.append(2)
    # 利用标记分离汉字、字母和数字
    for i in range(len(flag_list)):
        if i + 1 == len(flag_list):
            temp_str += input_str[i]
            result_list.append(temp_str)
            break
        elif flag_list[i] == flag_list[i + 1]:
            temp_str += input_str[i]
        elif flag_list[i] != flag_list[i + 1]:
            temp_str += input_str[i]
            result_list.append(temp_str)
            temp_str = ""
    return result_list


def if_have_num(input_str: str) -> bool:
    """
    判断字符串里是否包含数字
    :param input_str: 字符串
    :return: bool
    """
    for elem in input_str:
        if elem in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return True
    else:
        return False


def if_have_letter(input_str: str) -> bool:
    """
    判断字符串里是否包含英文字母
    :param input_str: 字符串
    :return: bool
    """
    for elem in input_str:
        if elem in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
            return True
    else:
        return False


def remove_all_num(input_str: str) -> str:
    """
    去除字符串中的所有数字
    :param input_str: 字符串
    :return: 去除后的字符串
    """
    return (input_str.replace("0", "").replace("1", "").replace("2", "")
            .replace("3", "").replace("4", "").replace("5", "")
            .replace("6", "").replace("7", "").replace("8", "")
            .replace("9", ""))


class Accumulator:
    def __init__(self, _init_num: int, _step: int):
        """
        累加器对象
        :param _init_num: 初始数值
        :param _step: 步长
        """
        self.num = _init_num,
        self.step = _step

    def move_one_step(self) -> int:
        """
        累加一个步长
        :return: 累加一次后的值
        """
        self.num += self.step
        return int(self.num)


if __name__ == '__main__':
    print(split_num_letter_chinese_character('吴铭杰12a3d34rrr4rt5t5t5t5'))
