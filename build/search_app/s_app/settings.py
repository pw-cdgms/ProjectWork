import requests,re
from bs4 import BeautifulSoup
from variables import header,g_apiurl
import db_queries,handle_api


def sanitize_input(user_input):
    sanitized_input = user_input.replace("'", "''")
    sanitized_input = re.sub(r"[^\w\s]", "", sanitized_input)
    return sanitized_input



def siteByGsearch(search_query,info=None):
    if info==None:
        gapi=handle_api.get_g_api("g_api_k_one","se_ID_one")  # Google API
        apik=gapi[0][0]
        seid=gapi[0][1]  # Google APP ID
    elif info=="newapi":
        gapi=handle_api.get_g_api("g_api_k_two","se_ID_two")  # Google API
        apik=gapi[0][0]
        seid=gapi[0][1]  # Google APP ID2
    params={
            "q": search_query,
            "key":apik,
            "cx":seid,
            "lr": "lang_it",
            "gl" :"IT"
        }
    try:
        response=requests.get(g_apiurl,params=params).json()["items"]
    except:
        return ""
    
    return response[0]["link"]#,response[1]["link"],response[2]["link"],response[3]["link"],response[4]["link"],response[5]["link"])


def ipByHostio(dns):
    token=handle_api.get_hostio_api()[0][0]
    api_url=f"https://host.io/api/dns/{dns}?token={token}"
    response=requests.get(api_url).json()
    ip=response['a'][0]
    return ip


def get_dns_by_site(site):
    content1=site.replace("https://","")
    content2=content1.replace("http://","")
    content3=content2.replace("www.","")
    dns=content3.replace("/","")
    return dns


def scrape_emails(url):
    response = requests.get(url,headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    emails_found = []
    for tag in soup.find_all('a'):
        href = tag.get('href')
        try:
            if 'mailto:' in href:
                emails_found.append(href.replace('mailto:', ''))
        except: pass
    for tag in soup.find_all('p'):
        text = tag.text
        for match in re.finditer(r"[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,3}", text):
            emails_found.append(match.group(0))
    emails=[]
    email_check=[]
    i=0
    for email in emails_found:
        i+=1
        if email not in email_check:
            email_check.append(email)
            emails.append(email)# emails è una lista di tuple che verrà poi trasformata in un dizionario nella funzione 'GetGeneralInfo()' (tutto in oneline con list comprehension)
        else:
            i-=1
    return emails[0]


def find_instagram_link(url):
    """
    Trova il link al profilo Instagram dal website.
    """
    response = requests.get(url,headers=header)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href and href.startswith("https://www.instagram.com/"):
            return href
    return None


def get_iguser(ig_link):
    u=ig_link.replace("https://www.instagram.com/","")
    username=u.replace("/","")
    return username


def insta_followers_posts(url):
    val=(None,None)
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        follower_count_element = soup.find('meta', {'property': 'og:description'})
        if follower_count_element:
            ig_info=follower_count_element.get("content")
            #print(ig_info)
            followers=ig_info.split(" ")[0]
            posts=ig_info.split(" ")[4]
            try:
                f=int(followers[0])
                p=int(posts[0])
                val=(followers,posts)
            except ValueError:
                return val
            return val
        else:
            return val
    except:
        return val


def internet_search_info(q):
    website=siteByGsearch(q)
    if len(website)<1:
        website=siteByGsearch(q,"newapi")
    dns=get_dns_by_site(website)
    ip=ipByHostio(dns)
    emails=scrape_emails(f"{website}contatti")
    try:
        ig_link=find_instagram_link(f"{website}contatti")
    except:
        ig_link=""
    try:
        ig_user=get_iguser(ig_link)
    except:
        ig_user=""
    try:
        ig_data=insta_followers_posts(ig_link)
    except:
        ig_data=("","")
    general_info={
                "search_query":q,
                "website":website,
                "dns":dns,
                "ip":ip,
                "emails":emails,
                "instagram":{"ig_link":ig_link,"followers":ig_data[0],"posts":ig_data[1],"username":ig_user}
                }
    return (general_info,[q,website,ip,dns,emails,ig_link,ig_user,ig_data[0],ig_data[1]])


def get_db_results(q):
    query_db=db_queries.QueryDB(query=q)
    res=db_queries.esegui_query_select(query_db.select_general_info())
    if len(res)>0:
        general_info={
            "search_query":res[0][0],
            "website":res[0][1],
            "dns":res[0][2],
            "ip":res[0][3],
            "emails":res[0][4],
            "instagram":{"ig_link":res[0][5],"username":res[0][6],"followers":res[0][7],"posts":res[0][8]}
            }
        return general_info
    else: 
        res=""
        return res


def add_info_to_db(info):
    try:
        query_db=db_queries.QueryDB(info[0],info[1],info[3],info[2],info[4],info[5],info[6],info[7],info[8])
        db_queries.esegui_query_insert(query_db.add_default_to_db())
        return True
    except:
        return False



def check_api():
    s=handle_api.get_all_api()
    if len(s)==1:
        return True
    else:
        return False