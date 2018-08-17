# 주요 모듈 불러옴
import json
import sqlite3
import threading

# 기타 코드 불러옴
from func import *
from mark import load_conn2, namumark

# JSON 불러옴
json_data = open('set.json').read()
set_data = json.loads(json_data)

# 디비 연결
conn = sqlite3.connect(set_data['db'] + '.db', check_same_thread = False)
curs = conn.cursor()

# 연결 전달
load_conn(conn)

print('1. BackLink ReSet')
print('2. ReCaptcha Delete')
print('3. Ban Delete')

print('select : ', end = '')
what_i_do = input()

if what_i_do == '1':
    # 파싱 해주는 함수
    def parser(data):
        namumark(data[0], data[1], 1)

    # 역링크 전부 삭제
    curs.execute("delete from back")
    conn.commit()

    # 데이터에서 제목이랑 내용 불러옴
    curs.execute("select title, data from data")
    data = curs.fetchall()

    # for 돌려서 처리
    for test in data:
        # 스레드 기반으로 처리
        t = threading.Thread(target = parser, args = [test])
        t.start()
        t.join()
elif what_i_do == '2':
    # 데이터 삭제
    curs.execute("delete from other where name = 'recaptcha'")
    curs.execute("delete from other where name = 'sec_re'")
elif what_i_do == '3':
    print('IP or User_Name : ', end = '')
    user_data = input()

    if re.search("^([0-9]{1,3}\.[0-9]{1,3})$", user_data):
        band = 'O'
    else:
        band = ''

    # 데이터 삭제
    curs.execute("insert into rb (block, end, today, blocker, why, band) values (?, ?, ?, ?, ?, ?)", [user_data, load_lang('release', 1), get_time(), load_lang('tool', 1) + ':Emergency', '', band])
    curs.execute("delete from ban where block = ?", [user_data])

print('OK')

# 커밋
conn.commit()