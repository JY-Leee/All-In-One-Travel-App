from data import *
from scheduling import *
from cmu_112_graphics import *

#background photo citation
#https://newsroom.aaa.com/2021/06/aaa-more-than-47m
# -americans-to-celebrate-with-an-independence-day-getaway/
def appStarted(app):
    app.message="Press 's' to Start!\nEnter Your Travel Information"
    app.next=""
    app.age=0
    app.name=""
    app.destination=''
    app.dates=("2022-01-01","2022-01-02")
    app.budget=0
    app.profile=None
    app.ageCategory=""
    app.plan=''
    app.days=0
    app.origin=''
    app.arrival=''
    app.Ccalendar=False
    app.Bcalendar=False
    app.text=True
    app.backgroundStatus=True
    app.background = app.loadImage('background.jpg')
    app.totalCost=0
    app.foodURL=""

def redrawAll(app, canvas):
    if app.backgroundStatus==True:
        canvas.create_image(app.width/2, app.height/2,
                        image = ImageTk.PhotoImage(app.background))
    if app.text==True:
        inputText(app,canvas)
    if app.Ccalendar==True:
        drawCheapestCalendar(app,canvas)
    if app.Bcalendar==True:
        drawBestCalendar(app,canvas)
    


# enter features are adapted from
#https://www.cs.cmu.edu/~112/notes/notes
# -animations-part4.html#ioMethods
def keyPressed(app,event):
    if event.key=="s": 
        name=app.getUserInput('What is your name ?')
        if (name == ""):
            while name=="":
                app.showMessage("Error! There was no input, enter again")
                name=app.getUserInput('What is your name ?')
                app.name=name
        else:
            app.showMessage('You entered: ' + name)
            app.message = f'Hi, {name}!'
            app.name=name
            
        #age input
        age=app.getUserInput('What is your age?')
        if (age == "") or not(age.isdigit()):
            while (age == "") or not (age.isdigit()):
                app.showMessage("Error! Input has to be an integer, enter again")
                age=app.getUserInput('What is your age ?')
                app.age=age
        else:
            app.showMessage('You entered: ' + age)
            app.age=age
        
        #destination input
        destination=app.getUserInput('What city are you traveling to?')
        supportingDestinations=["Los Angeles","New York City"]
        if (destination not in supportingDestinations):
            while (destination not in supportingDestinations):
                app.showMessage("Error! We currently only support Los Angeles, enter again")
                destination=app.getUserInput('What city are you traveling to?')
                app.destination=destination
        else:
            app.showMessage('You are traveling to ' + destination)
            app.destination=destination

        #origin airport input
        origin=app.getUserInput('What airport are you flying from? (e.g JFK, LAX, PIT)')
        if (len(origin)!=3):
            while (len(origin)!=3):
                app.showMessage('Error! You need to input the 3 letter abbreviation of the airport (e.g JFK, LAX, PIT)')
                origin=app.getUserInput('What airport are you flying from? (e.g JFK, LAX, PIT)')
                app.origin=origin
        else:
            app.showMessage('You are traveling from ' + origin)
            app.origin=origin

        #arrival airport input
        arrival=app.getUserInput('What airport are you flying to?')
        if (len(origin)!=3):
            while (len(origin)!=3):
                app.showMessage('Error! You need to input the 3 letter abbreviation of the airport (e.g JFK, LAX, PIT)')
                arrival=app.getUserInput('What airport are you flying to?')
                app.arrival=arrival
        else:
            app.showMessage('You are traveling to ' + origin)
            app.arrival=arrival
             
        #date input
        fromDate=app.getUserInput('When do you plan to travel?\
                                enter in YYYY-MM-DD')
        toDate=app.getUserInput("When do you plan to come back?\
                                enter in YYYY-MM-DD")
        if (len(fromDate)!=10):
            while (len(fromDate)!=10):
                app.showMessage('Error! Input has to be in YYYY-MM-DD form')
                fromDate=app.getUserInput('When do you plan to travel?\
                                enter in YYYY-MM-DD')
        if (len(toDate)!=10):
            while (len(toDate)!=10):
                app.showMessage('Error! Input has to be in YYYY-MM-DD form')
                toDate=app.getUserInput('When do you plan to travel?\
                                enter in YYYY-MM-DD')
        else:
            app.showMessage(f'You are traveling from {fromDate} to {toDate}')
        app.dates=(fromDate,toDate)

        app.profile=presentUserProfile(app)
        app.message=''
        app.next=''


    if event.key=="b":
        #budget input
        budget=app.getUserInput('What is your budget? \
                                \n (Enter in USD)')
        if (budget == None):
            app.message = 'You canceled!'
        else:
            app.showMessage(f'Your budget is ${budget}' )
            app.budget=int(budget)
        days=int(countTotalDays(app))
        app.plan+="Hotel Information\n"
        bestHotelInfo=bestHotel(app.destination,app.dates[0],app.dates[1],app.budget/2)
        app.plan+=f"{bestHotelInfo}"
        app.totalCost+=int(bestHotelInfo[1])
        app.plan+="\n\n"
        app.plan+="Flight Informaion\n"
        flight=f"{flightSearch(app)}"
        app.plan+=flight
        for key in flight:
            if key=="price":
                app.totalCost+=int(flight[key])
        app.plan+="\n\n"
        app.plan+="Restaurant List\n"
        bestRestaurantPlan=restaurantPlan(app.budget/3,days)
        app.plan+=bestRestaurantPlan
        app.profile=""
        app.totalCost+=restaurantPlanPrice(app.budget/3,days)
        app.plan+=f"\nTotal Cost of the Trip: ${app.totalCost}\n"
        app.plan+="\npress 'd' to view the day-by-day calendar"

    if event.key=="c":
        app.plan+="Hotel Information\n"
        days=int(countTotalDays(app))
        cheapestHotelInfo=cheapestHotel(app.destination,app.dates[0],app.dates[1])
        app.plan+=f"{cheapestHotelInfo}"
        app.totalCost+=int(cheapestHotelInfo[1])
        app.plan+="\n\n"
        app.plan+="Flight Informaion\n"
        flight=f"{flightSearch(app)}"
        app.plan+=flight
        for key in flight:
            if key=="price":
                app.totalCost+=int(flight[key])
        app.plan+="\n\n"
        app.plan+="Restaurant List\n"
        cheapRestaurantPlan=cheapestRestaurants(days)
        app.plan+=cheapRestaurantPlan
        app.totalCost+=cheapestRestaurantsPrice(days)
        app.plan+=f"\nTotal Cost of the Trip: ${app.totalCost}\n"
        app.plan+="\n\npress 'a' to to view the day-by-day calendar"
        app.profile=""
        
    if event.key=="a":  
        app.backgroundStatus=False
        app.Bcalendar=False
        app.Ccalendar=True
        app.text=False

    if event.key=="d": 
        app.backgroundStatus=False 
        app.Ccalendar=False
        app.Bcalendar=True
        app.text=False


#to present to users
def collectUserProfile(app):
    profile={}
    profile["Name"]=app.name
    profile["Age"]=app.age
    profile["Destination"]=app.destination
    profile["Traveling Dates"]=app.dates
    # profile["Budget"]=app.budget
    profile["Origin Airport"]=app.origin
    profile["Destination Airport"]=app.arrival
    return profile

def presentUserProfile(app):
    profile=collectUserProfile(app)
    res=""
    for key in profile:
        res=res+f'{key}: {profile[key]} \n'
    res+="\n\n\n\n press 'c' to view the cheapest possible itinerary\n\
    press 'b' to see the best intenerary for a budget"
    return res

#for algorithm
def userProfileData(app):
    profile={}
    profile["Age Category"]=ageCategory()
    profile["Total Days"]=countTotalDays()

def countTotalDays(app):
    fromDate=app.dates[0]
    toDate=app.dates[1]
    fromDate.replace("-","")
    toDate.replace("-","")
    if fromDate[4:6]==toDate[4:6]:
        return (int(toDate[-2:])-int(fromDate[-2:]))
    else: 
        month=int(toDate[4:6])-int(fromDate[4:6])   
        return month*30+int(toDate[-2:])-int(fromDate[-2:])


def ageCategory(app):
    age=int(app.age)
    if 0<age<=18:
        return "Young"
    if 18<age<=30:
        return "Younger"
    if 30<age<=50:
        return "Middle"
    if 50<age<=65:
        return "Older"
    if 65<age:
        return "Old"

def flightSearch(app):
    category=ageCategory(app)
    if (category=="Older") or (category=="Old"):
        return oneWayFlight(app.origin,app.arrival,
        app.dates[0],app.dates[1])
    else: 
        return cheapestFlight(app.origin,app.arrival,
        app.dates[0],app.dates[1])

def drawCheapestCalendar(app,canvas):
    fromDate=app.dates[0]
    days=countTotalDays(app)
    y=app.width/3
    dx=app.width/(days)
    for x in range (days):
        canvas.create_rectangle(x*dx,app.height/3,(x+1)*dx,
        (app.height/3)+y,outline='black')
        canvas.create_text(x*dx+35,app.height/3+10,
        text=f'{fromDate[:8]}{str(int(fromDate[-2:])+x)}',
        font='Ariel 10 bold',fill='black')
        if x==0:
            canvas.create_text(x*dx+0.5*dx,app.height/3+20,
            text=f'Check-in for {cheapestHotel(app.destination,app.dates[0],app.dates[1])}',
            font='Ariel 6 bold',fill='black')
            canvas.create_text(x*dx+0.5*dx,app.height/3+40,
            text=f'Flight to {app.arrival}',
            font='Ariel 6 bold',fill='black')
        if x==(days-1):
            canvas.create_text(x*dx+0.5*dx,app.height/3+25,
            text=f'Check-out for {cheapestHotel(app.destination,app.dates[0],app.dates[1])}',
            font='Ariel 6 bold',fill='black')
            canvas.create_text(x*dx+0.5*dx,app.height/3+40,
            text=f'Flight to {app.origin}',
            font='Ariel 6 bold',fill='black')
    string=cheapestRestaurants(days)
    food=restaurantsList(string)
    for x in range (days):
        for i in range (len(food)):
            if x*2==i:
                canvas.create_text(x*dx+0.5*dx,app.height/3+80,
                text=f'{food[i]}\n{food[i+1]}',
                font='Ariel 6 bold',fill='black')

def drawBestCalendar(app,canvas):
    fromDate=app.dates[0]
    days=countTotalDays(app)
    y=app.width/3
    dx=app.width/(days)
    for x in range (days):
        canvas.create_rectangle(x*dx,app.height/3,(x+1)*dx,
        (app.height/3)+y,outline='black')
        canvas.create_text(x*dx+35,app.height/3+10,
        text=f'{fromDate[:8]}{str(int(fromDate[-2:])+x)}',
        font='Ariel 10 bold',fill='black')
        if x==0:
            canvas.create_text(x*dx+dx/2,app.height/3+20,
            text=f'Check-in for {bestHotel(app.destination,app.dates[0],app.dates[1],app.budget/2)}',
            font='Ariel 6 bold',fill='black')
            canvas.create_text(x*dx+0.5*dx,app.height/3+40,
            text=f'Flight to {app.arrival}',
            font='Ariel 6 bold',fill='black')
        if x==(days-1):
            canvas.create_text(x*dx+0.5*dx,app.height/3+25,
            text=f'Check-out for {bestHotel(app.destination,app.dates[0],app.dates[1],app.budget/2)}',
            font='Ariel 6 bold',fill='black')
            canvas.create_text(x*dx+0.5*dx,app.height/3+40,
            text=f'Flight to {app.arrival}',
            font='Ariel 6 bold',fill='black')
    string=cheapestRestaurants(days)
    food=restaurantsList(string)
    for x in range (days):
        for i in range (len(food)):
            if x*2==i:
                canvas.create_text(x*dx+120,app.height/3+80,
                text=f'{food[i]}\n{food[i+1]}',
                font='Ariel 6 bold',fill='black')
    

def inputText(app,canvas):
    canvas.create_text(app.width/2,app.height/2
            ,text=app.message,
            font=f'Ariel 20 bold',fill='black')
    canvas.create_text(app.width/2,5*app.height/6,
            text=app.next,
            font=f'Ariel 15 bold',fill='blue')
    canvas.create_text(app.width/2,app.height/2,
            text=app.profile,
            font=f'Ariel 15 bold',fill='black')
    canvas.create_text(app.width/2,app.height/2,
            text=app.plan,
            font=f'Ariel 10 bold',fill='black')

runApp(width=800, height=600)
