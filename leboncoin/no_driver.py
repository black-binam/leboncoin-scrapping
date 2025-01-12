import time
import nodriver as uc
from nodriver import cdp
import json
from random import randint

requests_id =[]
visited = []

pages_to_visit = []
rank_pages_to_visit = set()

def listen_network(tab):
    """
    Listen to network events
    Must come just after the tab creation
    Even if you change to another page, the handler will still be active
    handler is a callback function that will be called each time a network event is triggered
    """
    async def handler(event: cdp.network.ResponseReceived):
        if event.type_ == cdp.network.ResourceType.FETCH and '/search' in event.response.url: 
            req_id = event.request_id
            # requests_id is an empty list that will contain
            # request_id for each request made by the browser
            global requests_id 
            requests_id.append(req_id)
            
            
            #print(event.response.url, req_id)
    tab.add_handler(cdp.network.ResponseReceived, handler)

async def get_requests(tab, requests_id, visited):
    """
    This function run through all the requests made by the browser then
    use the 
    :await tab.send(cdp.network.get_response_body(req)) to grab the request body data
    it returns a tuple. First is the body request data, second is false or true 
    i've forgotten what false or true is for.
    
    """
    # got to wait until the tab is ready
    await tab
    for req in requests_id:
        if req not in visited:
            visited.append(req)
            res = await tab.send(cdp.network.get_response_body(req))
            if res is not None and 'ads' in res[0]:
               
                response_body = res[0].replace("false", "False").replace("true", "True").replace("null", "None")
                response_body = eval(response_body)
                #print(response_body)
                return response_body

async def get_all_pages(tab, pages_to_visit):
    """
    this function captures all pages link in the pagination.
    i choosed this option because each time clicking on the > (next) the request log
    get refreshed wheareas clicking on each link don't.
    For sure in nodriver must be option where we can preserve the log.
    """
    await tab
    global rank_pages_to_visit
    pages = await tab.query_selector_all("a[data-index]")
    
    for page in pages_to_visit:
        rank_pages_to_visit.add(page["data-index"])

    for page in pages:
        if page["data-index"] not in rank_pages_to_visit:
            pages_to_visit.append(page)

    return pages_to_visit

def save_data(data):
    with open("scrape_lbc.txt", 'r') as document:
        file = document.read()
        try:
            file = json.loads(file)
        except:
            file = []
    if isinstance(data, dict) == True:
        file.append(data)
        
    #print("-------",type(file))

    with open("scrape_lbc.txt", 'w') as document:
        try:
            document.write(json.dumps(file, indent = 4 ))
        except Exception as ex:
            print(ex)
        


async def main():
    site ="https://www.leboncoin.fr/recherche?category=9&locations=Le%20Bourget_93350__48.93346_2.42323_1605_1000"
    global pages_to_visit

    browser = await uc.start()
    tab =  browser.main_tab
  
    tab.add_handler(cdp.network.Headers, get_requests)
    listen_network(tab)
    

    tab = await browser.get(site)
    time.sleep(10)
    pages_to_visit = await get_all_pages(tab, pages_to_visit)
    page_rank = 0
    #print(pages_to_visit)


    while True:
        await tab
        #listen_network(tab)
        #print(tab)

        data = await get_requests(tab, requests_id, visited)
        save_data(data)

        #print(requests_id)
        #print("-"*15,"Pages to visit","-"*15)

        time.sleep(5)

        try:
            await pages_to_visit[page_rank].click()
        except:
            pages_to_visit = await get_all_pages(tab, pages_to_visit)
            try:
                await pages_to_visit[page_rank].click()
            except:
                return "No more pages to visit"

        page_rank += 1
        time.sleep(randint(10, 30))
        

if __name__ == "__main__":
    uc.loop().run_until_complete(main())