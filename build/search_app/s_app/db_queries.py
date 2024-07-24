#In questo file sono presenti le query SQL e le funzioni per eseguirle e connettersi al DB.
import mysql.connector
import os

def connetti_db_search_app():
    """
    Funzione per connettersi al db MySQL.

    """
    try:
        p_path="/run/secrets/db_results_up"
        f=open(p_path,"r")
        p=f.read()
        f.close()
        connection = mysql.connector.connect(
        host="db_results",
        database="results_db",
        user="search_app_user",
        password=p,
        )
        return connection
    except mysql.connector.Error as e:
        print(e)
        return "Error:/DBconn"


def esegui_query_select(query, parametri=None):
    """
    Funzione per eseguire una query SELECT sul db.
    """
    conn=connetti_db_search_app()
    try:
        cursore = conn.cursor()
        if parametri is not None:
            cursore.execute(query, parametri)
        else:
            cursore.execute(query)
            risultati = cursore.fetchall()
            cursore.close()
            return risultati
    except mysql.connector.Error as e:
        print(f"Errore durante l'esecuzione della query:",e)
        return "Error:/DBits"
  

def esegui_query_insert(query):
    """
    Funzione per eseguire una query di INSERT.
    """
    conn=connetti_db_search_app()
    try:
        cursore = conn.cursor()
        cursore.execute(query)
        conn.commit()
        inserito_id = cursore.lastrowid
        cursore.close()
        return inserito_id
    except mysql.connector.Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return "Error:/DBiti"


class QueryDB:
    def __init__(self,query=None,website=None,ip=None,dns=None,email=None,ig_link=None,
                 ig_username=None,ig_followers=None,ig_posts=None):
        self.query=query
        self.website=website
        self.ip=ip
        self.dns=dns
        self.email=email
        self.ig_link=ig_link
        self.ig_username=ig_username
        self.ig_followers=ig_followers
        self.ig_posts=ig_posts
        self.table="search_app_results"

    def add_default_to_db(self):
        return f"INSERT INTO {self.table} (query, website, ip, dns, email, ig_link, ig_username, ig_followers, ig_posts) VALUES ('{self.query}','{self.website}','{self.ip}','{self.dns}','{self.email}','{self.ig_link}','{self.ig_username}','{self.ig_followers}','{self.ig_posts}');"
    
    def select_all(self):
        return f"SELECT * FROM {self.table};"
    
    def select_general_info(self):
        return f"SELECT DISTINCT query, website, ip, dns, email, ig_link, ig_username, ig_followers, ig_posts FROM {self.table} WHERE query='{self.query}';"
    



######################## API DB AND QUERY ########################

def connetti_db_api():
    """
    Funzione per connettersi al db MySQL.
    """
    try:
        p_path="/run/secrets/db_api_up"
        f=open(p_path,"r")
        p=f.read()
        f.close()
        connection = mysql.connector.connect(
        host="db_api",
        database="api_db",
        user="user_api",
        password=p,
        )
        return connection
    except mysql.connector.Error as e:
        print(e)
        return "Error:/DBconn"


def esegui_query_select_api(query):
    """
    Funzione per eseguire una query SELECT sul db.
    """
    conn=connetti_db_api()
    try:
        cursore = conn.cursor()
        cursore.execute(query)
        risultati = cursore.fetchall()
        cursore.close()
        conn.close()
        return risultati
    except mysql.connector.Error as e:
        print(f"Errore durante l'esecuzione della query:",e)
        return "Error:/DBits"
  

def esegui_query_insert_api(query):
    """
    Funzione per eseguire una query di INSERT.
    conn: l'oggetto connessione MySQL
    query: la query INSERT INTO da eseguire
    """
    conn=connetti_db_api()
    try:
        cursore = conn.cursor()
        cursore.execute(query)
        conn.commit()
        inserito_id = cursore.lastrowid
        cursore.close()
        conn.close()
        return inserito_id
    except mysql.connector.Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return "Error:/DBiti"


class QuerydbAPI:
    def __init__(self,g_api_k_one=None,g_api_k_two=None,se_ID_one=None,se_ID_two=None,hostio=None):
        if g_api_k_one!=None and g_api_k_two!=None and se_ID_one!=None and se_ID_two!=None and hostio!=None:
            self.g_api_k_one=g_api_k_one
            self.g_api_k_two=g_api_k_two
            self.se_ID_one=se_ID_one
            self.se_ID_two=se_ID_two
            self.hostio=hostio
        self.table="api_tab"

    def add_keys(self):
        return f"INSERT INTO {self.table} (g_api_k_one,g_api_k_two,se_ID_one,se_ID_two,hostio) VALUES ('{self.g_api_k_one}','{self.g_api_k_two}','{self.se_ID_one}','{self.se_ID_two}','{self.hostio}');"
    
    def select_g_key(self,api_key,se_id):
        return f"SELECT {api_key},{se_id} FROM {self.table};"
    
    def select_hostio_api(self):
        return f"SELECT hostio FROM {self.table};"
    
    def select_all_api(self):
        return f"SELECT * FROM {self.table};"