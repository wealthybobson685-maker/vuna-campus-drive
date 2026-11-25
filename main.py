from fastapi import FastAPI


app = FastAPI(title="Vuna Campus Drive")


@app.get("/")

def home():

    return {"message": "Campus ride server is running"}

    from fastapi import FastAPI, HTTPException


app = FastAPI(title="Vuna Campus Drive")


# Campus places. Latitude and longitude will be added later.

places = [

    {"id": 1, "name": "Main Gate"},

    {"id": 2, "name": "Sports Arena"},

    {"id": 3, "name": "Chapel"},

    {"id": 4, "name": "Faculty of Law"},

    {"id": 5, "name": "Faculty of Computing"},

    {"id": 6, "name": "Auditorium"},

    {"id": 7, "name": "Library"},

    {"id": 8, "name": "Girls Hostel"},

    {"id": 9, "name": "Old Kelson"},

    {"id": 10, "name": "New Kelson"},

    {"id": 11, "name": "Boys Hostels R, S, T"},

    {"id": 12, "name": "Choppies"},

    {"id": 13, "name": "Boys Hostel (FLE and above)"},

    {"id": 14, "name": "Basketball Court"},

    {"id": 15, "name": "Veritas Cafe"},

    {"id": 16, "name": "LLC (Multipurpose Hall)"},

    {"id": 17, "name": "Postgraduate Area"},

    {"id": 18, "name": "MPH"},

    {"id": 19, "name": "Asa Cafe"},

    {"id": 20, "name": "NLT (Blocks A, B, C)"},

    {"id":21, "name": "Bookshop"},

]

@app.get("/")

def home():

    return {"message": "Campus ride server is running"}

# Returns the whole list of places

@app.get("/places")

def get_places():
    return places



# Returns one place by its id, for example /places/3

@app.get("/places/{place_id}")

def get_place(place_id: int):

    for place in places:

        if place["id"] == place_id:
            return place

    raise HTTPException(status_code=404, detail="Place not found")
    jls_extract_var = "Your New Place"
{"id": 21, "name": "Your New Place"},
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# --- 1. Your existing places data and routes ---
places = [
    {"id": 1, "name": "Campus Gate"},
    {"id": 2, "name": "Library"},
    {"id": 3, "name": "Student Center"}
]

@app.get("/places/{place_id}")
def get_place(place_id: int):
    for place in places:
        if place["id"] == place_id:
            return place
    raise HTTPException(status_code=404, detail="Place not found")


# --- 2. New: Pydantic model for ride requests ---
class RideRequest(BaseModel):
    pickup: str
    destination: str
    offered_price: float


# --- 3. New: Database list and endpoints for rides ---
rides = []

@app.post("/rides")
def create_ride(ride: RideRequest):
    new_ride = {
        "id": len(rides) + 1,
        "pickup": ride.pickup,
        "destination": ride.destination,
        "offered_price": ride.offered_price,
        "status": "requested"
    }
    rides.append(new_ride)
    return new_ride

@app.get("/rides")
def get_rides():
    return rides
    from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. Shared base model (notice we removed offered_price so the system sets it automatically)
class BaseRide(BaseModel):
    pickup: str
    destination: str
    vehicle_type: str


# 2. Keke model: Shared (200) vs Private/Charter (800)
class KekeRide(BaseRide):
    vehicle_type: str = "keke"
    is_private: bool = False  # False = people can join (200), True = private/drop (800)


# 3. Minibus model: Shared (200 per seat) vs Private/Charter (800)
class MinibusRide(BaseRide):
    vehicle_type: str = "minibus"
    is_private: bool = False
    seats_needed: int = 1


rides = []

@app.post("/rides")
def create_ride(ride: KekeRide | MinibusRide):
    new_ride = ride.model_dump()
    new_ride["id"] = len(rides) + 1
    new_ride["status"] = "requested"

    # Automatic Pricing Logic
    if ride.is_private:
        new_ride["price"] = 800
    else:
        if isinstance(ride, MinibusRide):
            new_ride["price"] = 200 * ride.seats_needed
        else:
            new_ride["price"] = 200

    rides.append(new_ride)
    return new_ride


@app.get("/rides")
def get_rides():
    return rides
    # 6. Endpoint for drivers to accept a ride
@app.patch("/rides/{ride_id}/accept")
def accept_ride(ride_id: int):
    for ride in rides:
        if ride["id"] == ride_id:
            if ride["status"] != "requested":
                return {"error": "This ride is no longer available or has already been accepted."}
            
            ride["status"] = "accepted"
            return {"message": "Ride successfully accepted by driver!", "ride": ride}
            
    return {"error": "Ride not found"}