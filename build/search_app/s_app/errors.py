def error(info=None):
    if info==None:
        pass
    elif info=="no_res":
        err={"Error:/search":"Can't get final results."}
    elif info=="nor_res_db":
        err={"Error:/search_onlY_db":"No result for this query."}
    elif info=="insert_failed":
        err={"Error:/search":"000000001"}
    return err