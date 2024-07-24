def error(info=None):
    if info==None:
        pass
    elif info=="no_res":
        err={"Error":"/search"}
    elif info=="nor_res_db":
        err={"Error:/search_onlY_db":"No result for this query."}
    elif info=="insert_failed":
        err={"Error":"/search01"}
    return err