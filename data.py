import bs4 
import requests
import json
token="822912f842ab681267fbb304bba55085"

#from minilecture for webscraping
def pullText(link):
    request=requests.get(link)
    soup=bs4.BeautifulSoup(request.text,"html.parser")
    paragraphs=soup.find_all("p")
    article=""
    for paragraph in paragraphs:
        article=article+paragraph.get_text()+"\n"
    return article

def getRestaurantData():
    EXAMPLE_URL = 'https://www.viator.com/Los-Angeles-tours/Dinner-Product-Food-Wine-and-Nightlife/d645-tag21579'

    request=requests.get(EXAMPLE_URL)
    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    res={}
    names = soup.select('div > div.col-6.col-md-6.px-0.pl-3.pr-md-1.d-flex.flex-column.justify-content-md-between > div.flex-md-1.d-flex.flex-column > h2 > a')
    prices = soup.select('div > div.col-md-2.d-none.d-md-flex.flex-column.align-items-end.px-0 > div > div > div >div.h3.line-height-same.mb-0.price-font.text-md-right')
    for i in range(len(names)):
        name = names[i]
        price = prices[i]
        res[name.text]=price.text[1:-3]
    return res

#https://travelpayouts.github.io/slate/?python#cheapest-tickets
#cheapest ticket search
#date is YYYY-MM-DD or YYYY-MM
def cheapestFlight(departureAirport,arrivalAirport,departureDate,arrivalDate):
    url = "https://api.travelpayouts.com/v1/prices/cheap"
    querystring = {"origin":departureAirport,"destination":arrivalAirport,
    "depart_date":departureDate,"return_date":arrivalDate, "currency":"USD"}
    headers = {'x-access-token': token}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.text

#one way flight (business or older people)
#https://travelpayouts.github.io/slate/?python#non-stop-tickets
#date is YYYY-MM-DD or YYYY-MM form
def oneWayFlight(departureAirport,arrivalAirport,departureDate,arrivalDate):
    url = "https://api.travelpayouts.com/v1/prices/direct"
    querystring = {"origin":departureAirport,"destination":arrivalAirport,"depart_date"\
                :departureDate,"return_date":arrivalDate, "currency":"USD"}
    headers = {'x-access-token': token}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.text

#search for hotels
#adapted from
# https://travelpayouts.github.io/slate/?py
# thon#hotel-search-by-name-or-location
#i want this to return hotelID
def searchHotels():
    url = "http://engine.hotellook.com/api/v2/lookup.json"
    querystring = {"query":"huntington beach","lang":"en"
                    ,"lookFor":"both","limit":"10","token":token}
    header={'x-access-token': '822912f842ab681267fbb304bba55085'}
    response = requests.request("GET", url, headers=header, params=querystring)
    return json.loads(response.text)

#finds hotel price
#adapted from https://travelpayouts.github.io/slate/?pyth
# on#displays-the-cost-of-living-in-hotels
def hotelPrice():
    url = "http://engine.hotellook.com/api/v2/cache.json"
    querystring = {"location":"Saint-Petersburg","hotelId":"277083","checkIn":"2019-09-13"
    ,"checkOut":"2019-09-18","currency": "USD", "limit": "1", "token":token}
    headers={'x-access-token': token}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.text

