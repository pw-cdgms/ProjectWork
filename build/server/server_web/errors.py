
def api_keys_db_upload():
    return "Errore: caricamento API nel database fallito. Riprovare."

def cant_contact_search_app():
    return "Errore: impossibile contattare la search app interna. Riprova"

def bad_status_code(status_code):
    return f"Errore di stato {status_code}: impossibile contattare la risorsa."


def no_api_provided():
    return "ATTENZIONE: Non hai caricato nessuna API."