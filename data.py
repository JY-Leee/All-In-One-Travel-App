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

def getRestaurantData(URL):
    request=requests.get(URL)
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
    departureDate=departureDate[:-3]
    arrivalDate=arrivalDate[:-3]
    querystring = {"origin":departureAirport,"destination":arrivalAirport,
    "depart_date":departureDate,"return_date":arrivalDate, "currency":"USD"}
    headers = {'x-access-token': token}
    response = requests.request("GET", url, headers=headers, params=querystring)
    result=json.loads(response.text)
    result=result["data"]
    theAirport=""
    for key in result:
        theAirport=key
    result=result[theAirport]
    prices=[]
    res={}
    for key in result:
        dict=result[key]
        for k in dict:
            if k=="price":
                prices.append(int(dict["price"]))
    prices.sort()
    for key in result:
        dict=result[key]
        for k in dict:
            if int(dict["price"])==prices[0]:
                res["flight number"]=dict["flight_number"]
                res["price"]=prices[0]
                res["airline"]=dict["airline"]
    return res

#one way flight (business or older people)
#https://travelpayouts.github.io/slate/?python#non-stop-tickets
#date is YYYY-MM-DD or YYYY-MM form
def oneWayFlight(departureAirport,arrivalAirport,departureDate,arrivalDate):
    url = "https://api.travelpayouts.com/v1/prices/direct"
    querystring = {"origin":departureAirport,"destination":arrivalAirport,"depart_date"\
                :departureDate,"return_date":arrivalDate, "currency":"USD"}
    headers = {'x-access-token': token}
    response = requests.request("GET", url, headers=headers, params=querystring)
    result=json.loads(response.text)
    result=result["data"]
    for key in result:
        theAirport=key
    result=result[theAirport]
    prices=[]
    res={}
    for key in result:
        dict=result[key]
        for k in dict:
            if k=="price":
                prices.append(int(dict["price"]))
    prices.sort()
    for key in result:
        dict=result[key]
        for k in dict:
            if int(dict["price"])==prices[0]:
                res["flight number"]=dict["flight_number"]
                res["price"]=prices[0]
                res["airline"]=dict["airline"]        
    return res 

  
#finds hotel data
#adapted from https://travelpayouts.github.io/slate/?pyth
# on#displays-the-cost-of-living-in-hotels
def hotelData(destination,checkIn,checkOut):
    url = "http://engine.hotellook.com/api/v2/cache.json"
    querystring = {"location":destination,"checkIn":checkIn,"checkOut":checkOut,
                    "currency": "USD", "limit": "8", "token":token}
    headers={'x-access-token': token}
    response = requests.request("GET", url, headers=headers, params=querystring)
    responseList=json.loads(response.text)
    res={}
    name=""
    price=0
    for dict in responseList:
        info={}
        for key in dict:
            if key=="hotelName": 
                name=dict["hotelName"]
            if key=="priceAvg":
                price=int(dict["priceAvg"])
            if key=="stars":
                star=int(dict["stars"])
        info["price"]=price
        info["stars"]=star
        res[name]=info
    return res

#finds the cheapest hotel returns ('hotel name', price)
def cheapestHotel(destination,checkIn,checkOut):
    data=hotelData(destination,checkIn,checkOut) 
    dict={}
    for key in data:
        subdict=data[key]
        price=subdict['price']
        dict[key]=price
    cheapest=99999999
    cheapestHotel=""
    for key in dict:
        if int(dict[key])<cheapest:
            cheapestHotel=key
            cheapest=int(dict[key])
    res=(cheapestHotel,cheapest)
    return res

#finds the best hotel in budget returns('hotel name', price)
def bestHotel(destination,checkIn,checkOut,budget):
    data=hotelData(destination,checkIn,checkOut) 
    dict={}
    bestHotel=""
    finalPrice=0
    for key in data:
        subdict=data[key]
        price=subdict['price']
        if price<=budget:
            dict[key]=price
    mostStars=0
    for key in dict:
        subdictTwo=data[key]
        stars=subdictTwo["stars"]
        priceTwo=subdictTwo["price"]
        if stars>=mostStars:
            bestHotel=key
            mostStars=stars
            finalPrice=priceTwo
    res=(bestHotel,finalPrice)
    return res