from propagate_deflection import *
import json
from dateutil.parser import *
from dateutil.relativedelta import *
import time
import math
import datetime

# Load simulation settings
settings_file = open("deflection_settings.json", "r")
settings = json.load(settings_file)
angle_resolution = settings['angle_resolution']
epoch_resolution = settings['epoch_resolution']
magnitude = settings['magnitude'] # Max NED Dv = 1.8e-05 km/s

# Load all asteroids to be simulated
asteroids_file = open("asteroids.json", "r")
asteroids = json.load(asteroids_file)

def main():
    for asteroid in asteroids:
        perf_start = time.perf_counter()
        # Reset CSV
        deflections_file = "./output/"+asteroid['name']+"_deflection.csv"
        # f = open(deflections_file, "w")
        # f.write("TDB_Gregorian,TDB_MJD,Magnitude,RA,DEC,Earth_RMAG,Earth_Altitude")
        # f.close()

        # max_deflections_file = asteroid['name']+"_max_deflections.csv"
        # f = open(max_deflections_file, "w")
        # f.write("UNIX_Timestamp,Earth_Altitude")
        # f.close()

        start_timestamp = time.mktime(parse(asteroid['start']).timetuple())
        end_timestamp = time.mktime(parse(asteroid['end']).timetuple())
        
        for epoch_timestamp in range(math.ceil(start_timestamp), math.floor(end_timestamp), epoch_resolution*24*60*60):
            epoch = datetime.datetime.fromtimestamp(epoch_timestamp).strftime("%d %b %Y %H:%M:%S")
            # max_deflection = 0

            for ra in range(0, 360, angle_resolution):
                for dec in range(0, 360, angle_resolution):

                    start = time.time()

                    print("=====================")
                    print(asteroid['name'], " ", epoch)
                    print("RA", str(ra)+"°", "    DEC", str(dec)+"°")

                    data = propagate_deflection(asteroid['SPK'], asteroid['NAIF_ID'], epoch, magnitude=magnitude, ra=ra, dec=dec)
                    #print(data)

                    # if(data['EarthAltitude'] > max_deflection):
                    #     max_deflection = data['EarthAltitude']

                    # TDB_Gregorian, TDB_MJD, Magnitude, RA, DEC, RMAG, Altitude
                    csv_col = "\n"+epoch+","+str(data['TDB_MJD'])+","+str(magnitude)+","+str(ra)+","+str(dec)+","+str(data['PosX_SunICRF'])+","+str(data['PosY_SunICRF'])+","+str(data['PosZ_SunICRF'])+","+str(data['EarthRMAG'])+","+str(data['EarthAltitude'])

                    f = open(deflections_file, "a")
                    f.write(csv_col) # Append sim results
                    f.close()

                    print(time.time()-start, "seconds")
            
            # f = open(max_deflections_file, "a")
            # f.write("\n"+str(epoch_timestamp)+","+str(max_deflection)) # Append sim results
            # f.close()

        print(str(time.perf_counter()-perf_start), "!!seconds!!")
            
