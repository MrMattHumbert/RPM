#!/usr/bin/env python
#
# Python script to generate fractional gravity walk for a random positioning machine
#

#Imports
import numpy as np
import pandas as pd
import random

class RandomWalk2D:
    def __init__(self, num_points, x_max, y_max):
        self.num_points = num_points
        self.x_max = x_max
        self.y_max = y_max
        self.path = pd.DataFrame()
        
    def generate_walk(self):
        theta_max = self.x_max
        phi_max = self.y_max

        points = pd.DataFrame({'Theta':0.,'Phi':0.,'Dir':[(1,1)],'X':0.,'Y':0.,'Z':-1.}) # set the first direction to be (1,1)    
        #Define random seed
        rng = np.random.default_rng(seed=12345)
        #Define edge proximity
        edge_prox = 0.99
        for i in range(self.num_points):
            
            # This is the relection Check if the point is near the edge
            if i == 0:
                direction = tuple(points.Dir[0])
            elif abs(points.Phi[i]) > edge_prox*phi_max and abs(points.Theta[i]) > edge_prox*theta_max: #Trapped in a corner head towards the origin! 
                direction = tuple([-np.sign(points.Phi[i]).astype(int),-np.sign(points.Theta[i]).astype(int)])
            elif abs(points.Phi[i]) > edge_prox*phi_max: # Reflect Phi
                direction = tuple([-points.Dir[i][0],points.Dir[i][1]])
            elif abs(points.Theta[i]) > edge_prox*theta_max: # Reflect theta
                direction = tuple([points.Dir[i][0],-points.Dir[i][1]])
            else: # Act normal
                # if the previous direction was theta=Phi go the other way
                if np.sum(list(points.Dir[i])) == 0:
                    direction = random.choice([(1, 1), (-1, -1)])
                else:
                    direction = random.choice([(-1, 1), (1, -1)])

            # Find the maximum Phi value we can go in either of the new directions
            if direction[0] <0 and direction[1] <0:           # Heading South-West
                Xint = -theta_max-points.Theta[i]+points.Phi[i]
                if -phi_max > Xint:      # We'll hit the left x boundary first
                    distance = rng.uniform(0,abs(-phi_max-points.Phi[i]))
                else:                                       # We'll hit the bottom boundary
                    distance = rng.uniform(0,abs(Xint-points.Phi[i]))
            
            elif direction[0] <0 and direction[1] >0:         # Heading North-West
                Xint = -theta_max+points.Theta[i]+points.Phi[i]
                if -phi_max > Xint:     # We'll hit the left x boundary first
                    distance = rng.uniform(0,abs(-phi_max-points.Phi[i]))
                else:                                       # We'll hit the top boundary
                    distance = rng.uniform(0,abs(Xint-points.Phi[i]))
            
            elif direction[0] >0 and direction[1] <0:         # Heading South-East
                Xint = theta_max+points.Theta[i]+points.Phi[i]
                if  phi_max < Xint:     # We'll hit the right x boundary first
                    distance = rng.uniform(0,abs(points.Phi[i]-phi_max))
                else:                                       # We'll hit the bottom boundary
                    distance = rng.uniform(points.Phi[i],Xint)-points.Phi[i]
            
            elif direction[0] >0 and direction[1] >0:         # Heading North-East
                Xint = theta_max-points.Theta[i]+points.Phi[i]
                if phi_max < Xint:      # We'll hit the right x boundary first
                    distance = rng.uniform(0,abs(points.Phi[i]-phi_max))
                else:                                       # We'll hit the top boundary
                    distance =rng.uniform(0,abs(points.Phi[i]-Xint))

            phi = direction[0] * distance + points.Phi[i]
            theta = direction[1] * distance + points.Theta[i]

            # Convert Phi and Theta to x,y,z
            phi_conversion = np.pi/15.5 # 15.5 is 180 degree rotation. 
            theta_conversion = np.pi/15.5
            phi_radians = phi * phi_conversion
            theta_radians = theta * theta_conversion

            x = np.sin(theta_radians) * np.cos(phi_radians)
            y = np.sin(phi_radians)
            z = (-1)*np.cos(theta_radians)*np.cos(phi_radians)

            # Update the new point and direction
            new_row = pd.DataFrame({'Theta':theta,
                                    'Phi':phi,
                                    'Dir':[direction],
                                    'X':x,
                                    'Y':y,
                                    'Z':z})


            points = pd.concat([points,new_row],ignore_index=True)
            # Print the current position
            #print(f"Current position and direction: ({points.Phi[i]}, {points.Theta[i]},{points.Dir[i]})")

            if abs(points.Phi[i])>phi_max or abs(points.Theta[i])>theta_max:
                break
            
        self.path = points
        return self

    def get_path(self):
        return self.path