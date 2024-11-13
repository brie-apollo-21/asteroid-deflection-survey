from deflection_sim import run_simulation
import json
from dateutil.parser import *
import dateutil.tz as tz
from dateutil.relativedelta import *
import time
import math
import datetime
from multiprocessing import Pool

# Load simulation settings
settings_file = open("deflection_settings.json", "r")
settings = json.load(settings_file)
angle_resolution = settings['angle_resolution']
epoch_resolution = settings['epoch_resolution']
magnitude = settings['magnitude'] # Max NED Dv = 1.8e-05 km/s

# Load all asteroids to be simulated
asteroids_file = open("asteroids.json", "r")
asteroids = json.load(asteroids_file)

def pool_func(ra, dec, epoch, asteroid):
    # print(asteroid['name'])
    # Reset CSV
    deflections_file = "./asteroid_data/"+asteroid['name']+"_deflection.csv"
    # f = open(deflections_file, "w")
    # f.write("TDB_Gregorian,TDB_MJD,Magnitude,RA,DEC,Earth_RMAG,Earth_Altitude")
    # f.close()

    # max_deflections_file = asteroid['name']+"_max_deflections.csv"
    # f = open(max_deflections_file, "w")
    # f.write("UNIX_Timestamp,Earth_Altitude")
    # f.close()
    
    # max_deflection = 0
    start = time.time()

    print("=====================\n"+asteroid['name'], " ", epoch+"\n"+"RA", str(ra)+"°", "    DEC", str(dec)+"°", flush=True)
    # print("=====================")
    # print(asteroid['name'], " ", epoch)
    # print("RA", str(ra)+"°", "    DEC", str(dec)+"°")

    data = run_simulation(asteroid['SPK'], asteroid['NAIF_ID'], epoch, magnitude=magnitude, ra=ra, dec=dec)
    #print(data)

    # if(data['EarthAltitude'] > max_deflection):
    #     max_deflection = data['EarthAltitude']

    # TDB_Gregorian, TDB_MJD, Magnitude, RA, DEC, RMAG, Altitude
    csv_row = "\n"+epoch+","+str(data['TDB_MJD'])+","+str(magnitude)+","+str(ra)+","+str(dec)+","+str(data['EarthRMAG'])+","+str(data['EarthAltitude'])

    f = open(deflections_file, "a")
    f.write(csv_row) # Append sim results
    f.close()

    print(time.time()-start, "seconds")

    return csv_row
    
    # f = open(max_deflections_file, "a")
    # f.write("\n"+str(epoch_timestamp)+","+str(max_deflection)) # Append sim results
    # f.close()

    # return deflections_file, csv_row

def survey(asteroid):
    start_timestamp = parse(asteroid['start']).replace(tzinfo=tz.UTC).timestamp()
    end_timestamp = parse(asteroid['end']).replace(tzinfo=tz.UTC).timestamp()
    epochs = []
    for epoch_timestamp in range(math.ceil(start_timestamp), math.floor(end_timestamp), epoch_resolution*24*60*60):
        epochs.append(datetime.datetime.fromtimestamp(epoch_timestamp, tz=tz.UTC).strftime("%d %b %Y %H:%M:%S"))
    
    iter = [(ra,dec,epoch,asteroid) for ra in range(0, 360, angle_resolution) for dec in range(0, 360, angle_resolution) for epoch in epochs]

    # print("Approximate", asteroid['name'] ,"simulation time:", str((len(iter)*0.55)/60/60/24), "days")

    with Pool() as pool:
        pool.starmap(pool_func, iter)

def main():
    for asteroid in asteroids:
        perf_start = time.perf_counter()
        # # Reset CSV
        # deflections_file = "./asteroid_data/"+asteroid['name']+"_deflection.csv"
        # f = open(deflections_file, "w")
        # f.write("TDB_Gregorian,TDB_MJD,Magnitude,RA,DEC,Earth_RMAG,Earth_Altitude")
        # f.close()
        survey(asteroid)
        print("\n\nCompleted", asteroid['name'], "simulation in", str(time.perf_counter()-perf_start), "seconds\n\n")