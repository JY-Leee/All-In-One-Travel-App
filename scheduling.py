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
    
def restaurantPlan(budget,days):
    restaurantDict=getRestaurantData()
    restaurants = []
    for key in restaurantDict:
        restaurants.append(Restaurant(key,int(restaurantDict[key])))
    shuffle(restaurants)
    schedules = scheduleRestaurants(restaurants,budget,days*2)
    res=''
    for restaurant in schedules:
        res+=f'{restaurant.name} (${str(restaurant.price)})\n'
    return res