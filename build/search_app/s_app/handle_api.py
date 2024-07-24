import db_queries

def add_api_from_input(g_api_k_one,g_api_k_two,se_ID_one,se_ID_two,hostio):
    try:
        query_api_db=db_queries.QuerydbAPI(g_api_k_one,g_api_k_two,se_ID_one,se_ID_two,hostio)
        db_queries.esegui_query_insert_api(query_api_db.add_keys())
        return True
    except:
        return False
    
def get_g_api(api,seid):
    try:
        query_api_db=db_queries.QuerydbAPI()
        api_k=db_queries.esegui_query_select_api(query_api_db.select_g_key(api,seid))
        return api_k
    except:
        return None
    
def get_hostio_api():
    try:
        query_api_db=db_queries.QuerydbAPI()
        api_k=db_queries.esegui_query_select_api(query_api_db.select_hostio_api())
        return api_k
    except:
        return None
    
def get_all_api():
    try:
        query=db_queries.QuerydbAPI()
        s=db_queries.esegui_query_select_api(query.select_all_api())
        return s
    except:
        return ""