# 設問1
# 第一引数　ログファイルパス

import datetime

def scrap_line(line):
    date_str, ip, status = line.rstrip("\n").split(",")
    return str_to_date(date_str), ip, status

def is_timeout_status(status):
    return status == "-"

def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y%m%d%H%M%S')

class ServerManager():
    server = None
    status = None
    log_datetime = None
    after_datetime = None

    def __init__(self, server, status, log_datetime):
        self.server = server
        self.status = status
        self.log_datetime = log_datetime

    def is_error(self):
        return is_timeout_status(self.status)

    def is_same_server(self, server):
        return self.server == server

    def is_returned(self):
        return self.after_datetime != None

    def output_log(self):
        error_term = self.after_datetime - self.log_datetime if self.is_returned() else None
        error_term_str = error_term.seconds if error_term else '復帰していません'
        return f'日時：{self.log_datetime.strftime("%Y/%m/%d %H:%M:%S")}, サーバアドレス：{self.server}, 故障期間(秒)：{error_term_str}'

def main(file_path):
    sm_list = []
    error_server_set = set()
    with open(file_path) as f:
        line = f.readline()
        while line:
            log_datetime, server, status = scrap_line(line)
            # サーバーごと最初のエラー時にServerManagerを作成する
            if is_timeout_status(status) and server not in error_server_set:
                error_server_set.add(server)
                sm_list.append(ServerManager(server, status, log_datetime))

            # エラーが起きたサーバーの復帰時間を取得する
            if not is_timeout_status(status) and server in error_server_set:
                for sm in sm_list:
                    if sm.is_same_server(server) and sm.after_datetime == None:
                        sm.after_datetime = log_datetime
            line = f.readline()

    return [ sm.output_log() for sm in sm_list ]

if __name__ == "__main__":
    import sys
    timeout_log_list = main(sys.argv[1])
    f = open('q2.txt', 'x', encoding='UTF-8')
    for log in timeout_log_list:
        f.write(log)
        f.write("\n")
    f.close()
