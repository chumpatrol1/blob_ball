import math
import os
import pygame as pg
cwd = os.getcwd()

def type_to_image(species):
    global cwd
    ball_dir = cwd + "/resources/images/balls/"
    if(species == "soccer_ball"):
        image = ball_dir+"soccer_ball.png"
    elif(species == "p1_token"):
        image = cwd+"/resources/images/p1_token.png"
    elif(species == "p2_token"):
        image = cwd+"/resources/images/p2_token.png"
    elif(species == "kicked_ball"):
        image = ball_dir+"kicked_ball.png"
    elif(species == "blocked_ball"):
        image = ball_dir+"blocked_ball.png"
    elif(species == "goal_ball"):
        image = ball_dir+"goal_ball.png"

    return image

def lineFromPoints(P, Q, D, E):
        #P is point A, Q is point B, D is an X coordinate, E is a y coordinate
        a = Q[1] - P[1]
        b = P[0] - Q[0]
        c = a*(P[0]) + b*(P[1])
        try:
            return -1 * (a*D - c)/b
        except:
            return 0

class Ball:
    def __init__(self, species = "soccer_ball", x_pos = 902, y_pos = 900):
        self.species = species
        self.image = type_to_image(species)
        self.x_speed = 0
        self.y_speed = 0
        self.speed = 0
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
        self.goal_grounded = False #True if the ball is rolling along the goal
        self.special_timer = 0 #Used when the ball is hit with a kick or block
        #Stores 10 afterimages
        self.previous_locations = []
        for i in range(10):
            #First number is X position, second is Y, third is ball speed, 4th is ball image, 5th is p1 ability, 6th is p2 ability
            self.previous_locations.append((902, 900, 0, "soccer_ball", "none", "none"))
        self.info = {
            'blob_standard_collisions': 0,
            'blob_reflect_collisions': 0,
            'blob_warp_collisions': 0,
            'kicked': 0,
            'blocked': 0,
            'x_distance_moved': 0,
            'y_distance_moved': 0,
            'floor_collisions': 0,
            'wall_collisions': 0,
            'ceiling_collisions': 0,
            'goal_collisions': 0,
        }
    
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

        ball_vector = pg.math.Vector2(self.x_center, self.y_center)
        p1_vector = pg.math.Vector2(blob.x_center, blob.y_center)
        
        if(blob.collision_timer == 0):
            if(blob.y_center < (self.y_center - 35)): #Is the slime way above the ball?
                if(abs(blob.x_center - self.x_center) < blob_collision_distance):
                    pass
            elif(blob.y_center < (self.y_center)): #Is the slime low enough to interact with the ball?
                if(abs(blob.x_center - self.x_center) <= blob_collision_distance) and self.grounded and blob.y_speed >= 0:
                    #True if x is close enough, ball is grounded, hit the bottom, and blob moving downwards
                    self.y_pos = self.y_pos + (p1_center_distance - 160) #Pop the ball upwards
                    self.y_speed = -5
                    self.x_speed = 0
                    blob.collision_timer = 0
                    self.info['blob_warp_collisions'] += 1
                elif(abs(blob.x_center - self.x_center) <= blob_collision_distance) and not self.grounded:
                    #True if x is close enough, and ball is airborne.
                    if(self.y_speed < 0): #Are we moving upwards?
                        self.y_speed = (-1 * self.y_speed) + blob.y_speed # Reflect!
                        blob.collision_timer = 10
                        if(blob.y_speed >= 0 and blob.y_pos >= 1100):
                            self.y_pos = self.y_pos + (p1_center_distance - 160)
                            self.y_speed = -5
                            self.x_speed = 0
                            blob.collision_timer = 5
                            self.info['blob_warp_collisions'] += 1
                        else:
                            self.info['blob_reflect_collisions'] += 1

            elif(blob.y_center >= self.y_center): #Is the ball above the blob?
                if(p1_vector.distance_to(ball_vector) < 80):
                    blob.collision_timer = 10
                if p1_vector.distance_to(ball_vector) <= blob_collision_distance and blob.kick_timer > 0:#Kicking the ball
                    self.image = type_to_image('kicked_ball')
                    self.info['kicked'] += 1
                    self.species = "kicked_ball"
                    self.special_timer = 30
                    p1_ball_nv = p1_vector - ball_vector
                    try:
                        p1_ball_collision = pg.math.Vector2(self.x_speed, self.y_speed).reflect(p1_ball_nv).normalize()
                        if(self.x_center > blob.x_center):
                            p1_ball_collision[0] = abs(p1_ball_collision[0])
                        else:
                            p1_ball_collision[0] = -1 * abs(p1_ball_collision[0])
                        blob_kick_x_modifier = 0
                    except: #Stationary ball?
                        p1_ball_collision = pg.math.Vector2(self.x_speed, self.y_speed).reflect(p1_ball_nv)
                        blob_kick_x_modifier = ((self.x_center - blob.x_center)/50) * 10
                    
                    blob_kick_y_modifier = 0#((blob.y_center - self.y_center)/50) * 10 #TODO: Fix for Sponge/Sci Slime
                    self.x_speed, self.y_speed = (40 * p1_ball_collision[0] + blob_kick_x_modifier), (-1 * abs(45 * p1_ball_collision[1] - blob_kick_y_modifier))
                elif p1_vector.distance_to(ball_vector) <= blob_collision_distance and ((self.goal_grounded and blob.y_pos < 875) or not self.goal_grounded): #Standard collision
                    self.info['blob_standard_collisions'] += 1
                    p1_ball_nv = p1_vector - ball_vector
                    p1_ball_collision = pg.math.Vector2(self.x_speed, self.y_speed).reflect(p1_ball_nv)
                    blob_kick_x_modifier = ((self.x_center - blob.x_center)/104) * ((8*blob_collision_distance/104) - 8)
                    blob_kick_y_modifier = ((blob.y_center - self.y_center)/104) * ((8*blob_collision_distance/104) - 8) #TODO: Fix for Sponge/Sci Slime
                    self.x_speed, self.y_speed = (p1_ball_collision[0] + (blob.x_speed * 1.25)) + blob_kick_x_modifier, (1 * p1_ball_collision[1] + ((blob.y_speed - 5) * 1.5)) - blob_kick_y_modifier
                    if p1_vector.distance_to(ball_vector) < blob_collision_distance:
                        #If the ball is stuck inside of the blob for some reason, move it out
                        #THIS CAUSES THE DRIBBLE GLITCH
                        self.x_pos += self.x_speed
                        self.y_pos += self.y_speed
                        
                        pass
            else:
                #Debug
                if(abs(blob.x_center - self.x_center) < blob_collision_distance):
                    pass
                else:
                    self.image = type_to_image("soccer_ball")
        else:
            if(blob.y_center < (self.y_center - 35)): #Is the slime way above the ball?
                if(abs(blob.x_center - self.x_center) < blob_collision_distance):
                    pass
            elif(abs(blob.x_center - self.x_center) < blob_collision_distance) and not self.grounded and p1_vector.distance_to(ball_vector) <= blob_collision_distance:
                #True if x is close enough, and ball is airborne.
                if(self.y_speed < 0): #Are we moving upwards?
                    self.y_pos = self.y_pos + (p1_center_distance - 160)
                    self.y_speed = -5
                    self.x_speed = 0
                    blob.collision_timer = 0
                    self.info['blob_warp_collisions'] += 1
        return blob

    def check_block_collisions(self, blob, other_blob):
        #Checks for block collisions
        if(blob.block_timer >= blob.block_timer_max - 3):
            collision_timer_duration = 30
            #Check for an active block (lasts one frame)
            #outer_intersection = lineFromPoints((self.x_pos, self.y_pos), self.previous_locations[-2], blob.block_outer, 0)
            #inner_intersection = lineFromPoints((self.x_pos, self.y_pos), self.previous_locations[-2], blob.block_inner, 0)
            ball_midpoint = ((self.x_pos + self.previous_locations[-2][0])/2, (self.y_pos + self.previous_locations[-2][1])/2)
            if(blob.facing == "left"):
                #If the blob is facing left
                if((blob.x_center - blob.collision_distance) - blob.block_outer <= self.x_center <= blob.x_center - blob.collision_distance + blob.block_inner):
                    #If the ball is within the x values of the bounding box
                    if((blob.y_center - blob.collision_distance) + blob.block_upper <= self.y_center <= blob.y_center + blob.block_lower):
                        #If the ball is within the y values of the bounding box
                        self.x_speed = 0
                        self.y_speed = -0.9
                        self.image = type_to_image("blocked_ball")
                        self.species = "blocked_ball"
                        self.special_timer = 30
                        blob.collision_timer = collision_timer_duration
                        other_blob.collision_timer = collision_timer_duration
                        #Stops the ball completely
                        if(blob.block_timer == blob.block_timer_max - 3):
                            self.info['blocked'] += 1
                elif((blob.x_center - blob.collision_distance) - blob.block_outer <= ball_midpoint[0] <= blob.x_center - blob.collision_distance + blob.block_inner):
                    #If the ball is within the x values of the bounding box
                    if((blob.y_center - blob.collision_distance) + blob.block_upper <= ball_midpoint[1] <= blob.y_center + blob.block_lower):
                        #If the ball is within the y values of the bounding box
                        self.x_pos = ball_midpoint[0]
                        self.y_pos = ball_midpoint[1]
                        #Teleport the ball to the midpoint
                        self.x_speed = 0
                        self.y_speed = -0.9
                        self.image = type_to_image("blocked_ball")
                        self.species = "blocked_ball"
                        self.special_timer = 30
                        blob.collision_timer = collision_timer_duration
                        other_blob.collision_timer = collision_timer_duration
                        #Stops the ball completely
                        if(blob.block_timer == blob.block_timer_max - 3):
                            self.info['blocked'] += 1
            else:
                #If the blob is facing right
                if(blob.x_center + blob.collision_distance - 25 <= self.x_center <= blob.x_center + blob.collision_distance + 150):
                    #If the ball is within the x values of the bounding box
                    if((blob.y_center - blob.collision_distance) - 200 <= self.y_center <= blob.y_center + 200):
                        #If the ball is within the y values of the bounding box
                        self.x_speed = 0
                        self.y_speed = -0.9
                        self.image = type_to_image("blocked_ball")
                        self.species = "blocked_ball"
                        self.special_timer = 30
                        blob.collision_timer = collision_timer_duration
                        other_blob.collision_timer = collision_timer_duration
                        #Stops the ball completely
                        if(blob.block_timer == blob.block_timer_max - 3):
                            self.info['blocked'] += 1
                elif(blob.x_center + blob.collision_distance - 25 <= ball_midpoint[0] <= blob.x_center + blob.collision_distance + 150):
                    #If the ball is within the x values of the bounding box
                    if((blob.y_center - blob.collision_distance) - 200 <= ball_midpoint[1] <= blob.y_center + 200):
                        #If the ball is within the y values of the bounding box
                        self.x_pos = ball_midpoint[0]
                        self.y_pos = ball_midpoint[1]
                        #If the ball is within the y values of the bounding box
                        self.x_speed = 0
                        self.y_speed = -0.9
                        self.image = type_to_image("blocked_ball")
                        self.species = "blocked_ball"
                        self.special_timer = 30
                        blob.collision_timer = collision_timer_duration
                        other_blob.collision_timer = collision_timer_duration
                        #Stops the ball completely
                        if(blob.block_timer == blob.block_timer_max - 3):
                            self.info['blocked'] += 1
        return blob, other_blob

    def check_blob_ability(self, blob):
        if(blob.used_ability == "fireball"):
            self.x_speed *= (1.05 - (self.x_speed/1000))
            self.y_speed *= (1.05 - (self.y_speed/1000))
        elif(blob.used_ability == "snowball"):
            self.x_speed *= .975
            self.y_speed *= (.95 - (self.y_speed/1000))
        elif(blob.used_ability == "geyser"):
            try:
                geyser_power = math.sqrt(Ball.ground - self.y_pos)/4-5
                if(geyser_power < 0.8 and self.y_speed > -25):
                    self.y_speed += geyser_power
                    if(self.y_speed > 0):
                        self.y_speed += geyser_power #Effectively, it's twice as powerful
                else:
                    self.y_speed -= 0.8
            except Exception as exception:
                print(exception)
                self.y_speed -= 5
        elif(blob.used_ability == "spire" and blob.special_ability_timer == blob.special_ability_cooldown_max - blob.special_ability_delay and self.y_pos >= 900):
            self.y_speed = -50
        elif(blob.used_ability == "thunderbolt" and blob.special_ability_timer == blob.special_ability_cooldown_max - blob.special_ability_delay):
            self.y_speed = Ball.ground - self.y_pos
        elif(blob.used_ability == "gale" and not blob.collision_timer):
            if(blob.player == 1 and self.x_speed < 15):
                self.x_speed += 0.25
            elif(blob.player == 2 and self.x_speed > -15):
                self.x_speed -= 0.25

    def move(self, p1_blob, p2_blob):
        ground = Ball.ground
        left_wall = 0
        right_wall = 1805
        left_goal = 140
        right_goal = 1665
        ceiling = 200
        goal_top = 825
        goal_bottom = 950

        self.previous_locations.append((self.x_pos, self.y_pos, self.speed, self.species, p1_blob.used_ability, p2_blob.used_ability))
        self.previous_locations = self.previous_locations[1:]

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
        if(self.x_pos < left_goal or self.x_pos > right_goal):
            if(self.x_pos < left_goal):
                side_intersection = lineFromPoints((self.x_pos, self.y_pos), self.previous_locations[-2], left_goal, 0)
                if(left_goal < left_goal - self.x_speed and goal_top <= self.y_pos <= goal_bottom and goal_top < side_intersection < goal_bottom): #Hit side of goalpoast
                    self.info['goal_collisions'] += 1
                    self.x_pos = left_goal + 1
                    if(self.x_speed < 0):
                        self.x_speed = self.x_speed * -0.5
                elif(self.y_pos - self.y_speed > goal_bottom > self.y_pos and self.y_speed < 0): #Hit bottom of goalpost
                    self.info['goal_collisions'] += 1
                    self.y_pos = goal_bottom
                    if(self.y_speed < 0):
                        self.y_speed = self.y_speed * -0.5
                elif(self.y_pos - self.y_speed < goal_top < self.y_pos + 1 and (self.y_speed >= 0  or self.species == "blocked_ball")): #Hit top of goalpost
                    self.y_pos = goal_top - self.gravity
                    self.x_speed += 0.5
                    self.goal_grounded = True
                    if(self.y_speed >= 0):
                        self.info['goal_collisions'] += 1
                        self.y_speed = self.y_speed * -0.5
                        if(p1_blob.species == "lightning" or p2_blob.species == "lightning"):
                            for previous_location in self.previous_locations:
                                if(previous_location[4] == "thunderbolt" or previous_location[5] == "thunderbolt"):
                                    self.y_speed = self.y_speed * 0.3
                                    break
                else:
                    self.goal_grounded = False

            if(self.x_pos > right_goal):
                side_intersection = lineFromPoints((self.x_pos, self.y_pos), self.previous_locations[-2], right_goal, 0)        
                if(right_goal > right_goal - self.x_speed and goal_top <= self.y_pos <= goal_bottom and goal_top < side_intersection < goal_bottom): #Hit side of goalpoast
                    self.info['goal_collisions'] += 1
                    self.x_pos = right_goal - 1
                    if(self.x_speed > 0):
                        self.x_speed = self.x_speed * -0.5
                elif(self.y_pos - self.y_speed > goal_bottom > self.y_pos and self.y_speed < 0): #Hit bottom of goalpost
                    self.info['goal_collisions'] += 1
                    self.y_pos = goal_bottom
                    if(self.y_speed < 0):
                        self.y_speed = self.y_speed * -0.5
                elif(self.y_pos - self.y_speed < goal_top < self.y_pos + 1 and (self.y_speed >= 0  or self.species == "blocked_ball")): #Hit top of goalpost
                    self.y_pos = goal_top - self.gravity
                    self.x_speed -= 0.5
                    self.goal_grounded = True
                    if(self.y_speed >= 0):
                        self.info['goal_collisions'] += 1
                        self.y_speed = self.y_speed * -0.5
                        if(p1_blob.species == "lightning" or p2_blob.species == "lightning"):
                            for previous_location in self.previous_locations:
                                if(previous_location[4] == "thunderbolt" or previous_location[5] == "thunderbolt"):
                                    self.y_speed = self.y_speed * 0.3
                                    break
                else:
                    self.goal_grounded = False
        else:
            self.goal_grounded = False

        #Interacting with the walls
        if(self.x_pos < left_wall): #Hit side of the wall
            self.info['wall_collisions'] += 1
            self.x_pos = left_wall
            if(self.x_speed < 0):
                self.x_speed = self.x_speed * -0.5

        if(self.x_pos > right_wall):
            self.info['wall_collisions'] += 1
            self.x_pos = right_wall
            if(self.x_speed > 0):
                self.x_speed = self.x_speed * -0.5
        #Speed Limits (X)
        if(self.x_speed > self.x_speed_max):
            self.x_speed = self.x_speed_max
        elif(self.x_speed < -1 * self.x_speed_max):
            self.x_speed = -1 * self.x_speed_max
        self.x_pos += self.x_speed
        self.info['x_distance_moved'] += abs(self.x_speed)

        #Interacting with the ground
        if(self.y_pos < ground):
            self.y_speed += self.gravity
        elif(self.y_pos >= ground): #Don't go under the floor!
            if(2 >= self.y_speed >= 0 or self.species == "blocked_ball"):
                self.y_speed = 0
            elif(self.y_speed < 0 ):
                pass
            else:
                self.y_speed = -1 * math.floor(self.y_speed * 0.75)
                self.info['floor_collisions'] += 1
                if(p1_blob.species == "lightning" or p2_blob.species == "lightning"):
                    for previous_location in self.previous_locations:
                        if(previous_location[4] == "thunderbolt" or previous_location[5] == "thunderbolt"):
                            self.y_speed = self.y_speed * 0.3
                            break
                            

                
                 #Reduces bounciness over time
            self.y_pos = ground
            
        if(self.y_pos < ceiling): #Don't raze the roof!
            self.info['ceiling_collisions'] += 1
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
        self.info['y_distance_moved'] += abs(self.y_speed)
        self.speed = math.sqrt(self.x_speed ** 2 + self.y_speed **2)

        self.x_center = self.x_pos+27 #Rough Estimate :)
        self.y_center = self.y_pos+38 #Rough Estimate :| (it's a ball... why is it different??)
        if(self.special_timer > 0):
            self.special_timer -= 1
            if(self.special_timer == 0):
                self.image = type_to_image('soccer_ball')
                self.species = "soccer_ball"
        