import sys
sys.path.append("./..")

import pytest
import datetime
from .. import q4

def log_format(datetime_str, server, term):
    return f'日時：{datetime_str}, サブネット：{server}, 故障期間(秒)：{term}'

# 連続でタイムアウトするとログに出力される(4以上が設定されると出力されない)
def test_q4_1():
    test_list = q4.main("./tests/resources/q4_1.log", 1)
    assert test_list == [log_format("2020/10/19 13:33:24", "16", "3")]

    test_list = q4.main("./tests/resources/q4_1.log", 2)
    assert test_list == [log_format("2020/10/19 13:33:24", "16", "3")]

    test_list = q4.main("./tests/resources/q4_1.log", 3)
    assert test_list == [log_format("2020/10/19 13:33:24", "16", "3")]

    test_list = q4.main("./tests/resources/q4_1.log", 4)
    assert test_list == []

# 同じサブネットで2回該当のパターンがあった場合、一回目のみ表示
def test_q4_2():
    test_list = q4.main("./tests/resources/q4_2.log", 1)
    assert test_list == [log_format("2020/10/19 13:33:24", "16", "2")]

# 複数サブネットを表示
def test_q4_3():
    test_list = q4.main("./tests/resources/q4_3.log", 1)
    assert test_list == [log_format("2020/10/19 13:33:24", "16", "2"), log_format("2020/10/19 13:33:28", "24", "復帰していません")]

def test_q4_subnet_name_1():
    test_str = q4.subnet_name("11.111.111/22")
    assert test_str == "22"

    test_str = q4.subnet_name("11.111.111")
    assert test_str == ""

def test_q4_scrap_line():
    date, ip, status = q4.scrap_line("20201231122000,server,time")
    assert date == datetime.datetime(2020, 12, 31, 12, 20, 00)
    assert ip == "server"
    assert status == "time"

def test_q4_is_timeout_status():
    assert q4.is_timeout_status("-")
    assert not q4.is_timeout_status("22")
