from random import shuffle
from data import getRestaurantData

class Restaurant:

    def __init__(self, name, price, category =0 ):
        self.name = name
        self.price = price
        self.category = category

    def __repr__(self):
        return f'Restaurant(name={self.name}, price={self.price})'

def scheduleRestaurants(restaurants, budget, maxRestaurant):
    selected = []
    return scheduleRestaurantsHelper(restaurants, budget, selected, maxRestaurant)

def scheduleRestaurantsHelper(restaurants, budget, selected, maxRestaurant):
    if budget < 0:
        return None
    if maxRestaurant == 0:
        return selected

    for r in restaurants:
        if r not in selected:
            selected.append(r)
            res = scheduleRestaurantsHelper(restaurants, budget-r.price, selected, maxRestaurant-1)
            if res != None:
                return res
            selected.pop()

    return None
    
def restaurantPlan(budget,days,URL):
    restaurantDict=getRestaurantData(URL)
    restaurants = []
    for key in restaurantDict:
        restaurants.append(Restaurant(key,int(restaurantDict[key])))
    shuffle(restaurants)
    schedules = scheduleRestaurants(restaurants,budget,days*2)
    res=''
    for restaurant in schedules:
        res+=f'{restaurant.name} (${str(restaurant.price)})\n'
    return res
def restaurantPlanPrice(budget,days):
    restaurantDict=getRestaurantData()
    restaurants = []
    for key in restaurantDict:
        restaurants.append(Restaurant(key,int(restaurantDict[key])))
    shuffle(restaurants)
    schedules = scheduleRestaurants(restaurants,budget,days*2)
    res=0
    for restaurant in schedules:
        res+=restaurant.price
    return res

# picks days*2 cheapest restaurant
def cheapestRestaurants(days):
    restaurantDict=getRestaurantData()
    dict={}
    prices=[]
    for key in restaurantDict:
        dict[key]=int(restaurantDict[key])
        prices.append(int(restaurantDict[key]))
    prices.sort()
    prices=prices[:days*2]
    res=''
    for elem in prices:
        for key in restaurantDict:
            if int(elem)==int(restaurantDict[key]):
                res= res+f'{key} (${str(restaurantDict[key])})'
                res+="\n"
    return res
def cheapestRestaurantsPrice(days):
    restaurantDict=getRestaurantData()
    dict={}
    prices=[]
    for key in restaurantDict:
        dict[key]=int(restaurantDict[key])
        prices.append(int(restaurantDict[key]))
    prices.sort()
    prices=prices[:days*2]
    res=0
    for elem in prices:
        for key in restaurantDict:
            if int(elem)==int(restaurantDict[key]):
                res+=(int(restaurantDict[key]))
    return res
    
def restaurantsList(input):
    string=input
    res=[]
    for line in string.splitlines():
        res.append(line)
    return res


