# Plane Tracker 
A real-time web app that tracks planes flying within 2 km of a chosen location using the OpenSky Network API.  
Built with **Python (Flask)**, **JavaScript**, **AWS S3**, **HTML**, and **CSS**.

## Features
- Live plane tracking with OpenSky API  
- Distance filtering with `geopy` (only shows flights within 2 km)  
- Airline logos hosted on AWS S3 with fallback handling  
- Automatic updates every 2 seconds via JavaScript  
- Simple web interface with live text + airline logo display  

## Setup
1. **Edit `planes.py` and update the constants for your location:**
   ```python
   MY_LAT = <your-latitude>
   MY_LON = <your-longitude>
   ```
   > The program will only detect planes **north of your house, heading east (35°–135°), and inside 2 km**.

2. **Clone the repo and install dependencies:**
   ```bash
   git clone https://github.com/diego-avalos-code/plane-tracker.git
   cd plane-tracker
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python planes.py
   ```

4. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Tech Stack
- **Backend**: Python, Flask, geopy, requests  
- **Frontend**: HTML, CSS, JavaScript (fetch API)  
- **Cloud**: AWS S3 for airline logos  
- **API**: OpenSky Network API  

