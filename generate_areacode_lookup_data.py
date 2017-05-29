from selenium import webdriver
from selenium.webdriver.common.by import By
from app.models import AreaCodeLookup
from pyzipcode import ZipCodeDatabase
from app import db
import us
from geopy.geocoders import Nominatim
from easydict import EasyDict as edict

print("starting webdriver")
driver = webdriver.Firefox()
print("getting webpage")
driver.get("https://www.allareacodes.com/")
result = driver.find_elements(By.XPATH, "//select[@style='width: 100%; margin-right: 2px']")
area_code_and_place = result[0].text.split("\n")
prefixes = [
    "New", "Los", "San", "Baton", "Fort",
    "Bowling", "Lake", "Grand", "Saint",
    "Charlotte"
]
zcdb = ZipCodeDatabase()
geolocator = Nominatim()
for area_code in area_code_and_place:
    state = area_code.split("-")[1].split("(")[0].strip()
    if "DC" in state:
        state = us.states.lookup("DC").abbr
    else:
        state = us.states.lookup(state).abbr
    city = area_code.split("-")[1].split("(")[1].rstrip(")")
    city = city.strip()
    if "," in city:
        city = city.split(",")[0]
    if " " in city:
        if [prefix for prefix in prefixes if prefix in city] == []:
            city = city.split(" ")[0]
    if isinstance(zcdb.find_zip(city=city,state=state),list):
        zip_code = zcdb.find_zip(city=city,state=state)[0]
    else:
        zip_code = zcdb.find_zip(city=city,state=state)
        if zip_code is None:
            try:
                zip_code = zcdb.find_zip(state=state)[0]
            except:
                if state == "MP":
                    zip_code = edict({
                        "latitude":15.200755,
                        "longitude":145.756952
                    })
                elif state == "GU":
                    zip_code = edict({
                        "latitude":13.463345,
                        "longitude":144.733168
                    })
                else:
                    import code
                    code.interact(local=locals())
            
            
    area_code = AreaCodeLookup(
        area_code.split("-")[0].strip(),
        city,
        state,
        zip_code.latitude,
        zip_code.longitude
    )
    
    db.session.add(area_code)
    db.session.commit()
