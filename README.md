# Asteroid Deflection Survey

## Quick Startup
Run `main.py` and enter desired survey configs

## Custom Survey Code Usage
To conduct the survey from your own code, run either `deflection_survey.linear()` or `deflection_survey.multiprocessing()`.
<br><br>
These methods don't require any arguments since all the survey and simulation details are configured in `asteroids.json` and `deflection_settings.json`.

## Details
### asteroids.json
This file contains all of the asteroids you would like to run surveys for. It's assumed that without any deflection, the asteroid will pass through Earth's SOI and any deflections applied will keep the asteroid's trajectory within Earth's SOI.
<br><br>
The start and end epochs define the period to simulate deflections for.
<br><br>
The only available ephemeris support currently available are SPICE SPK kernels.
### deflection_settings.json
`angle_resolution` is the RA/DEC interval between each deflection direction in degrees.
<br>
`epoch_resolution` is the time interval between each deflection simulation run in days.
