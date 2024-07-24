from secrets import token_bytes
import base64,sys


def check():
    c=open("./build/db_api/dump.sql","r").read()
    if c.endswith("'user_api'@'%';"):
        return True
    else:
        return False



def gen_secret():
    t=token_bytes(32)
    secret=base64.b64encode(t).decode()
    return secret


if check():
    sys.exit()

paths=[
"./build/db_api/up.txt",
"./build/db_results/up.txt",
"./build/db_api/rp.txt",
"./build/db_results/rp.txt"
]

k=[]

for path in paths:
    s=gen_secret()
    k.append(s)
    f=open(path,"w")
    f.write(s)
    f.close()

sql_path=["./build/db_api/dump.sql","./build/db_results/dump.sql"]

f=open(sql_path[0],"a")
f.write(f"CREATE USER 'user_api'@'%' IDENTIFIED BY '{k[0]}';\nGRANT SELECT, INSERT ON api_tab TO 'user_api'@'%';")
f.close()


f=open(sql_path[1],"a")
f.write(f"CREATE USER 'search_app_user'@'%' IDENTIFIED BY '{k[1]}';\nGRANT SELECT, INSERT ON search_app_results TO 'search_app_user'@'%';")
f.close()