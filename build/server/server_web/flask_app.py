#Questo è il file delle routes che abbiamo creato. questo file prende di solito il nome di 'views', ma in questo caso
# aiuterà solo a definire la struttura del nostro server web.
# (e anche la gestione delle pagine html, dell'input utente, cookies e molto altro)

from flask import Flask, render_template,redirect,make_response,request
import settings,errors,os
from variables import cookie_name,valid_cookies_value,config_path

app=Flask(__name__)

app.config['SECRET_KEY'] = settings.gen_secret()


@app.route("/")
def index():
    cookie=request.cookies.get(cookie_name)
    if cookie in valid_cookies_value:
        return redirect("/search")
    else:
        cookie_value=settings.create_cookie()
        valid_cookies_value.append(cookie_value)
        response=make_response(redirect("/search"))
        response.set_cookie(cookie_name,cookie_value,secure=True,max_age=24*60*60)
        return response


@app.route("/search",methods=["GET","POST"])
def search():
    cookie=request.cookies.get(cookie_name)
    if cookie in valid_cookies_value:
        if settings.check_api():
            if request.method=="POST":
                qu=request.form["user_input"]    # 'q' è la query (presumibilmente il nome dell'azienda) che vuole cercare l'utente.
                if qu:
                    return redirect(f"/output/{qu}/json")
                else:
                    return redirect("/search")
            else:
                return render_template("index.html")
        else:
            return render_template("index.html",err=errors.no_api_provided())
    else:
        return redirect("/")
        
    
@app.route("/output/<q>")
def output(q):
    if q:
        return "OK"
    else:
        return "NO q"


@app.route("/output/<q>/json")
def output_json(q):

    """
    JSON Results: abbiamo inserito questa route da cui gli "utenti" della webapp 
    potranno accedere direttamente ai risultati in formato JSON (utile per altri script
    python o per uso da terminale con il comando curl, oltre che utile per funzionalità di debug).
    """
    cookie=request.cookies.get(cookie_name)
    if cookie in valid_cookies_value or request.headers.get("API")=="dev_key":
        if q:
            json_results=settings.startSearch(q)
            
            return json_results
        else:
            return redirect("/")
    else:
        return redirect("/")


@app.route("/config",methods=["GET","POST"])
def api_config():
    """
    Questa route serve all'utente per caricare un file json contenente le proprie API keys da inserire nel database.
    Una volta caricato, il file, viene letto, rimosso e il contenuto json viene inviato alla search_app che si occuperà di
    salvare le API keys nel database.
    """
    cookie=request.cookies.get(cookie_name)
    if cookie in valid_cookies_value:
        if settings.check_api():
            return redirect("/")
        else:
            if request.method=="POST":
                file=request.files["api_config_file"]
                if file.filename.endswith(".json"):
                    print("OK")
                    file.save(f"{config_path}/api.json")
                    print("FILE SALVATO")
                    d=settings.read_and_send_user_API()
                    print("search_app response.",d)
                    if d[0]:
                        return render_template("success.html")
                    else:
                        if d[1]=="no":
                            return render_template("api_config.html",err=errors.api_keys_db_upload())
                        elif d[1]=="no_response":
                            return render_template("api_config.html",err=errors.cant_contact_search_app())
                        elif d[1].startswith("status:"):
                            status_code=d[1].replace("status:","")
                            return render_template("api_config.html",err=errors.bad_status_code(status_code))
                else:
                    return render_template("file_error.html")
            else:
                return render_template("api_config.html")
    else:
        return redirect("/")



######################
######################


@app.errorhandler(404) 
def not_found(e): 
  """
  Gestione dell'errore 404 Not Found attraverso il decoratore built in di Flask.
  Lo scopo di questa funzione è solo mostrare una pagina di errore Not Found 404 personalizzata.
  """
  return render_template("404.html")



if __name__=="__main__":
    app.run("0.0.0.0",9090,ssl_context="adhoc")