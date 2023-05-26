from dataclasses import dataclass
from enum import Enum
import json
from str_util import String
import pymysql

class sql_status(Enum):
    unconnected = 1
    disconnected = 2
    connected = 3
class commitStatus(Enum):
    manual_commit = 0  # 开启事务了
    auto_commit = 1 # 自动提交模式(default)
'''
 数据库工具类
'''

@dataclass
class basic_db:
    def __init__(self,host:str|None = None,port:int|None = None,user:str|None = None,password:str|None=None,charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        self.connection:pymysql.connections.Connection | None = None
        super(basic_db,self)

    @classmethod
    def getInstance(cls,connect: pymysql.connections.Connection | None = None, *, host:str = None, port:int = None,
                    user:str = None, password:str = None,charset:str = 'utf8') -> 'basic_db | None':
        if connect is not None:
            return cls(connect.host,connect.port,connect.user,connect.password,connect.charset)
        if host and port and user and password:
            return cls(host,port,user,password,charset)
        else:
            return None

    #return basic_db(connect.host,connect.port,connect.user,connect.password,connect.charset)


    def connect_mysql_server(self,commit_status:commitStatus = commitStatus.manual_commit):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                charset=self.charset,
                autocommit=commit_status.value
            )
        except pymysql.Error as e:
            print("数据库连接失败 Exception:")
            raise
    '''事务状态 默认:Auto-Commit '''
    def setup(self,db_name:str,is_start_transaction:bool = False) -> None:
        self.connect_database(db_name)
        if is_start_transaction:
            self.startTransAction()

    def connect_database(self,db_name:str) -> None:
        try:
            if not self.is_database_exists(db_name):
                self.create_database(db_name)
                print(f"检测到库不存在,已创建库[{db_name}]!")
            self.connection.select_db(db_name)
        except pymysql.err.OperationalError as e:
            print(f"连接库{db_name}失败: ")
            raise
    def disconnect_mysql_server(self):
        if self.connect_status.value == sql_status.connected.value:
            self.connection.close()
            self.connection = None

    def excuse_command(self,cmd:str) -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute(cmd)
        except Exception as e:
            print("执行数据库命令发生错误: ")
            raise
    @property
    def Commit_status(self) -> commitStatus:
        cursor = self.connection.cursor()
        cursor.execute("select @@autocommit")
        result = cursor.fetchall()[0][0]
        if result == 1:
            return commitStatus.auto_commit
        if result == 0:
            return commitStatus.manual_commit
    def data_to_list(self,data:str) -> list[str]:
        return eval(data)
    def data_to_list2(self,data:str) -> list[str]:
        data = json.loads(data)
        # 将 null 转换为 None
        data = [None if item is None else item for item in data]
        return data

    def set_Commit_Status(self,Commit_status):
        self.excuse_command(f"set autocommit = {Commit_status.value}")
    def startTransAction(self) -> None:
        self.excuse_command("start transaction")
    def Commit(self) -> None:
        self.excuse_command("COMMIT")
    def rollback(self) -> None:
        self.excuse_command("ROLLBACK")
    def execute_sql_language(self, sql_language:str) -> tuple[tuple[any,...],...]:  #返回的是每一行的元素
        try:
            sv = String(sql_language)
            sv.replaceAll("None","NULL")
            cursor = self.connection.cursor()
            try:
                affected_line:int = cursor.execute(sv.string)
                result:tuple[tuple[any],...] = cursor.fetchall()
                return result
            except pymysql.Error as e2:
                print("执行sql语句发生数据库错误: ")
                raise
            finally:
                cursor.close()
        except pymysql.err.ProgrammingError as e:
            print("你还没有选择数据库: ")
            raise
    #返回和服务器的连接状态
    @property
    def connect_status(self) -> sql_status:
        if self.connection is None:
            return sql_status.unconnected
        try:
            self.connection.ping()
            c = self.connection.cursor()
            return sql_status.connected
        except pymysql.Error as e:
            return sql_status.disconnected

    def is_database_exists(self,database_name:str) -> bool:
        cursor = self.connection.cursor()
        query = f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{database_name}'"
        cursor.execute(query)
        result = cursor.fetchone()
        return result is not None

    def create_database(self,database_name:str) -> None:
        cursor = self.connection.cursor()
        query = f"CREATE DATABASE {database_name}"
        cursor.execute(query)

    def is_has_Table(self, tb_name: str) -> bool:
        cursor = self.connection.cursor()
        try:
            # 执行查询表是否存在的语句
            cursor.execute(f"SHOW TABLES LIKE '{tb_name}'")
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            #print("查询表是否存在时发生错误:", e)
            return False
        finally:
            cursor.close()

    def showTables(self) -> list[str]:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            result = cursor.fetchall()
            table_names = [row[0] for row in result]
            return table_names
        except Exception as e:
            print("查询表失败:", e)
            raise
    def is_has_View(self, view_name: str) -> bool:
        cursor = self.connection.cursor()
        try:
            # 执行查询视图是否存在的语句
            cursor.execute(f"SHOW CREATE VIEW {view_name}")
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            #print("查询视图是否存在时发生错误:", e)
            return False
        finally:
            cursor.close()
    def __del__(self):
        try:
            if self.connect_status == sql_status.connected:
                self.disconnect_mysql_server()
        finally:
            ...