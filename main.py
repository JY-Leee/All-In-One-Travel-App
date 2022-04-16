from data import *
from scheduling import *
from cmu_112_graphics import *

def appStarted(app):
    app.message="Press 's' to Start!"
    app.next=""
    app.age=0
    app.name=""
    app.gender=""
    app.purpose=''
    app.destination=''
    app.travelerCount=1
    app.relationship=''
    app.dates=("2022-01-01","2022-01-02")
    app.budget=0
    app.profile=None
    app.ageCategory=""
    app.plan=''
    app.days=0
    app.origin=''

def redrawAll(app, canvas):
    inputText(app,canvas)

# enter features are adapted from
#https://www.cs.cmu.edu/~112/notes/notes
# -animations-part4.html#ioMethods
def keyPressed(app,event):
    if event.key=="s": 
        name=app.getUserInput('What is your name ?')
        if (name == None):
            app.message = 'You canceled!'
        else:
            app.showMessage('You entered: ' + name)
            app.message = f'Hi, {name}!'
            app.name=name
        #age input
        age=app.getUserInput('What is your age?')
        if (age == None):
            app.message = 'You canceled!'
        else:
            app.showMessage('You entered: ' + age)
            app.age=int(age)
        #gender input
        gender=app.getUserInput('What is your gender?')
        if (gender == None):
            app.message = 'You canceled!'
        else:
            app.showMessage('You entered: ' + gender)
            app.gender=gender
        #number of travelers input
        travelerCount=app.getUserInput('How many people are you traveling with?\
                                            (Including Yourself)')
        if (travelerCount == None):
            app.showMessage('You are traveling alone')
        else:
            app.showMessage(f'You are traveling with {travelerCount} people')
            app.travelerCount=int(travelerCount)
        #relationship input
        relationship=app.getUserInput('What is the relationship\
                                     with your fellow travelers?\
                                        (Family, Individual, Colleagues, Couple)')
        if (relationship == None):
            app.relationship='Individual'
            app.showMessage('You are traveling alone')
        else:
            app.showMessage('You are traveling with' + relationship)
            app.relationship=relationship
        app.next="Press '->' to Proceed"
        
    if event.key=="Right":
        #origin input

        origin=app.getUserInput('What city are you comming from?')
        if (origin == None):
            app.showMessage('You entered: ' + origin)
            app.origin=origin
        else:
            app.showMessage('You are traveling from' + origin)
            app.origin=origin
        #destination input
        destination=app.getUserInput('What city are you traveling to?')
        if (destination == None):
            app.showMessage('You entered: ' + destination)
            app.destination=destination
        else:
            app.showMessage('You are traveling to' + destination)
            app.destination=destination
        #purpose input
        purpose=app.getUserInput('What is the purpose of your travel? \
                                \n (Business, Vacation, Long Term)')
        if (purpose == None):
            app.message = 'You canceled!'
        else:
            app.showMessage('You purpose of traveling is' + purpose)
            app.purpose=purpose

        #date input
        fromDate=app.getUserInput('When do you plan to travel?\
                                enter in YYYY-MM-DD')
        toDate=app.getUserInput("When do you plan to come back?\
                                enter in YYYY-MM-DD")
        if (purpose == None):
            app.message = 'You canceled!'
        else:
            app.showMessage(f'You are traveling from {fromDate} to {toDate}')
            app.dates=(fromDate,toDate)
        #budget input
        budget=app.getUserInput('What is your budget? \
                                \n (Enter in USD)')
        if (budget == None):
            app.message = 'You canceled!'
        else:
            app.showMessage(f'Your budget is ${budget}' )
            app.budget=int(budget)
        app.profile=presentUserProfile(app)
        app.message=''
        app.next=''

    if event.key=="l":
        days=countTotalDays(app)
        app.plan+=restaurantPlan(app.budget,days)
        app.plan+="\n"
        # app.plan+=flightSearch(app)
        app.profile=""


#to present to users
def collectUserProfile(app):
    profile={}
    profile["Name"]=app.name
    profile["Age"]=app.age
    profile["Gender"]=app.gender
    profile["Purpose"]=app.purpose
    profile["Destination"]=app.destination
    profile["Traveler Count"]=app.travelerCount
    profile["Traveling Dates"]=app.dates
    profile["Budget"]=app.budget
    return profile

def presentUserProfile(app):
    profile=collectUserProfile(app)
    res=""
    for key in profile:
        res=res+f'{key}: {profile[key]} \n'
    res+="\n\n\n\n press 'l' to see your final iternary"
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
    if 0<app.age<=18:
        return "Young"
    if 18<app.age<=30:
        return "Younger"
    if 30<app.age<=50:
        return "Middle"
    if 50<app.age<=65:
        return "Older"
    if 65<app.age:
        return "Old"

def flightSearch(app):
    category=ageCategory(app)
    if (category=="Older") or (category=="Old"):
        return oneWayFlight(app.origin,app.destination,
        app.dates[0],app.dates[1])
    else: 
        return cheapestFlight(app.origin,app.destination,
        app.dates[0],app.dates[1])

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
