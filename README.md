# RPM
Random Positioning Machine path generation and analysis

random_walk.py contains the class used to generate sudo random points on a constrained 2D surface. 
``utilites.py`` contains two helper functions; interpolate_points and rpmcartesian. ``interpolate_points`` is used to break the path up into evenly spaced points. ``rpm2cartesian`` converts the machine X&Y, which are named Theta & Phi in the code, to cartesian x,y,z coordinates. 

The Jupyter/ipynb ``setup_analysis.ipynb`` demonstrates how to generate code and also how to run statistics on the path. It also demonstrates how to generate a path and save it as Gcode. 


# Requirements

Packages requrired to generate a random walk path
- numpy
- pandas
- random
Additional packages used in the notebook for analysis and plotting
- xarray
- matplotlib
