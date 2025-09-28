import requests
import time
import threading
from geopy.distance import geodesic
from flask import Flask, render_template

#Enter here the latitude and longitude of your house
MY_LAT = #<your-latitude>
MY_LON = #<your-longitude>

#max distance to check for planes in kilometers
MAX_DISTANCE = 2


planeVar = {
    "lastPlane": "No last plane yet",
    "currentPlane": "Waiting for next plane...",
    "codeJustLetters":  "https://airlinelogosbucket.s3.us-east-1.amazonaws.com/logos/waitingforplane.png",
}


app = Flask(__name__)

#returns the code of the plane with no numbers to be able to get the images
def airlineCode(sign):
    codeJustLetter = sign[0:3]
    return codeJustLetter

#return the link to the s3 bucket
def getAirlineLogoFromS3(codeJustLetter):
    url =  f"https://airlinelogosbucket.s3.us-east-1.amazonaws.com/logos/{codeJustLetter}.png"
    try:
        resStatus = requests.head(url)
        if resStatus.status_code == 200:
            return url
        else:
            return "https://airlinelogosbucket.s3.us-east-1.amazonaws.com/logos/notfound.png"
    except:
        return "https://airlinelogosbucket.s3.us-east-1.amazonaws.com/logos/notfound.png"



def planeTracker():
    while True:
        try:
            data = requests.get("https://opensky-network.org/api/states/all").json()
            for plane in data["states"]:
                sign = plane[1] or "Unknown"
                lon = plane[5]
                lat = plane[6]
                heading = plane[10]
                if lat and lon:
                    distance = geodesic((MY_LAT, MY_LON), (lat, lon)).km
                    if distance < MAX_DISTANCE:
                        if heading is not None and (35 < heading < 135):
                            if planeVar["lastPlane"] != sign: 
                                planeVar["lastPlane"] = sign
                                planeVar["codeJustLetters"] = airlineCode(sign)
                                planeVar["codeJustLetters"] = getAirlineLogoFromS3(planeVar["codeJustLetters"])
                                planeVar["currentPlane"] = f"Flight: {sign}"

                                print(f"DEBUG: Flight:", planeVar["currentPlane"]) #debug 
                                print(f"DEBUG: ", planeVar["codeJustLetters"]) #debug
                            else: 
                                planeVar["currentPlane"] = "Waiting for the next plane..."
                                planeVar["codeJustLetters"] = "https://airlinelogosbucket.s3.us-east-1.amazonaws.com/logos/waitingforplane.png"
                                print("DEBUG WAITING.....") #debug
                            
        except Exception as e:
            print("API Not returning data", e)

        time.sleep(10)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/current")
def current():
    return {"plane": planeVar["currentPlane"], "logo_s3_url": planeVar["codeJustLetters"]}

if __name__ == "__main__":
    tracker = threading.Thread(target=planeTracker, daemon=True)
    tracker.start()
    app.run()


