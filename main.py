import json
import math
import os
import deflection_survey

if __name__ == '__main__':
    
    api_startup_file_template = open("./propagate_deflection/api_startup_file_template.txt", "r").read()
    
    api_startup_file = open("./propagate_deflection/api_startup_file.txt", "w")
    api_startup_file.write(api_startup_file_template.replace(r"{curdir}", os.path.abspath(os.path.curdir)))
    api_startup_file.close()

    print("Asteroid Deflection Survey\n====================")

    angle_resolution = input("Angle resolution (default of 5°): ")
    epoch_resolution = input("Epoch resolution (default of 7 days): ")
    magnitude = input("Deflection magnitude (default of 1.8e-05 km/s): ")

    settings = {
        'angle_resolution': int(angle_resolution) if len(angle_resolution) > 0 else 5,
        'epoch_resolution': int(epoch_resolution) if len(epoch_resolution) > 0 else 7,
        'magnitude': float(magnitude) if len(magnitude) > 0 else 1.8*math.pow(10, -5)
    }

    settings_file = open("deflection_settings.json", "w")
    settings_file.write(json.dumps(settings))
    settings_file.close()

    asteroids_file = open("asteroids.json", "r")
    asteroids = json.load(asteroids_file)
    asteroids_file.close()

    reset_csv_flag = input("Clear current data files? (Y/n) ")
    multiprocessing_flag = input("Use multiprocessing? (Y/n) ")

    for asteroid in asteroids:
        # Reset CSV
        if not os.path.exists("./output/"):
            os.makedirs("./output/")
        deflections_file = "./output/"+asteroid['name']+"_deflection.csv"
        if reset_csv_flag.lower() == "y" or len(reset_csv_flag) == 0:
            f = open(deflections_file, "w")
            f.write("TDB_Gregorian,TDB_MJD,Magnitude,RA,DEC,X,Y,Z,Earth_RMAG,Earth_Altitude")
            f.close()

    if multiprocessing_flag.lower() == "y" or len(multiprocessing_flag) == 0:
        deflection_survey.multiprocessing()
    elif multiprocessing_flag.lower() == "n":
        deflection_survey.linear()
    else:
        print("Invalid multiprocessing flag input")
