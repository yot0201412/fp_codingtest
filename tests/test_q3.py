import sys
sys.path.append("./..")

import pytest
import datetime
import numpy as np
from .. import q3

def log_format(server, datetime_str_before, datetime_str_after):
    return f'サーバアドレス：{server}, {datetime_str_before} ~ {datetime_str_after}'

# 平均応答時間が11ミリ秒以下ならログ無し過負荷状態ではない
def test_q3_1():
    log_list, overload_log_list = q3.main("./tests/resources/q3_1.log", 3, 3, 11)
    assert overload_log_list == [log_format("10.20.30.1/16","2020/10/19 13:33:25", "2020/10/19 13:33:28")]

# 平均応答時間が12ミリ秒以下ならログ無し過負荷状態ではない
def test_q3_2():
    log_list, overload_log_list = q3.main("./tests/resources/q3_1.log", 3, 3, 12)
    assert overload_log_list == []

# 平均応答時間が12ミリ秒以下ならログ無し過負荷状態ではない
def test_q3_3():
    log_list, overload_log_list = q3.main("./tests/resources/q3_1.log", 3, 4, 9)
    assert overload_log_list == [log_format("10.20.30.1/16","2020/10/19 13:33:24", "2020/10/19 13:33:28")]

# 平均応答時間が12ミリ秒以下ならログ無し過負荷状態ではない
def test_q3_4():
    log_list, overload_log_list = q3.main("./tests/resources/q3_1.log", 3, 3, 5)
    assert overload_log_list == [
                                    log_format("10.20.30.1/16","2020/10/19 13:33:24", "2020/10/19 13:33:26"),
                                    log_format("10.20.30.1/16","2020/10/19 13:33:25", "2020/10/19 13:33:28"),
                                ]

def test_q3_scrap_line():
    date, ip, status = q3.scrap_line("20201231122000,server,time")
    assert date == datetime.datetime(2020, 12, 31, 12, 20, 00)
    assert ip == "server"
    assert status == "time"

def test_q3_is_timeout_status():
    assert q3.is_timeout_status("-")
    assert not q3.is_timeout_status("22")

def test_q3_is_overload():
    sm = q3.ServerManager("server", "stete", None)
    sm.response_time_list = np.array([5, 6, 7, 7])
    assert sm.is_overload(3, 6) == True
    assert sm.is_overload(3, 7) == False
    assert sm.is_overload(2, 7) == False
