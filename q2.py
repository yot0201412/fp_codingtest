# 設問2
# 第1引数　ログファイルパス
# 2第引数　タイムアウト回数

import datetime

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

    def __init__(self, server, status, log_datetime):
        self.server = server
        self.status = status
        self.log_datetime = log_datetime

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

    def output_log(self):
        error_term = self.after_datetime - self.log_datetime if self.is_returned() else None
        error_term_str = error_term.seconds if error_term else '復帰していません'
        return f'日時：{self.log_datetime.strftime("%Y/%m/%d %H:%M:%S")}, サーバアドレス：{self.server}, 故障期間(秒)：{error_term_str}'

def get_server_manager(sm_list, server):
    for sm in sm_list:
        if sm.is_same_server(server):
            return sm

# タイムアウト連続回数のカウントアップ
def timeout_cnt_up(sm_list, server):
    sm = get_server_manager(sm_list, server)
    sm.timeout_cnt_up()

def timeout_reset(sm_list, server):
    sm = get_server_manager(sm_list, server)
    sm.timeout_reset()

def main(file_path, max_timeout_cnt):
    sm_list = []

    with open(file_path) as f:
        line = f.readline()
        while line:
            log_datetime, server, status = scrap_line(line)
            line = f.readline()

            # サーバーごと最初のログ時にServerManagerを作成する
            if not get_server_manager(sm_list, server):
                sm_list.append(ServerManager(server, status, log_datetime))

            sm = get_server_manager(sm_list, server)

            # タイムアウト回数が上限超えたら、更新しない
            if sm.timeout_cnt > max_timeout_cnt and sm.after_datetime != None:
                continue

            # タイムアウトだったらカウントアップ
            if is_timeout_status(status):
                if not sm.is_timeout():
                    sm.status = status
                    sm.log_datetime = log_datetime
                sm.timeout_cnt_up()
            # タイムアウトじゃなかったらリセット,またはタイムアウト回数が規定回数以上なら、復帰日時を保持
            else :
                if sm.timeout_cnt >= max_timeout_cnt and sm.after_datetime == None:
                    sm.after_datetime = log_datetime
                else:
                    sm.timeout_reset()
                    sm.status = status

    timeout_log_list = []
    for sm in sm_list:
        if sm.timeout_cnt >= max_timeout_cnt:
            timeout_log_list.append(sm.output_log())
    return timeout_log_list

if __name__ == "__main__":
    import sys
    timeout_log_list = main(sys.argv[1], int(sys.argv[2]))
    f = open('q2.txt', 'x', encoding='UTF-8')
    for log in timeout_log_list:
        f.write(log)
        f.write("\n")
    f.close()