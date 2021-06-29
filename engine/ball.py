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
        self.gravity = 1 #Each star increases gravity
        self.grounded = False #True if the ball is on the ground

    def reset(self):
        self.x_speed = 0
        self.y_speed = 0
        self.x_pos = 902
        self.y_pos  = 900

    def check_collisions(self, p1_blob, p2_blob, *objs):
        #The distance to p1's blob
        p1_center_distance = round(math.sqrt((p1_blob.x_center - self.x_center)**2 + (p1_blob.y_center - self.y_center)**2),1)
        p2_center_distance = round(math.sqrt((p2_blob.x_center - self.x_center)**2 + (p2_blob.y_center - self.y_center)**2),1)
        #X distance used for calculations. If the distance between centers is less than this, a collision can happen
        blob_collision_distance = 104
        ball_angle = math.atan2(self.x_speed, self.y_speed)
        #print(ball_angle)
        p1_angle = math.atan2(self.x_center - p1_blob.x_pos, self.y_center - p1_blob.y_pos)
        p2_angle = math.atan2(self.x_center - p2_blob.x_pos, self.y_center - p2_blob.y_pos)
        p1_speed = round(math.sqrt(p1_blob.x_speed**2 + p1_blob.y_speed**2))
        p2_speed = round(math.sqrt(p2_blob.x_speed**2 + p2_blob.y_speed**2))
        ball_speed = round(math.sqrt(self.x_speed**2 + self.y_speed**2))

        ball_vector = pg.math.Vector2(self.x_center, self.y_center)
        p1_vector = pg.math.Vector2(p1_blob.x_center, p1_blob.y_center)
        p2_vector = pg.math.Vector2(p2_blob.x_center, p2_blob.y_center)
        
        if(p1_blob.y_center < (self.y_center - 35)): #Is the slime way above the ball?
            if(abs(p1_blob.x_center - self.x_center) < blob_collision_distance):
                self.image = type_to_image("soccer_ball")
        elif(p1_blob.y_center < (self.y_center)): #Is the slime low enough to interact with the ball?
            if(abs(p1_blob.x_center - self.x_center) < blob_collision_distance) and self.grounded and p1_center_distance < 50 and p1_blob.y_speed >= 0:
                #True if x is close enough, ball is grounded, hit the bottom center, and moving downwards
                self.y_speed = -10
                self.y_pos = 1100 #Pop the ball upwards
            elif(abs(p1_blob.x_center - self.x_center) < blob_collision_distance) and self.grounded and p1_center_distance >= 50 and p1_blob.y_speed >= 0:
                #True if x is close enough, ball is grounded, hit an edge, and moving downwards
                if(p1_blob.x_center > self.x_center):
                    #True if p1_blob is to the right of the ball
                    self.y_speed = -5
                    self.x_speed = -10 - math.sqrt(abs(p1_blob.x_speed))
                    self.y_pos = 1200 #Pop the ball up and away
                    self.x_pos -= 25 + blob_collision_distance - abs(p1_blob.x_center - self.x_center)
                else:
                    #True if p1_blob is to the left of the ball
                    self.y_speed = -5
                    self.x_speed = 10 + math.sqrt(abs(p1_blob.x_speed))
                    self.y_pos = 1200 #Pop the ball up and away
                    self.x_pos += 25 + blob_collision_distance - abs(p1_blob.x_center - self.x_center)
            elif(abs(p1_blob.x_center - self.x_center) < blob_collision_distance) and not self.grounded:
                #True if x is close enough, and ball is airborne.
                if(self.y_speed < 0): #Are we moving upwards?
                    self.y_speed = (-1 * self.y_speed) + p1_blob.y_speed # Reflect!
        elif(p1_blob.y_center >= self.y_center): #Is the ball above the blob?
            if p1_vector.distance_to(ball_vector) < blob_collision_distance:
                p1_ball_nv = p1_vector - ball_vector
                p1_ball_collision = pg.math.Vector2(self.x_speed, self.y_speed).reflect(p1_ball_nv)
                self.x_speed, self.y_speed = p1_ball_collision[0] + (p1_blob.x_speed * 1.5), (1 * p1_ball_collision[1] + ((p1_blob.y_speed - 5) * 2))
                if p1_vector.distance_to(ball_vector) < blob_collision_distance:
                    self.x_pos += self.x_speed
                    self.y_pos += self.y_speed
        else:
            #Debug
            if(abs(p1_blob.x_center - self.x_center) < blob_collision_distance):
                pass
            else:
                self.image = type_to_image("soccer_ball")

        if(p2_blob.y_center < (self.y_center - 35)): #Is the slime way above the ball?
            if(abs(p2_blob.x_center - self.x_center) < blob_collision_distance):
                self.image = type_to_image("soccer_ball")
        elif(p2_blob.y_center < (self.y_center)): #Is the slime low enough to interact with the ball?
            if(abs(p2_blob.x_center - self.x_center) < blob_collision_distance) and self.grounded and p2_center_distance < 50 and p2_blob.y_speed >= 0:
                #True if x is close enough, ball is grounded, hit the bottom center, and moving downwards
                self.y_speed = -10
                self.y_pos = 1100 #Pop the ball upwards
            elif(abs(p2_blob.x_center - self.x_center) < blob_collision_distance) and self.grounded and p2_center_distance >= 50 and p2_blob.y_speed >= 0:
                #True if x is close enough, ball is grounded, hit an edge, and moving downwards
                if(p2_blob.x_center > self.x_center):
                    #True if p2_blob is to the right of the ball
                    self.y_speed = -5
                    self.x_speed = -10 - math.sqrt(abs(p2_blob.x_speed))
                    self.y_pos = 1200 #Pop the ball up and away
                    self.x_pos -= 25 + blob_collision_distance - abs(p2_blob.x_center - self.x_center)
                else:
                    #True if p2_blob is to the left of the ball
                    self.y_speed = -5
                    self.x_speed = 10 + math.sqrt(abs(p2_blob.x_speed))
                    self.y_pos = 1200 #Pop the ball up and away
                    self.x_pos += 25 + blob_collision_distance - abs(p2_blob.x_center - self.x_center)
            elif(abs(p2_blob.x_center - self.x_center) < blob_collision_distance) and not self.grounded:
                #True if x is close enough, and ball is airborne.
                if(self.y_speed < 0): #Are we moving upwards?
                    self.y_speed = (-1 * self.y_speed) + p2_blob.y_speed # Reflect!
        elif(p2_blob.y_center >= self.y_center): #Is the ball above the blob?
            if p2_vector.distance_to(ball_vector) < blob_collision_distance:
                p2_ball_nv = p2_vector - ball_vector
                p2_ball_collision = pg.math.Vector2(self.x_speed, self.y_speed).reflect(p2_ball_nv)
                self.x_speed, self.y_speed = p2_ball_collision[0] + (p2_blob.x_speed * 1.5), (1 * p2_ball_collision[1] + ((p2_blob.y_speed - 5) * 2))
                if p2_vector.distance_to(ball_vector) < blob_collision_distance:
                    self.x_pos += self.x_speed
                    self.y_pos += self.y_speed
        else:
            #Debug
            if(abs(p2_blob.x_center - self.x_center) < blob_collision_distance):
                pass
            else:
                self.image = type_to_image("soccer_ball")

    def move(self):
        ground = 1240
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
        self.y_pos += self.y_speed
        if(self.y_pos > ground): #Don't go under the floor!
            if(self.y_speed < 4):
                self.y_speed = 0
            else:
                self.y_speed = math.floor(self.y_speed * -0.75) #Reduces bounciness over time
            self.y_pos = ground

        elif(self.y_pos < ceiling): #Don't raze the roof!
            if(self.y_speed > -4):
                self.y_speed = 0
            else:
                self.y_speed = math.floor(self.y_speed * -0.5) #Reduces bounciness over time
            self.y_pos = ceiling
        self.x_center = self.x_pos+27 #Rough Estimate :)
        self.y_center = self.y_pos+38 #Rough Estimate :| (it's a ball... why is it different??)
        