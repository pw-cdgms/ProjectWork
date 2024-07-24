import requests,base64,re,json,os
from variables import search_app_url,config_path,internal_api_key
from string import ascii_lowercase,ascii_uppercase
from random import choice
from secrets import token_bytes



def create_cookie():
    cookie=""
    for i in range (1,32):
        random_char=choice(f"{ascii_lowercase}{ascii_uppercase}0123456789_-")
        cookie+=random_char
    return cookie

def gen_secret():
    t=token_bytes(64)
    secret=base64.b64encode(t).decode()
    return secret


###########################
##### OUTPUT SETTINGS #####
###########################


class Output: #Questa Classe definisce l'output per l'utente.
    def __init__(self,query,website,ip,dns,emails,ig_link,ig_username,ig_followers,ig_posts):
        self.query=query
        self.website=website
        self.ip=ip
        self.dns=dns
        self.emails=emails
        self.ig_link=ig_link
        self.ig_username=ig_username
        self.ig_followers=ig_followers
        self.ig_posts=ig_posts

    def get_emails(self):
        try:
            le=[]
            for i in range(1,len(self.emails)):
                le.append(self.emails[f"email_{i}"])
            return le
        except:
            return []
                

def startSearch(q): #JSON RESULTS
    """
    Questa funzione manda una richiesta di GET all'API interna (ovvero alla search_app)
    La response è in formato JSON.
    """
    try:
        r=requests.get(f"{search_app_url}/search/{q}").json()
        return r
    except:
        return {"Error-server-settings":f"Can't contact the {search_app_url}"}


def get_ui_results(r):
    output=Output(r["search_query"],r["website"],r["ip"],r["dns"],r["emails"],
                  r["instagram"]["ig_link"],r["instagram"]["username"],r["instagram"]["followers"],r["instagram"]["posts"]
                  )
    return output



#####################################
############ API UPLOAD #############
#####################################


def read_and_send_user_API():
    api_file=open(f"{config_path}/api.json")
    user_api=json.load(api_file)
    try:
        r=requests.post(f"{search_app_url}/read_api",data=user_api)
        os.remove(f"{config_path}/api.json")
    except:
        return (False,"no_response")
    if r.status_code==200:
        if r.text=="ok":
            return (True,"ok")
        else:
            return (False,"no")
    else:
        return(False,f"status: {r.status_code}")


def check_api():
    r=requests.get(f"{search_app_url}/check_api").json()
    if r["r"]=="true":
        return True
    elif r["r"]=="false":
        return False
    elif r["r"]=="no-internal-api-key-provided":
        return False
    #check=open(f"{config_path}/check.txt").read()
    #if "1" in check:
    #    return True
    #else:
    #     return False
    

def sanitize_input(input_string):
    sanitized_string = re.sub(r'\"|;|<|>|\'|#|-|=', ' ', input_string)
    return sanitized_string.lower()