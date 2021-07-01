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
    elif(type == "kicked_ball"):
        image = cwd+"\\resources\\images\\kicked_ball.png"
    elif(type == "blocked_ball"):
        image = cwd+"\\resources\\images\\blocked_ball.png"

    return image

class ball:
    def __init__(self, type = "soccer_ball", x_pos = 902, y_pos = 900):
        self.type = type
        self.image = type_to_image(type)
        self.x_speed = 0
        self.y_speed = 0
        self.x_speed_max = 50
        self.y_speed_max = 50
        self.x_pos = x_pos #Ball's position
        self.x_center = x_pos + 27
        self.y_center = y_pos + 38
        self.y_pos = y_pos #Ball's position
        self.traction = 0.15 #Ground Traction
        self.friction = 0.1 #Air Friction
        self.gravity = 0.9
        self.grounded = False #True if the ball is on the ground
        self.special_timer = 0 #Used when the ball is hit with a kick or block
    
    ground = 1240

    def reset(self):
        self.x_speed = 0
        self.y_speed = 0
        self.x_pos = 902
        self.y_pos  = 900
        self.image = type_to_image("soccer_ball")

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
                    pass
            elif(blob.y_center < (self.y_center)): #Is the slime low enough to interact with the ball?
                if(abs(blob.x_center - self.x_center) < blob_collision_distance) and self.grounded and blob.y_speed >= 0:
                    #True if x is close enough, ball is grounded, hit the bottom, and blob moving downwards
                    self.y_pos = self.y_pos + (p1_center_distance - 160) #Pop the ball upwards
                    self.y_speed = -5
                    self.x_speed = 0
                    blob.collision_timer = 5
                elif(abs(blob.x_center - self.x_center) < blob_collision_distance) and not self.grounded:
                    #True if x is close enough, and ball is airborne.
                    if(self.y_speed < 0): #Are we moving upwards?
                        self.y_speed = (-1 * self.y_speed) + blob.y_speed # Reflect!
                        blob.collision_timer = 10
                        if(blob.y_speed >= 0 and blob.y_pos >= 1100):
                            self.y_pos = ball.ground + (p1_center_distance - 160)
                            self.y_speed = -5
                            self.x_speed = 0


            elif(blob.y_center >= self.y_center): #Is the ball above the blob?
                if(p1_vector.distance_to(ball_vector) < 80):
                    blob.collision_timer = 10
                if p1_vector.distance_to(ball_vector) <= blob_collision_distance: #Standard collision
                    p1_ball_nv = p1_vector - ball_vector
                    p1_ball_collision = pg.math.Vector2(self.x_speed, self.y_speed).reflect(p1_ball_nv)
                    blob_kick_x_modifier = ((self.x_center - blob.x_center)/104) * ((8*blob_collision_distance/104) - 8)
                    blob_kick_y_modifier = ((blob.y_center - self.y_center)/104) * ((8*blob_collision_distance/104) - 8) #TODO: Fix for Sponge/Sci Slime
                    self.x_speed, self.y_speed = (p1_ball_collision[0] + (blob.x_speed * 1.25)) + blob_kick_x_modifier, (1 * p1_ball_collision[1] + ((blob.y_speed - 5) * 1.5)) - blob_kick_y_modifier
                    if p1_vector.distance_to(ball_vector) < blob_collision_distance:
                        #If the ball is stuck inside of the blob for some reason, move it out
                        self.x_pos += self.x_speed
                        self.y_pos += self.y_speed
                    if(blob.kick_timer > 0):
                        self.image = type_to_image('kicked_ball')
                        self.special_timer = 30
            else:
                #Debug
                if(abs(blob.x_center - self.x_center) < blob_collision_distance):
                    pass
                else:
                    self.image = type_to_image("soccer_ball")

    def check_block_collisions(self, blob, other_blob):
        #Checks for block collisions
        if(blob.block_timer == blob.block_timer_max):
            #Check for an active block (lasts one frame)
            if(blob.facing == "left"):
                #If the blob is facing left
                if((blob.x_center - blob.collision_distance) - 150 <= self.x_center <= blob.x_center - blob.collision_distance + 25):
                    #If the ball is within the x values of the bounding box
                    if((blob.y_center - blob.collision_distance) - 200 <= self.y_center <= blob.y_center + 200):
                        #If the ball is within the y values of the bounding box
                        self.x_speed = 0
                        self.y_speed = 0
                        self.image = type_to_image("blocked_ball")
                        self.special_timer = 30
                        blob.collision_timer = 3
                        other_blob.collision_timer = 3
                        #Stops the ball completely
            else:
                #If the blob is facing right
                if(blob.x_center + blob.collision_distance - 25 <= self.x_center <= blob.x_center + blob.collision_distance + 150):
                    #If the ball is within the x values of the bounding box
                    if((blob.y_center - blob.collision_distance) - 200 <= self.y_center <= blob.y_center + 200):
                        #If the ball is within the y values of the bounding box
                        self.x_speed = 0
                        self.y_speed = 0
                        self.image = type_to_image("blocked_ball")
                        self.special_timer = 30
                        blob.collision_timer = 3
                        other_blob.collision_timer = 3
                        #Stops the ball completely
    
    def move(self):
        ground = ball.ground
        left_wall = 0
        right_wall = 1805
        left_goal = 140
        right_goal = 1665
        ceiling = 200
        goal_top = 825
        goal_bottom = 950

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
        #Interacting with the goalposts
        if(self.x_pos < left_goal < left_goal - self.x_speed and goal_top <= self.y_pos <= goal_bottom): #Hit side of goalpoast
            self.x_pos = left_goal + 1
            if(self.x_speed < 0):
                self.x_speed = self.x_speed * -0.5
        elif(self.x_pos < left_goal and self.y_pos - self.y_speed > goal_bottom > self.y_pos and self.y_speed < 0): #Hit bottom of goalpost
            self.y_pos = goal_bottom
            if(self.y_speed < 0):
                self.y_speed = self.y_speed * -0.5
        elif(self.x_pos < left_goal and self.y_pos - self.y_speed < goal_top < self.y_pos and self.y_speed >= 0): #Hit bottom of goalpost
            self.y_pos = goal_top - 1
            self.x_speed += 0.5
            if(self.y_speed >= 0):
                self.y_speed = self.y_speed * -0.5
        
        if(self.x_pos > right_goal > right_goal - self.x_speed and goal_top <= self.y_pos <= goal_bottom): #Hit side of goalpoast
            self.x_pos = right_goal - 1
            if(self.x_speed > 0):
                self.x_speed = self.x_speed * -0.5
        elif(self.x_pos > right_goal and self.y_pos - self.y_speed > goal_bottom > self.y_pos and self.y_speed < 0): #Hit bottom of goalpost
            self.y_pos = goal_bottom
            if(self.y_speed < 0):
                self.y_speed = self.y_speed * -0.5
        elif(self.x_pos > right_goal and self.y_pos - self.y_speed < goal_top < self.y_pos and self.y_speed >= 0): #Hit bottom of goalpost
            self.y_pos = goal_top - 1
            self.x_speed -= 0.5
            if(self.y_speed >= 0):
                self.y_speed = self.y_speed * -0.5

        #Interacting with the walls
        if(self.x_pos < left_wall): #Hit side of goalpoast
            self.x_pos = left_wall
            if(self.x_speed < 0):
                self.x_speed = self.x_speed * -0.5

        if(self.x_pos > right_wall):
            self.x_pos = right_wall
            if(self.x_speed > 0):
                self.x_speed = self.x_speed * -0.5
        #Speed Limits (X)
        if(self.x_speed > self.x_speed_max):
            self.x_speed = self.x_speed_max
        elif(self.x_speed < -1 * self.x_speed_max):
            self.x_speed = -1 * self.x_speed_max
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
                self.y_speed = math.floor(self.y_speed * -0.3) #Reduces bounciness over time
            self.y_pos = ceiling
        if(self.y_speed > self.y_speed_max):
            self.y_speed = self.y_speed_max
        elif(self.y_speed < -1 * self.y_speed_max):
            self.y_speed = -1 * self.y_speed_max
        self.y_pos += self.y_speed

        self.x_center = self.x_pos+27 #Rough Estimate :)
        self.y_center = self.y_pos+38 #Rough Estimate :| (it's a ball... why is it different??)

        if(self.special_timer > 0):
            self.special_timer -= 1
            if(self.special_timer == 0):
                self.image = type_to_image('soccer_ball')
        