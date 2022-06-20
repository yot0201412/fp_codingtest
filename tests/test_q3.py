import sys
sys.path.append("./..")

import pytest
from .. import q3

def log_format(server, datetime_str_before, datetime_str_after):
    return f'サーバアドレス：{server}, {datetime_str_before} ~ {datetime_str_after}'

# 平均応答時間が11ミリ秒以下ならログ無し過負荷状態ではない
def test_q3_1():
    log_list, overload_log_list = q3.main("./test/resources/q3_1.log", 3, 3, 11)
    assert overload_log_list == [log_format("10.20.30.1/16","2020/10/19 13:33:25", "2020/10/19 13:33:28")]

# 平均応答時間が12ミリ秒以下ならログ無し過負荷状態ではない
def test_q3_2():
    log_list, overload_log_list = q3.main("./test/resources/q3_1.log", 3, 3, 12)
    assert overload_log_list == []

# 平均応答時間が12ミリ秒以下ならログ無し過負荷状態ではない
def test_q3_3():
    log_list, overload_log_list = q3.main("./test/resources/q3_1.log", 3, 4, 9)
    assert overload_log_list == [log_format("10.20.30.1/16","2020/10/19 13:33:24", "2020/10/19 13:33:28")]

# 平均応答時間が12ミリ秒以下ならログ無し過負荷状態ではない
def test_q3_4():
    log_list, overload_log_list = q3.main("./test/resources/q3_1.log", 3, 3, 5)
    assert overload_log_list == [
                                    log_format("10.20.30.1/16","2020/10/19 13:33:24", "2020/10/19 13:33:26"),
                                    log_format("10.20.30.1/16","2020/10/19 13:33:25", "2020/10/19 13:33:28"),
                                ]
