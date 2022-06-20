import sys
sys.path.append("./..")

import pytest
from .. import q2

def log_format(datetime_str, server, term):
    return f'日時：{datetime_str}, サーバアドレス：{server}, 故障期間(秒)：{term}'

# 連続でタイムアウトするとログに出力される(4以上が設定されると出力されない)
def test_q2_1():
    test_list = q2.main("./test/resources/q2_1.log", 1)
    print(test_list)
    assert test_list == [log_format("2020/10/19 13:33:24", "10.20.30.1/16", "1")]

    test_list = q2.main("./test/resources/q2_1.log", 3)
    assert test_list == [log_format("2020/10/19 13:33:24", "10.20.30.1/16", "1")]

    test_list = q2.main("./test/resources/q2_1.log", 4)
    assert test_list == []

# 連続タイムアウトが一度途切れる
def test_q2_2():
    test_list = q2.main("./test/resources/q2_2.log", 1)
    assert test_list == [log_format("2020/10/19 13:33:24", "10.20.30.1/16", "1")]

    test_list = q2.main("./test/resources/q2_2.log", 2)
    assert test_list == [log_format("2020/10/19 13:33:26", "10.20.30.1/16", "3")]