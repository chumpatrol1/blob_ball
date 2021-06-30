from engine.blobs import blob
import math
import os
import pygame as pg
cwd = os.getcwd()

def type_to_image(type):
    global cwd
    #print("The type is...")
    #print(type)
    if(type == "soccer_ball"):
        image = cwd+"\\resources\\images\\soccer_ball.png"
    elif(type == "p1_token"):
        image = cwd+"\\resources\\images\\p1_token.png"
    elif(type == "p2_token"):
        image = cwd+"\\resources\\images\\p2_token.png"

    return image

class ball:
    def __init__(self, type = "soccer_ball", x_pos = 902, y_pos = 900):
        self.type = type
        self.image = type_to_image(type)
        #self.top_speed = 100 #The fastest that the ball can move?
        self.x_speed = 0
        self.y_speed = 0
        self.x_pos = x_pos #Ball's position
        self.x_center = x_pos + 27
        self.y_center = y_pos + 38
        self.y_pos = y_pos #Ball's position
        self.traction = 0.15 #Ground Traction
        self.friction = 0.1 #Air Friction
        self.gravity = 0.9 #Each star increases gravity
        self.grounded = False #True if the ball is on the ground
    
    ground = 1240

    def reset(self):
        self.x_speed = 0
        self.y_speed = 0
        self.x_pos = 902
        self.y_pos  = 900

    def check_blob_collisions(self, blob):
        #The distance to p1's blob
        p1_center_distance = round(math.sqrt((blob.x_center - self.x_center)**2 + (blob.y_center - self.y_center)**2),1)
        blob_collision_distance = blob.collision_distance
        #X distance used for calculations. If the distance between centers is less than this, a collision can happen

        ball_angle = math.atan2(self.x_speed, self.y_speed)
        #print(ball_angle)
        p1_angle = math.atan2(self.x_center - blob.x_pos, self.y_center - blob.y_pos)
        p1_speed = round(math.sqrt(blob.x_speed**2 + blob.y_speed**2))
        ball_speed = round(math.sqrt(self.x_speed**2 + self.y_speed**2))

        ball_vector = pg.math.Vector2(self.x_center, self.y_center)
        p1_vector = pg.math.Vector2(blob.x_center, blob.y_center)
        
        if(blob.collision_timer == 0):
            if(blob.y_center < (self.y_center - 35)): #Is the slime way above the ball?
                if(abs(blob.x_center - self.x_center) < blob_collision_distance):
                    self.image = type_to_image("soccer_ball")
            elif(blob.y_center < (self.y_center)): #Is the slime low enough to interact with the ball?
                if(abs(blob.x_center - self.x_center) < blob_collision_distance) and self.grounded and blob.y_speed >= 0:
                    #True if x is close enough, ball is grounded, hit the bottom center, and moving downwards
                    self.image = type_to_image("p1_token")
                    self.y_pos = self.y_pos + (p1_center_distance - 160) #Pop the ball upwards
                    self.y_speed = -5
                    self.x_speed = 0
                    blob.collision_timer = 2
                elif(abs(blob.x_center - self.x_center) < blob_collision_distance) and not self.grounded:
                    #True if x is close enough, and ball is airborne.
                    if(self.y_speed < 0): #Are we moving upwards?
                        self.y_speed = (-1 * self.y_speed) + blob.y_speed # Reflect!
                        if(blob.y_speed >= 0 and blob.y_pos >= 1100):
                            self.y_pos = ball.ground + (p1_center_distance - 160)
                            self.y_speed = -5
                            self.x_speed = 0


            elif(blob.y_center >= self.y_center): #Is the ball above the blob?
                if(p1_vector.distance_to(ball_vector) < blob_collision_distance * 0.8):
                    blob.collision_timer = 3
                if p1_vector.distance_to(ball_vector) < blob_collision_distance: #Standard collision
                    p1_ball_nv = p1_vector - ball_vector
                    p1_ball_collision = pg.math.Vector2(self.x_speed, self.y_speed).reflect(p1_ball_nv)
                    self.x_speed, self.y_speed = p1_ball_collision[0] + (blob.x_speed * 1.25), (1 * p1_ball_collision[1] + ((blob.y_speed - 5) * 1.5))
                    if p1_vector.distance_to(ball_vector) < blob_collision_distance:
                        self.x_pos += self.x_speed
                        self.y_pos += self.y_speed
            else:
                #Debug
                if(abs(blob.x_center - self.x_center) < blob_collision_distance):
                    pass
                else:
                    self.image = type_to_image("soccer_ball")


    def move(self):
        ground = ball.ground
        left_wall = 0
        right_wall = 1805
        ceiling = 0

        #Traction/Friction
        if(self.y_pos == ground):
            self.grounded = True
            if(self.x_speed < 0): #If we're going left, decelerate
                if(self.x_speed + self.traction) > 0:
                    self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                else:
                    self.x_speed += self.traction #Normal deceleration
            elif(self.x_speed > 0):
                if(self.x_speed - self.traction) < 0:
                    self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                else:
                    self.x_speed -= self.traction #Normal deceleration
        else:
            self.grounded = False
            if(self.x_speed < 0): #If we're going left, decelerate
                if(self.x_speed + self.friction) > 0:
                    self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                else:
                    self.x_speed += self.friction #Normal deceleration
            elif(self.x_speed > 0):
                if(self.x_speed - self.friction) < 0:
                    self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                else:
                    self.x_speed -= self.friction #Normal deceleration
        #Interacting with the main walls
        if(self.x_pos < left_wall):
            self.x_pos = left_wall
            self.x_speed = self.x_speed * -0.9
        if(self.x_pos > right_wall):
            self.x_pos = right_wall
            self.x_speed = self.x_speed * -0.9
        self.x_pos += self.x_speed

        #Interacting with the ground
        if(self.y_pos < ground):
            self.y_speed += self.gravity
        elif(self.y_pos >= ground): #Don't go under the floor!
            if(2 >= self.y_speed >= 0):
                self.y_speed = 0
            else:
                self.y_speed = -1 * math.floor(self.y_speed * 0.75)
                 #Reduces bounciness over time
            self.y_pos = ground
            
        if(self.y_pos < ceiling): #Don't raze the roof!
            if(self.y_speed > -4):
                self.y_speed = 0
            else:
                self.y_speed = math.floor(self.y_speed * -0.5) #Reduces bounciness over time
            self.y_pos = ceiling
        self.y_pos += self.y_speed

        self.x_center = self.x_pos+27 #Rough Estimate :)
        self.y_center = self.y_pos+38 #Rough Estimate :| (it's a ball... why is it different??)
        