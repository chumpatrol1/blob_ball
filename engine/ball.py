from cmath import sqrt
import math
import os
import pygame as pg
from engine.environmental_modifiers import return_environmental_modifiers

from resources.sound_engine.sfx_event import createSFXEvent
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
    def __init__(self, species = "soccer_ball", x_pos = 902, y_pos = 900, x_speed = 0, y_speed = 0, id = 0):
        self.species = species
        self.image = type_to_image(species)
        self.id = id
        self.all_blobs = {}
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.speed = 0
        self.x_speed_max = 50
        self.y_speed_max = 50
        self.bounciness = 1
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
        self.blocked_timer = 0
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
        self.status_effects = {
            'glued': 0,
            'zapped': 0,
            'bubbled': 0,
        }
        self.bubble = None
    
    ground = 1240

    def reset(self):
        self.x_speed = 0
        self.y_speed = 0
        self.x_pos = 902
        self.y_pos  = 900
        self.image = type_to_image("soccer_ball")
        for effect in self.status_effects:
            self.status_effects[effect] = 0

    def check_blob_collisions(self):
        #The distance to p1's blob
        for blob in self.all_blobs.values():
            p1_center_distance = round(math.sqrt((blob.x_center - self.x_center)**2 + (blob.y_center - self.y_center)**2),1)
            blob_collision_distance = blob.collision_distance
            #X distance used for calculations. If the distance between centers is less than this, a collision can happen

            ball_vector = pg.math.Vector2(self.x_center, self.y_center)
            p1_vector = pg.math.Vector2(blob.x_center, blob.y_center)
            
            if(not blob.collision_timer and not blob.status_effects['stoplit']):
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
                        self.update_bubble_status(None)
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
                                createSFXEvent('ball_blob_bounce', volume_modifier = ((self.x_speed**2 +self.y_speed**2)/(self.x_speed_max**2 + self.y_speed_max**2))**(1/3))
                            self.update_bubble_status(None)

                elif(blob.y_center >= self.y_center): #Is the ball above the blob?
                    if(p1_vector.distance_to(ball_vector) < 80):
                        blob.collision_timer = 10
                    if p1_vector.distance_to(ball_vector) <= blob_collision_distance and ((self.goal_grounded and blob.y_pos < 875) or not self.goal_grounded) and blob.kick_timer > 0:#Kicking the ball
                        self.image = type_to_image('kicked_ball')
                        self.info['kicked'] += 1
                        self.species = "kicked_ball"
                        self.special_timer = 30

                        try:
                            # Make this not dependent on ball speed!
                            #p1_ball_collision = pg.math.Vector2(self.x_speed, self.y_speed).reflect(p1_ball_nv)
                            p1_ball_collision = p1_vector - ball_vector
                            if(self.x_center > blob.x_center):
                                p1_ball_collision[0] = abs(p1_ball_collision[0])
                                
                            else:
                                p1_ball_collision[0] = -1 * abs(p1_ball_collision[0])
                            
                            
                            blob_kick_x_modifier = 0
                            p1_ball_collision.scale_to_length(50)
                        except: #Stationary ball?
                            p1_ball_collision = pg.math.Vector2(self.x_speed, self.y_speed).reflect(p1_vector - ball_vector)
                            blob_kick_x_modifier = ((self.x_center - blob.x_center)/50) * 10
                        
                        #print(ball_vector, p1_vector, p1_ball_collision, p1_ball_nv)
                        blob_kick_y_modifier = 0#((blob.y_center - self.y_center)/50) * 10 #TODO: Fix for Sponge/Sci Slime
                        self.x_speed, self.y_speed = (p1_ball_collision[0] + blob_kick_x_modifier), (-1 * abs(p1_ball_collision[1] - blob_kick_y_modifier))
                        #print(self.x_speed, self.y_speed)
                        createSFXEvent('ball_blob_bounce', volume_modifier = ((self.x_speed**2 +self.y_speed**2)/(self.x_speed_max**2 + self.y_speed_max**2))**(1/3))
                        self.x_speed *= self.bounciness
                        self.y_speed *= self.bounciness
                        for other_blob in blob.all_blobs.values():
                            if(other_blob.special_ability == "hook" and other_blob.special_ability_timer):
                                other_blob.status_effects['silenced'] += 360
                        self.update_bubble_status(None)
                        #print("speed", p1_ball_collision, "loc diff", p1_ball_nv)
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
                        self.x_speed *= self.bounciness
                        self.y_speed *= self.bounciness
                        
                        createSFXEvent('ball_blob_bounce', volume_modifier = ((self.x_speed**2 + self.y_speed**2)/(self.x_speed_max**2 + self.y_speed_max**2))**(1/3))
                        self.update_bubble_status(None)
                else:
                    #Debug
                    if(abs(blob.x_center - self.x_center) < blob_collision_distance):
                        pass
                    else:
                        self.image = type_to_image("soccer_ball")
            elif(blob.status_effects['stoplit']):
                pass
            else:
                if(blob.y_center < (self.y_center - 35)): #Is the slime way above the ball?
                    if(abs(blob.x_center - self.x_center) < blob_collision_distance):
                        pass
                elif(abs(blob.x_center - self.x_center) < blob_collision_distance) and not self.grounded and p1_vector.distance_to(ball_vector) <= blob_collision_distance:
                    #True if x is close enough, and ball is airborne.
                    if(self.y_speed < 0): #Are we moving upwards?
                        #print('warp')
                        self.y_pos = self.y_pos + (p1_center_distance - 160)
                        self.y_speed = -5
                        self.x_speed = 0
                        blob.collision_timer = 0
                        self.info['blob_warp_collisions'] += 1
                    self.update_bubble_status(None)
            self.check_ceiling_collisions()

    def check_block_collisions(self):
        #Checks for block collisions
        for blob in self.all_blobs.values():
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
                            self.get_blocked(collision_timer_duration, blob)
                    elif((blob.x_center - blob.collision_distance) - blob.block_outer <= ball_midpoint[0] <= blob.x_center - blob.collision_distance + blob.block_inner):
                        #If the ball is within the x values of the bounding box
                        if((blob.y_center - blob.collision_distance) + blob.block_upper <= ball_midpoint[1] <= blob.y_center + blob.block_lower):
                            #If the ball is within the y values of the bounding box
                            self.x_pos = ball_midpoint[0]
                            self.y_pos = ball_midpoint[1]
                            self.get_blocked(collision_timer_duration, blob)
                else:
                    #If the blob is facing right
                    if(blob.x_center + blob.collision_distance - 25 <= self.x_center <= blob.x_center + blob.collision_distance + 150):
                        #If the ball is within the x values of the bounding box
                        if((blob.y_center - blob.collision_distance) - 200 <= self.y_center <= blob.y_center + 200):
                            #If the ball is within the y values of the bounding box
                            self.get_blocked(collision_timer_duration, blob)
                    elif(blob.x_center + blob.collision_distance - 25 <= ball_midpoint[0] <= blob.x_center + blob.collision_distance + 150):
                        #If the ball is within the x values of the bounding box
                        if((blob.y_center - blob.collision_distance) - 200 <= ball_midpoint[1] <= blob.y_center + 200):
                            #If the ball is within the y values of the bounding box
                            self.x_pos = ball_midpoint[0]
                            self.y_pos = ball_midpoint[1]
                            self.get_blocked(collision_timer_duration, blob)
        self.check_ceiling_collisions()

    def get_blocked(self, collision_timer_duration, blob):
        #If the ball is within the y values of the bounding box
        self.x_speed = 0
        self.y_speed = 0
        self.image = type_to_image("blocked_ball")
        self.species = "blocked_ball"
        self.special_timer = 30
        blob.collision_timer = collision_timer_duration - 20
        for other_blob in blob.all_blobs.values():
            if(other_blob.player != blob.player):
                other_blob.collision_timer = collision_timer_duration
            if(other_blob.special_ability == "hook" and other_blob.special_ability_timer):
                other_blob.status_effects['silenced'] += 360
        #Stops the ball completely
        if(blob.block_timer == blob.block_timer_max - 3):
            self.info['blocked'] += 1
        self.bounciness = 0.1
        self.blocked_timer = 20
        self.update_bubble_status(None)

    def check_blob_ability(self):
        for blob in self.all_blobs.values():
            if("fireball" in blob.used_ability):
                self.x_speed *= (1.05 - (self.x_speed/1000))
                self.y_speed *= (1.05 - (self.y_speed/1000))
            elif("snowball" in blob.used_ability):
                self.x_speed *= .975
                self.y_speed *= (.9 - (self.y_speed/1000))
            elif("geyser" in blob.used_ability):
                try:
                    geyser_power = math.sqrt(Ball.ground - self.y_pos)/4-5
                    if(geyser_power < 0.8 and self.y_speed > -25):
                        self.y_speed += geyser_power
                        if(self.y_speed > 0):
                            self.y_speed += geyser_power #Effectively, it's twice as powerful
                    else:
                        self.y_speed -= 0.8
                except Exception as exception:
                    self.y_speed -= 5
            elif("gale" in blob.used_ability and not blob.collision_timer):
                if(blob.player == 1 and self.x_speed < 15):
                    self.x_speed += 0.4
                elif(blob.player == 2 and self.x_speed > -15):
                    self.x_speed -= 0.4
            elif("stoplight" in blob.used_ability):
                self.x_speed = 0
                self.y_speed = 0
                self.image = type_to_image("blocked_ball")
                self.species = "blocked_ball"
                self.special_timer = 30
                for other_blob in blob.all_blobs.values():
                    if(other_blob.special_ability == "hook" and blob.special_ability_timer):
                        other_blob.special_ability_timer = 1
            elif("mirror" in blob.used_ability):
                self.x_speed *= -0.9
                self.y_speed *= -0.5
            elif("hook" in blob.used_ability):
                if(blob.ability_holding_timer > blob.special_ability_delay and not self.species == "blocked_ball"):
                    # After the delay, start reeling the ball in. This is a gradual
                    # process, meaning that the ball won't get jerked in a certain
                    # direction and it also allows for the ball to be body blocked
                    #print((blob.x_center - 25 - self.x_pos)//150)
                    x_dir = 0
                    hook_dir = 0

                    if(blob.x_center - self.x_pos != 0):
                        hook_dir = abs(blob.x_center - self.x_pos)/(blob.x_center - self.x_pos)
                    else:
                        hook_dir = 1

                    if(self.x_speed != 0):
                        x_dir = abs(self.x_speed)/self.x_speed
                    else:
                        x_dir = hook_dir
                    
                    if(x_dir != hook_dir or abs(self.x_speed) < 15):
                        self.x_speed += (blob.x_center - self.x_pos)//150

                    if(self.y_speed < 5):
                        self.y_speed += (blob.y_center - 200 - self.y_pos)//200
                    '''if(abs(self.x_speed) > 5):
                        self.x_speed *= 0.95'''
                    # Change the number after // - bigger means the pulling force is weaker
                elif(not self.species == "blocked_ball"):
                    x_dist = (self.x_center - blob.x_center)**2
                    y_dist = (self.y_center - blob.y_center)**2
                    t_dist = math.sqrt(x_dist + y_dist)
                    #print(t_dist)
                    if(t_dist < 500):
                        blob.ability_holding_timer += 1
                    '''
                    pull_force_x = math.sqrt(abs(blob.x_center - 25 - self.x_pos))
                    try:
                        pull_sign_x = (blob.x_center - 25 - self.x_pos)/abs(blob.x_center - 25 - self.x_pos)
                    except:
                        pull_sign_x = 1
                    pull_force_y = math.sqrt(abs(blob.y_center - 200 - self.y_pos))
                    try:
                        pull_sign_y = (blob.y_center - 200 - self.y_pos)/abs(blob.y_center - 200 - self.y_pos)
                    except:
                        pull_sign_y = 1
                    '''
                    #print((pull_force_x * pull_sign_x)/20)
                    #self.x_speed += (pull_force_x * pull_sign_x)/20
                    #self.y_speed += (pull_force_y * pull_sign_y)/20

    def check_environmental_collisions(self, environment):
        
        for hazard in environment['glue_puddle']:
            #print(hazard.player, hazard.affects)
            if("ball" in hazard.affects):
                if(hazard.x_pos - 50 < self.x_pos < hazard.x_pos + 90 and self.y_pos >= Ball.ground):
                    self.status_effects['glued'] = 2
                    break
        
        for hazard in environment['spire_glyph']:
            hazard.x_pos = self.x_pos - 40
        
        for hazard in environment['spire_spike']:
            if("ball" in hazard.affects):
                if(hazard.lifetime == hazard.max_lifetime - 1 and self.y_pos >= 900):
                    createSFXEvent('ball_spire_hit')
                    self.y_speed = -50
        
        for hazard in environment['thunder_glyph']:
            hazard.x_pos = self.x_pos - 40

        for hazard in environment['thunder_bolt']:
            if("ball" in hazard.affects):
                if(hazard.lifetime == hazard.max_lifetime - 1):
                    self.y_speed = Ball.ground - self.y_pos
                    self.status_effects['zapped'] += 120
        
        for hazard in environment['cactus_spike']:
            if("ball" in hazard.affects):
                
                ball_vector = pg.math.Vector2(self.x_center, self.y_center + 50)
                hazard_vector = pg.math.Vector2(hazard.x_pos, hazard.y_pos + 20)

                #print("X", hazard.x_pos, self.x_pos)
                #print("Y", hazard.y_pos, self.y_pos)
                
                dist_vector = hazard_vector.distance_to(ball_vector)
                if(dist_vector < 75):
                    try:
                        hazard.lifetime = 0
                        ball_nv = pg.math.Vector2(self.x_pos - hazard.x_pos, (self.y_pos + 50) - hazard.y_pos)
                        ball_nv.scale_to_length(20)
                        if(not self.species == "blocked_ball"):
                            self.x_speed = ball_nv[0]
                            self.y_speed = ball_nv[1]
                    except:
                        hazard.lifetime = 0
                        if(not self.species == "blocked_ball"):
                            self.x_speed = 0
                            self.y_speed = -10

                    continue

                
                hazard_nv = hazard_vector - ball_vector
                if(dist_vector > 150):
                    hazard_nv.scale_to_length(25)
                else:
                    hazard_nv.scale_to_length(20)
                hazard.x_pos -= hazard_nv[0]
                hazard.y_pos -= hazard_nv[1] * 2
                #print(hazard_nv.length())

        for hazard in environment['bubble']:
            if("ball" in hazard.affects):
                ball_vector = pg.math.Vector2(self.x_center, self.y_center)
                hazard_vector = pg.math.Vector2(hazard.x_pos + 60, hazard.y_pos + 60)

                #print("X", hazard.x_pos, self.x_pos)
                #print("Y", hazard.y_pos, self.y_pos)
                
                dist_vector = hazard_vector.distance_to(ball_vector)
                #print(dist_vector, self.y_center, hazard.y_pos + 60)
                if(dist_vector < 135):
                    try:
                        #hazard.lifetime = 0
                        #ball_nv = pg.math.Vector2(self.x_pos - hazard.x_pos, (self.y_pos + 50) - hazard.y_pos)
                        #ball_nv.scale_to_length(20)
                        #if(not self.species == "blocked_ball"):
                            #self.x_speed = ball_nv[0]
                            #self.y_speed = ball_nv[1]
                        self.x_speed = 0
                        self.y_speed = 0
                        self.x_pos = hazard.x_pos + 60 - 5
                        self.y_pos = hazard.y_pos + 30
                        self.status_effects['bubbled'] = hazard.lifetime
                        #print("TRY", self.y_center - (hazard.y_pos + 60))
                    except:
                        #hazard.lifetime = 0
                        if(not self.species == "blocked_ball"):
                            self.x_speed = 0
                            self.y_speed = -10
                            self.x_pos = hazard.x_pos + 60 - 5
                            self.y_pos = hazard.y_pos + 30
                            self.status_effects['bubbled'] = hazard.lifetime
                            #print("EXCEPTION", self.y_center - (hazard.y_pos + 60))
                    
                    if(self.bubble != hazard):
                        self.update_bubble_status(hazard)

                    continue



                


    def check_ceiling_collisions(self):
        ceiling = 210
        if(self.y_pos < ceiling): #Don't raze the roof!
            self.info['ceiling_collisions'] += 1
            if(self.y_speed > -4):
                self.y_speed = 0
            else:
                self.y_speed = math.floor(self.y_speed * -0.3) #Reduces bounciness over time
            createSFXEvent('ball_metal_bounce', volume_modifier=(math.sqrt(abs(self.y_speed/self.y_speed_max))))
            self.y_pos = ceiling

    def move(self): # Also has cooldowns in it.
        ground = Ball.ground
        left_wall = 0
        right_wall = 1805
        left_goal = 140
        right_goal = 1665
        ceiling = 200
        goal_top = 825
        goal_bottom = 950

        self.previous_locations.append((self.x_pos, self.y_pos, self.speed, self.species))
        self.previous_locations = self.previous_locations[1:]

        #Traction/Friction
        def apply_traction_friction():
            ball_traction = self.traction
            if(self.status_effects['glued']):
                #self.image = type_to_image('kicked_ball')
                #self.species = "kicked_ball"
                #self.special_timer = 10
                ball_traction += 0.2
            if(self.y_pos == ground):
                self.grounded = True
                if(self.x_speed < 0): #If we're going left, decelerate
                    if(self.x_speed + ball_traction) > 0:
                        self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                    else:
                        self.x_speed += ball_traction #Normal deceleration
                elif(self.x_speed > 0):
                    if(self.x_speed - ball_traction) < 0:
                        self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                    else:
                        self.x_speed -= ball_traction #Normal deceleration
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
        def interact_with_goal_posts():
            if(self.x_pos < left_goal or self.x_pos > right_goal):
                if(self.x_pos < left_goal): # Left Goal
                    side_intersection = lineFromPoints((self.x_pos, self.y_pos), self.previous_locations[-2], left_goal, 0)
                    if(left_goal < left_goal - self.x_speed and goal_top <= self.y_pos <= goal_bottom and goal_top < side_intersection < goal_bottom): #Hit side of goalpoast
                        self.info['goal_collisions'] += 1
                        self.x_pos = left_goal + 1
                        if(self.x_speed < 0):
                            self.x_speed = self.x_speed * -0.5
                        createSFXEvent('ball_metal_bounce', volume_modifier = math.sqrt(self.x_speed/self.x_speed_max))
                    elif(self.y_pos - self.y_speed > goal_bottom > self.y_pos and self.y_speed < 0): #Hit bottom of goalpost
                        self.info['goal_collisions'] += 1
                        self.y_pos = goal_bottom
                        if(self.y_speed < 0):
                            self.y_speed = self.y_speed * -0.5
                        createSFXEvent('ball_metal_bounce', volume_modifier = math.sqrt(abs(self.x_speed/self.x_speed_max)))
                    elif(self.y_pos - self.y_speed < goal_top < self.y_pos + 1 and (self.y_speed >= 0  or self.species == "blocked_ball")): #Hit top of goalpost
                        self.y_pos = goal_top - self.gravity
                        self.x_speed += 0.5
                        self.goal_grounded = True
                        if(self.y_speed >= 0):
                            self.info['goal_collisions'] += 1
                            self.y_speed = self.y_speed * -0.5
                            if(self.y_speed >= 2):
                                createSFXEvent('ball_metal_bounce', volume_modifier = math.sqrt(abs(self.y_speed/self.y_speed_max)))
                            if(self.status_effects['zapped']):
                                self.y_speed = self.y_speed * 0.3
                    else:
                        self.goal_grounded = False
                    if(goal_top < self.y_pos < goal_top + 1 and self.y_speed >= 0):
                        self.y_pos = goal_top - self.gravity
                

                if(self.x_pos > right_goal): # Right goal
                    side_intersection = lineFromPoints((self.x_pos, self.y_pos), self.previous_locations[-2], right_goal, 0)
                    if(right_goal > right_goal - self.x_speed and goal_top <= self.y_pos <= goal_bottom and goal_top < side_intersection < goal_bottom): #Hit side of goalpoast
                        self.info['goal_collisions'] += 1
                        self.x_pos = right_goal - 1
                        if(self.x_speed > 0):
                            self.x_speed = self.x_speed * -0.5
                        createSFXEvent('ball_metal_bounce', volume_modifier = math.sqrt(abs(self.x_speed/self.x_speed_max)))
                    elif(self.y_pos - self.y_speed > goal_bottom > self.y_pos and self.y_speed < 0): #Hit bottom of goalpost
                        self.info['goal_collisions'] += 1
                        self.y_pos = goal_bottom
                        if(self.y_speed < 0):
                            self.y_speed = self.y_speed * -0.5
                        createSFXEvent('ball_metal_bounce', volume_modifier = math.sqrt(abs(self.y_speed/self.y_speed_max)))
                    elif(self.y_pos - self.y_speed < goal_top < self.y_pos + 1 and (self.y_speed >= 0  or self.species == "blocked_ball")): #Hit top of goalpost
                        self.y_pos = goal_top - self.gravity
                        self.x_speed -= 0.5
                        self.goal_grounded = True
                        if(self.y_speed >= 0):
                            self.info['goal_collisions'] += 1
                            self.y_speed = self.y_speed * -0.5
                            if(self.y_speed >= 2):
                                createSFXEvent('ball_metal_bounce', volume_modifier = math.sqrt(abs(self.y_speed/self.y_speed_max)))
                            if(self.status_effects['zapped']):
                                self.y_speed = self.y_speed * 0.3
                    else:
                        self.goal_grounded = False
                    if(goal_top < self.y_pos < goal_top + 1 and self.y_speed >= 0):
                        self.y_pos = goal_top - self.gravity
            else:
                self.goal_grounded = False

        #Interacting with the walls
        def interact_with_walls():
            if(self.x_pos < left_wall): #Hit side of the wall
                self.info['wall_collisions'] += 1
                self.x_pos = left_wall
                if(self.x_speed < 0):
                    self.x_speed = self.x_speed * -0.5
                createSFXEvent('ball_metal_bounce', volume_modifier=(math.sqrt(abs(self.x_speed/self.x_speed_max))))

            if(self.x_pos > right_wall):
                self.info['wall_collisions'] += 1
                self.x_pos = right_wall
                if(self.x_speed > 0):
                    self.x_speed = self.x_speed * -0.5
                createSFXEvent('ball_metal_bounce', volume_modifier=(math.sqrt(abs(self.x_speed/self.x_speed_max))))
        
        def apply_x_speed_limits():
            #Speed Limits (X)
            speed_limit = self.x_speed_max
            if(self.status_effects['glued']):
                speed_limit -= 10
            if(self.x_speed > speed_limit):
                self.x_speed = speed_limit
            elif(self.x_speed < -1 * speed_limit):
                self.x_speed = -1 * speed_limit
        self.x_pos += self.x_speed
        self.info['x_distance_moved'] += abs(self.x_speed)

        apply_traction_friction()
        interact_with_goal_posts()
        interact_with_walls()
        apply_x_speed_limits()

        #Interacting with the ground
        if(self.y_pos < ground):
            self.y_speed += self.gravity
        elif(self.y_pos >= ground): #Don't go under the floor!
            self.check_environmental_collisions(return_environmental_modifiers())
            if(2 >= self.y_speed >= 0 or self.species == "blocked_ball"):
                self.y_speed = 0
            elif(self.y_speed < 0 ):
                pass
            else:
                self.y_speed = -1 * math.floor(self.y_speed * 0.75)
                createSFXEvent('ball_grass_bounce', volume_modifier=(abs(self.y_speed/self.y_speed_max)))
                self.info['floor_collisions'] += 1
                if(self.status_effects['zapped']):
                            self.y_speed = self.y_speed * 0.3
                if(self.status_effects['glued']):
                    self.y_speed = self.y_speed * 0.75
                            

                
                 #Reduces bounciness over time
            self.y_pos = ground
        
        self.check_ceiling_collisions()

        def apply_y_speed_limits():
            if(self.y_speed > self.y_speed_max):
                self.y_speed = self.y_speed_max
            elif(self.y_speed < -1 * self.y_speed_max):
                self.y_speed = -1 * self.y_speed_max
        apply_y_speed_limits()
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
        if(self.blocked_timer > 0):
            self.blocked_timer -= 1
            if(self.blocked_timer == 0):
                self.bounciness = 1
        
        for effect in self.status_effects:
            if(self.status_effects[effect] > 0):
                self.status_effects[effect] -= 1
                if(self.status_effects["bubbled"] == 0):
                    self.bubble = None
        
    def update_bubble_status(self, bubble):
        current_bubble = self.bubble
        self.bubble = bubble
        if(current_bubble):
            current_bubble.lifetime = 0