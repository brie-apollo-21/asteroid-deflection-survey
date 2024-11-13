from propagate_deflection import gmatpy as gmat
import os
import math

def propagate_deflection(spk, naif_id, epoch, v1=None, v2=None, v3=None, magnitude=None, ra=None, dec=None):
    print(os.path.abspath(os.path.curdir)+"\propagate_deflection\\api_startup_file.txt")
    gmat.Setup(os.path.abspath(os.path.curdir)+"\propagate_deflection\\api_startup_file.txt")
    gmat.LoadScript("propagate_deflection.script")

    Asteroid = gmat.GetObject("Asteroid")
    Asteroid.SetField("OrbitSpiceKernelName", os.path.abspath(os.path.curdir)+"\SPICE_SPKs\\"+spk)
    Asteroid.SetField("NAIFId", naif_id)
    #Asteroid.SetField("Epoch", "01 Jan 2018 00:00:00.000")
    Asteroid.SetField("Epoch", epoch)

    DeflectionBurn = gmat.GetObject("Deflection")

    # Deflection is defined using x, y, z components
    if v1 != None and v2 != None and v3 != None:
        DeflectionBurn.SetField("Element1", v1)
        DeflectionBurn.SetField("Element2", v2)
        DeflectionBurn.SetField("Element3", v3)
    
    # Deflection is defined using a magnitude and RA, DEC angles
    if magnitude != None and ra != None and dec != None:
        vx = magnitude*math.sin(math.radians(90-dec))*math.cos(math.radians(ra))
        vy = magnitude*math.sin(math.radians(90-dec))*math.sin(math.radians(ra))
        vz = magnitude*math.cos(math.radians(90-dec))

        DeflectionBurn.SetField("Element1", vx)
        DeflectionBurn.SetField("Element2", vy)
        DeflectionBurn.SetField("Element3", vz)

    gmat.RunScript()

    EarthRMAG = gmat.GetRuntimeObject("EarthRMAG")
    # print("EarthRMAG", EarthRMAG.GetRealParameter("Value"), "km")

    EarthAltitude = gmat.GetRuntimeObject("EarthAltitude")
    # print("EarthAltitude", EarthAltitude.GetRealParameter("Value"), "km")

    ElapsedSecs = gmat.GetRuntimeObject("ElapsedSecs")
    # print("Elapsed", ElapsedSecs.GetRealParameter("Value")/60/60/24/365, "years")

    timeConverter = gmat.TimeSystemConverter.Instance()

    return {
        "EarthRMAG": EarthRMAG.GetRealParameter("Value"),
        "EarthAltitude": EarthAltitude.GetRealParameter("Value"),
        "ElapsedSecs": ElapsedSecs.GetRealParameter("Value"),
        "TDB_MJD": timeConverter.ConvertGregorianToMjd(epoch)
    }