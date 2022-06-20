import sys
sys.path.append("./..")

import pytest
import datetime
from .. import q1

def log_format(datetime_str, server, term):
    return f'日時：{datetime_str}, サーバアドレス：{server}, 故障期間(秒)：{term}'

# タイムアウトしているログがあれば出力される
def test_q1():
    test_list = q1.main("./tests/resources/q1_1.log")
    assert test_list == [log_format("2020/10/19 13:33:24", "10.20.30.1/16", "1")]

# タイムアウト後一度も故障から明けていない場合
def test_q2():
    test_list = q1.main("./tests/resources/q1_2.log")
    assert test_list == [log_format("2020/10/19 13:33:24", "10.20.30.1/16", "復帰していません")]

# タイムアウトが複数回ある場合
def test_q3():
    test_list = q1.main("./tests/resources/q1_3.log")
    assert test_list == [log_format("2020/10/19 13:33:24", "10.20.30.1/16", "2")]

def test_q1_scrap_line():
    date, ip, status = q1.scrap_line("20201231122000,server,time")
    assert date == datetime.datetime(2020, 12, 31, 12, 20, 00)
    assert ip == "server"
    assert status == "time"

def test_q1_is_timeout_status():
    assert q1.is_timeout_status("-")
    assert not q1.is_timeout_status("22")
