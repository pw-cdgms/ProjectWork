#Questo file rappresenta una sorta di API interna della nostra applicazione, è come un demone sempre in attesa di una query
# attraverso la quale effettuare le ricerche delle aziende in internet (in settings.)
from flask import Flask, jsonify,request
import settings,handle_api
import errors
from variables import internal_api_key

app=Flask(__name__)

@app.route("/search/<q>",methods=["GET"])  # 'q' è la query di ricerca dell'utente (il nome di un'azienda)
def search(q):
        general_info=settings.get_db_results(q)
        if general_info:
            return general_info
        else:
            try:
                general_info=settings.internet_search_info(q)
                if settings.add_info_to_db(general_info[1]):
                    return jsonify(general_info[0])
                else: 
                    return jsonify(errors.error(info='insert_failed'))  
            except:
                return jsonify(errors.error(info='no_res')) 
        
                

@app.route("/search_only_db/<q>",methods=["GET"])
def search_only_db(q):
    if request.headers.get("API_internal")==internal_api_key:
        general_info=settings.get_db_results(q)
        if general_info:
            return general_info
        else:
            return jsonify(errors.error(info='no_res_db'))
    else:
        return jsonify(errors.error(info='no_res')) 
    


@app.route("/read_api",methods=("POST",))
def read_and_save_api():
    if request.method=="POST":
        g_api_k_one=request.form["g_api_k_one"]
        g_api_k_two=request.form["g_api_k_two"]
        se_ID_one=request.form["se_ID_one"]
        se_ID_two=request.form["se_ID_two"]
        hostio=request.form["hostio"]
        if handle_api.add_api_from_input(g_api_k_one,g_api_k_two,se_ID_one,se_ID_two,hostio):
            print("OK")
            return "ok"
        else:
            return "no"
    else:
        return "M N A: Method Not Allowed"


@app.route("/check_api",methods=("GET",))
def check_Api():
    if settings.check_api():
        return jsonify({"r":"true"})
    else:
        return jsonify({"r":"false"})

    


if __name__=="__main__":
    app.run("0.0.0.0",9091)