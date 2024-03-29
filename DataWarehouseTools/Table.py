from typing import List
from MyDataStructure import IteratorFactory
from MyException import SqlTypeNotSupportException, MissImportantTableInfoException, \
    TableColumnNameCanNotBeSameException
from SmallTools import get_today


class Column:
    def __init__(self,
                 _column_name_list: List[str],
                 _column_type_list: List[str] = None,
                 _column_comment_list: List[str] = None
                 ):
        """
        创建一个列对象
        :param _column_name_list: 列名列表
        :param _column_type_list: 列类型列表
        :param _column_comment_list: 列注释列表
        """
        self.column_name_list = _column_name_list
        self.column_type_list = _column_type_list
        self.column_comment_list = _column_comment_list
        self.check_if_same_column_name()

    def check_if_same_column_name(self) -> None:
        column_name_if = IteratorFactory(self.column_name_list)
        if column_name_if.if_have_same_elem():
            raise TableColumnNameCanNotBeSameException()


class Table:
    def __init__(self,
                 _table_name: str,
                 _schema_name: str = "",
                 _column: Column = None,
                 _table_comment: str = "",
                 _delimiter: str = "|",
                 _file_type: str = "textFile"):
        """
        创建一个表对象
        :param _schema_name: 数据库名
        :param _table_name: 表名
        :param _column: 列信息对象
        :param _table_comment: 表注释
        :param _delimiter: 分隔符(hive独有)
        :param _file_type: 文件类型(hive独有)
        """
        self.schema_name = _schema_name
        self.table_name = _table_name
        self.column = _column
        self.table_comment = _table_comment
        self.delimiter = _delimiter
        self.file_type = _file_type

    def if_add_dot(self) -> str:
        return "" if self.schema_name == "" else "."


class SqlTools:
    @staticmethod
    def generate_sql_create_table(table: Table, sql_type: str):
        result_str = []
        if sql_type not in ['hive', 'pg']:
            raise SqlTypeNotSupportException(_sql_type=sql_type)
        elif table.column is None:
            raise MissImportantTableInfoException("生成建表语句时确实了重要的表信息, 列名未知 !!!")
        elif sql_type == 'hive':
            # 拼接出列信息
            column_info_iter = IteratorFactory(input_iter=table.column.column_name_list)
            column_info_iter.zip(other_iter=table.column.column_type_list)
            column_info_iter.zip(other_iter=table.column.column_comment_list)
            column_info_iter.map(lambda elem: f"\t{elem[0]}\t{elem[1]}\tCOMMENT '{elem[2]}'")
            column_info_str = column_info_iter.join(delimiter=",\n")
            result_str = f"""CREATE TABLE IF NOT EXISTS {table.schema_name}{table.if_add_dot()}{table.table_name} (
{column_info_str}
) COMMENT '{table.table_comment}'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '{table.delimiter}'
STORED AS {table.file_type}
;"""
        elif sql_type == 'pg':
            # 拼接出列信息
            column_info_iter = IteratorFactory(input_iter=table.column.column_name_list)
            column_info_iter.zip(other_iter=table.column.column_type_list)
            column_info_iter.map(lambda elem: f"\t{elem[0]}\t{elem[1]}")
            column_info_str = column_info_iter.join(delimiter=",\n")
            # 拼接出列注释信息
            column_comment_iter = IteratorFactory(input_iter=table.column.column_name_list)
            column_comment_iter.zip(other_iter=table.column.column_comment_list)
            column_comment_iter.map(
                lambda elem: f"COMMENT ON COLUMN {table.schema_name}{table.if_add_dot()}" +
                             f"{table.table_name}.{elem[0]} IS '{elem[1]}';"
            )
            column_comment_str = column_comment_iter.join('\n')
            result_str = f"""CREATE TABLE IF NOT EXISTS {table.schema_name}{table.if_add_dot()}{table.table_name} (
{column_info_str}
);
COMMENT ON TABLE {table.schema_name}{table.if_add_dot()}{table.table_name} IS '{table.table_comment}';
{column_comment_str}"""
        return result_str

    @staticmethod
    def generate_sql_lazy_select_insert(source_table: Table, target_table: Table, if_overwrite: bool = True):
        """
        生成 INSERT + SELECT * 语句
        :param source_table: 来源表
        :param target_table: 目标表
        :param if_overwrite: 是否覆盖插入
        :return: sql
        """
        return f"""INSERT {"OVERWRITE TABLE" if if_overwrite else "INTO"} {target_table.schema_name}{target_table.if_add_dot()}{target_table.table_name}
SELECT * FROM {source_table.schema_name}{source_table.if_add_dot()}{source_table.table_name};"""

    @staticmethod
    def generate_comment_basic(source_table: Table, target_table: Table, author: str,
                               if_have_other: bool = False) -> str:
        """
        生成基础注释
        :param source_table: 来源表
        :param target_table: 目标表
        :param author: 作者
        :param if_have_other: 是否还有其他注释信息
        :return: 注释字符串
        """
        result_str = f"""-- {'*'*70} --
-- 作者: {author}
-- 创建时间: {get_today()}
-- 目标表: {target_table.schema_name}{target_table.if_add_dot()}{target_table.table_name}
-- 来源表: {source_table.schema_name}{source_table.if_add_dot()}{source_table.table_name}
$other$
-- {'*'*70} --"""
        if if_have_other:
            return result_str
        else:
            return result_str.replace("\n$other$", "")


if __name__ == '__main__':
    pass
