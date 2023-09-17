#!/usr/bin/env python
#
# Python utility functions for dealing with random positioning machine code and paths
#

import numpy as np


def interpolate_points(series1,series2, target_length):
    '''Function interpolates points in a [[x1,y1],[x2,y2],[x3,y3]]
    so all the points have an even spacing if this is taken to be big enough say target length 0.01 or 0.001
    then we can multiply by the velocty and get the time averaged gravity'''
    points =np.array([[x,y] for x, y in zip(series1,series2)])
    interpolated_points = []
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        distance = np.linalg.norm(p2 - p1)
        num_segments = int(np.ceil(distance / target_length))
        t_values = np.linspace(0, 1, num_segments + 1)
        for t in t_values[:-1]:
            interpolated_point = p1 + t * (p2 - p1)
            interpolated_points.append(interpolated_point)
    interpolated_points.append(points[-1])  # Add the last point
    return np.array(interpolated_points)

def rpm2cartesian(theta,phi):
    # Convert Phi and Theta to x,y,z
    phi_conversion = np.pi/15.5 # 15.5 is 180 degree rotation. 
    theta_conversion = np.pi/15.5
    phi_radians = phi * phi_conversion
    theta_radians = theta * theta_conversion

    x = np.sin(theta_radians) * np.cos(phi_radians)
    y = np.sin(phi_radians)
    z = (-1)*np.cos(theta_radians)*np.cos(phi_radians)
    return x,y,z
