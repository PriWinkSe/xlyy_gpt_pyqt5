import dataclasses
import json

from src.common_utils.io_util import *
from str_util import String


@dataclasses.dataclass
class SQL_Config:
    host:str
    port:int
    user:str
    password:str

def read_sql_config() -> SQL_Config:
    sc_path:str = get_sql_config_path()
    with open(sc_path) as f:
        config = json.load(f)
        ip = config['ip']
        port = config['port']
        user = config['user']
        password = config['password']
        sql_config = SQL_Config(ip, port, user, password)
        return sql_config
def get_sql_config_path() -> str:
    sql_config_path: str = "/configs/sql_config.json"
    file_dir: String = String(get_last_dir(3))
    sc_path: str = file_dir.replaceAll("\\", "/") + sql_config_path
    return sc_path
def write_sql_config(data:dict):
    json_data = json.dumps(data, indent=1)
    sc_path: str = get_sql_config_path()
    with open(sc_path, 'w') as f:
        f.write(json_data)