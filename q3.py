# 設問2
# 第1引数　ログファイルパス
# 2第引数　タイムアウト回数

import datetime
import numpy as np

def scrap_line(line):
    date_str, ip, status = line.rstrip("\n").split(",")
    return str_to_date(date_str), ip, status

def is_timeout_status(status):
    return status == "-"

def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y%m%d%H%M%S')


class ServerManager():
    timeout_cnt = 0
    server = None
    status = None
    log_datetime = None
    after_datetime = None
    response_time_list = None
    log_datetime_list = None


    def __init__(self, server, status, log_datetime):
        self.server = server
        self.status = status
        self.log_datetime = log_datetime
        self.log_datetime_list = []
        self.response_time_list = np.empty(0, dtype=int)

    def timeout_cnt_up(self):
        self.timeout_cnt += 1
    
    def timeout_reset(self):
        self.timeout_cnt = 0
        self.log_datetime = None
        self.after_datetime = None

    def is_timeout(self):
        return is_timeout_status(self.status)

    def is_same_server(self, server):
        return self.server == server

    def is_returned(self):
        return self.after_datetime != None

    def add_response_time(self, response_time):
        # タイムアウトは999秒として計算
        if is_timeout_status(response_time):
            response_time = "999"
        self.response_time_list = np.append(self.response_time_list, int(response_time))

    def is_overload(self, agg_cnt, deadline_time):
        agg_list = self.response_time_list[-agg_cnt:]
        return agg_list.mean() > deadline_time

    def add_log_datetime(self, log_datetime):
        self.log_datetime_list.append(log_datetime)

    def log_cnt(self):
        return len(self.log_datetime_list)

    def output_log(self):
        error_term = self.after_datetime - self.log_datetime if self.is_returned() else None
        error_term_str = error_term.seconds if error_term else '復帰していません'
        return f'日時：{self.log_datetime.strftime("%Y/%m/%d %H:%M:%S")}, サーバアドレス：{self.server}, 故障期間(秒)：{error_term_str}'

    def output_overload_log(self, agg_cnt):
        dt_list = self.log_datetime_list[-agg_cnt:]
        return f'サーバアドレス：{self.server}, {dt_list[0].strftime("%Y/%m/%d %H:%M:%S")} ~ {dt_list[-1].strftime("%Y/%m/%d %H:%M:%S")}'


def get_server_manager(sm_list, server):
    for sm in sm_list:
        if sm.is_same_server(server):
            return sm



def main(file_path, max_timeout_cnt, agg_cnt, deadline_time):
    sm_list = []
    overload_log_list = []
    with open(file_path) as f:
        line = f.readline()
        while line:
            log_datetime, server, status = scrap_line(line)
            line = f.readline()

            # サーバーごと最初のログ時にServerManagerを作成する
            if not get_server_manager(sm_list, server):
                sm_list.append(ServerManager(server, status, log_datetime))

            sm = get_server_manager(sm_list, server)
            sm.add_response_time(status)
            sm.add_log_datetime(log_datetime)

            if sm.is_overload(agg_cnt, deadline_time) and sm.log_cnt() >= agg_cnt:
                overload_log_list.append(sm.output_overload_log(agg_cnt))  

            # タイムアウト回数が上限超えたら、更新しない
            if sm.timeout_cnt > max_timeout_cnt and sm.after_datetime != None:
                continue

            # エラーだったらカウントアップ
            if is_timeout_status(status):
                if not sm.is_timeout():
                    sm.status = status
                    sm.log_datetime = log_datetime
                sm.timeout_cnt_up()
            # タイムアウトじゃなかったらリセット,またはタイムアウト回数が規定回数以上なら、復帰日時を保持
            else:
                if sm.timeout_cnt >= max_timeout_cnt and sm.after_datetime == None:
                    sm.after_datetime = log_datetime
                else:
                    sm.timeout_reset()
                    sm.status = status
    
    timeout_log_list = []
    for sm in sm_list:
        if sm.timeout_cnt >= max_timeout_cnt:
            timeout_log_list.append(sm.output_log())
    return timeout_log_list, overload_log_list

