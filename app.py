from flask import Flask, request, render_template, redirect, url_for, session
from process_email import extract_domain, InvalidEmail
import sys

app = Flask(__name__)  # The name of the app is arbitrarily set to the name of the module

allLocations = [{"name" : "circleK", "town" : "Gorey", "address" : "Arklow Road", "dieselprice" : 1.89, "petrolprice" : 10.99},
                {"name" : "Gala", "town" : "Gorey", "address" : "Clonattin", "dieselprice" : 20.89, "petrolprice" : 1.99},
                {"name" : "Applegreen", "town" : "Gorey", "address" : "Ramstown", "dieselprice" : 3.89, "petrolprice" : 3.99},
                {"name" : "Londis", "town" : "Gorey", "address" : "Carnew Road", "dieselprice" : 4.89, "petrolprice" : 4.99},
                {"name" : "Circle K", "town" : "Greystones", "address" : "Rathdown Road", "dieselprice" : 3.89, "petrolprice" : 3.99},
                {"name" : "Circle K", "town" : "Greystones", "address" : "Kilcoole", "dieselprice" : 4.89, "petrolprice" : 4.99},  
                {"name" : "circleK", "town" : "Greystones", "address" : "Kilmacanogue", "dieselprice" : 1.89, "petrolprice" : 10.99},
                {"name" : "Kilpedder Filling Station", "town" : "Greystones", "address" : "Johnstown", "dieselprice" : 20.89, "petrolprice" : 1.99},
                {"name" : "O'Mahonys", "town" : "Arklow", "address" : "Dublin Road", "dieselprice" : 3.89, "petrolprice" : 3.99},
                {"name" : "Certa", "town" : "Arklow", "address" : "Wexford Road", "dieselprice" : 4.89, "petrolprice" : 4.99},
                {"name" : "Applegreen", "town" : "Arklow", "address" : "Wexford Road", "dieselprice" : 3.89, "petrolprice" : 3.99},
                {"name" : "Circle K", "town" : "Arklow", "address" : "Ferrybank", "dieselprice" : 4.89, "petrolprice" : 4.99},
                {"name" : "circleK", "town" : "Enniscorthy", "address" : "Templeshannon", "dieselprice" : 1.89, "petrolprice" : 10.99},
                {"name" : "Campus", "town" : "Enniscorthy", "address" : "Kilcannon", "dieselprice" : 20.89, "petrolprice" : 1.99},
                {"name" : "Pat Webster", "town" : "Enniscorthy", "address" : "Askbrook", "dieselprice" : 3.89, "petrolprice" : 3.99},
                {"name" : "Londis", "town" : "Enniscorthy", "address" : "Bellefield Road", "dieselprice" : 4.89, "petrolprice" : 4.99},
                {"name" : "Maxol", "town" : "Wexford", "address" : "Trinity Street", "dieselprice" : 3.89, "petrolprice" : 3.99},
                {"name" : "Texaco", "town" : "Wexford", "address" : "Carrick Lawn", "dieselprice" : 4.89, "petrolprice" : 4.99},
                {"name" : "Maxol", "town" : "Wexford", "address" : "Trinity Street", "dieselprice" : 3.89, "petrolprice" : 3.99},
                {"name" : "Circle K", "town" : "Wexford", "address" : "Clonard", "dieselprice" : 4.89, "petrolprice" : 4.99}]



@app.route("/")
def index():
    towns = getTowns()
    locations = SearchLocations("gorey", "diesel")
    return render_template('index.html', towns=towns, locations=locations, selectedtown="gorey", selectedfuel="diesel")


@app.route("/membership")
def membership():
    return render_template("membership.html")

@app.route("/fuel_price_update")
def fuel_price_update():
    return render_template("fuel_price_update.html")

@app.route('/GetLocations/', methods=['POST'])
def GetLocations():
    data = request.form

    selectTown = data['selectTown']
    SortBy = data['SortBy']
    
    
    towns = getTowns()
    locations = SearchLocations(selectTown, SortBy)

    return render_template('index.html', towns=towns, locations=locations, selectedtown=selectTown, selectedfuel=SortBy)


def SearchLocations(town, sortby = "petrol"):
    global allLocations
    foundLocations = []
    
    for loc in allLocations:

        if loc.get("town").lower() == town.lower():
            foundLocations.append([loc.get("name"), loc.get("town"), loc.get("address"), loc.get("dieselprice"), loc.get("petrolprice")])   
        
    if sortby == "petrol":
        sortIndex = 4
    elif sortby == "diesel":
        sortIndex = 3
    else: 
        sortIndex = 4

    sortedLocations = sorted(foundLocations, key=lambda d: d[sortIndex])
    
    return sortedLocations


@app.route('/Login/', methods=['POST'])
def Login():
    data = request.form
    frm_email = data['email']
    frm_password = data['password']
    isValid = True
    
    try:
        local_part = extract_domain(frm_email)
    except InvalidEmail as e:
        isValid = False
        print("The email address you provided is invalid, please fix the issue and submit it again.")
        error_message = f"Error details: {e}"
        
    if isValid == True:
        return render_template('membership.html', email=frm_email)
    else:
        return render_template('membership.html', error_message=error_message)


@app.route('/Logout/', methods=['POST'])
def Logout():
    return render_template('membership.html')

@app.route('/ApplyFuelCard/', methods=['POST'])
def ApplyFuelCard():
    header = "Fuel Card Application"
    message = "Application submitted successfully, fuel card will be issued shortly"
    return render_template("response.html",  message=message, header=header)


@app.route('/AddLocation/', methods=['POST'])
def AddLocation():
    global allLocations

    data = request.form
    name = data['loc_name']
    town = data['loc_town']
    address = data['loc_address']
    dieselprice = data['loc_dieselprice']
    petrolprice = data['loc_petrolprice']

    newLoc ={"name" : name, "town" :  town, "address" :  address,  "dieselprice" : float(dieselprice),  "petrolprice" : float(petrolprice)}
    allLocations.append(newLoc)

    header = "Location,address and Fuel Price Input"
    message = "Location, address and fuel prices submitted successfully and has been included in the search data on the HOME page    " + "<a href='/'>Home</a>"

    return render_template("response.html",  message=message, header=header)



def getTowns():
    global allLocations
    towns = []
    
    for loc in allLocations:
        if not inList(loc["town"], towns):
            towns.append(loc["town"])

    return towns



def inList(town, towns):
    isFound = False

    for t in towns:
        if t.lower() == town.lower():
            isFound = True
            break

    return isFound



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)