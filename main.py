from os import kill
import pygame
import sys 
import random


#game variables
WIDTH = 800
HEIGHT = 400
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        ###animation status
        self.idle_animation = False
        self.light_attack_animation = False 
        self.heavy_attack_animation = False
        self.jump_animation = False
        self.gravity = 0
        
        ###frames for each separate chain of actions
        super().__init__()
        self.sprites_run = []     #run
        self.sprites_run.append(pygame.image.load("data/player_run_1.png").convert_alpha())
        self.sprites_run.append(pygame.image.load("data/player_run_2.png").convert_alpha())

        
        self.sprites_light_attack = []  #light attack
        self.sprites_light_attack.append(pygame.image.load("data/player_attack_1.png").convert_alpha())
        self.sprites_light_attack.append(pygame.image.load("data/player_attack_2.png").convert_alpha())
        
        
        self.sprites_heavy_attack = []  #heavy attack
        self.sprites_heavy_attack.append(pygame.image.load("data/player_attack_5.png").convert_alpha())
        self.sprites_heavy_attack.append(pygame.image.load("data/player_attack_6.png").convert_alpha())
        
        
        self.current_sprite = 0 
        
        self.image = self.sprites_run[int(self.current_sprite)]
        self.image = self.sprites_light_attack[int(self.current_sprite)]
        self.image = self.sprites_heavy_attack[int(self.current_sprite)]
        self.rect = self.image.get_rect(midbottom = (pos_x,pos_y))
    
    def run(self):
        self.idle_animation = True
        #self.attack_status = False
        
    def light_attack(self):
        self.light_attack_animation = True
        #self.attack_status = True
    
    def heavy_attack(self):
        self.heavy_attack_animation = True
        #self.attack_status = True
        
    def jump(self):
        self.jump_animation = True
        #self.attack_status = False
        
    def fall_gravity(self):    #create an earth gravity when the player jumps
        self.gravity = self.gravity + 1
        self.rect.y = self.rect.y + self.gravity
        if self.rect.bottom >= 340:
            self.rect.bottom = 340
        
    def update(self,speed):     #update the animations for the player
        self.fall_gravity()
        if self.jump_animation == True:
            self.gravity = -15           #only apply gravity when player jumps
            self.jump_animation = False
        elif self.light_attack_animation == True:
            self.current_sprite = self.current_sprite + speed
            if int(self.current_sprite) >= len(self.sprites_light_attack):
                self.current_sprite = 0
                self.light_attack_animation = False
            self.image = self.sprites_light_attack[int(self.current_sprite)] 
        elif self.heavy_attack_animation == True:
            self.current_sprite = self.current_sprite + speed
            if int(self.current_sprite) >= len(self.sprites_heavy_attack):
                self.current_sprite = 0
                self.heavy_attack_animation = False
            self.image = self.sprites_heavy_attack[int(self.current_sprite)] 
        elif self.idle_animation == True:
            self.current_sprite = self.current_sprite + speed
            if int(self.current_sprite) >= len(self.sprites_run):
                self.current_sprite = 0
                self.idle_animation = False
            self.image = self.sprites_run[int(self.current_sprite)] 
    
class Monster(pygame.sprite.Sprite):
    def __init__(self,type):   #set up different types of monsters and their positions
        super().__init__()
        if type == 1:
            wing_1 = pygame.image.load("data/wing_1.png").convert_alpha()
            wing_2 = pygame.image.load("data/wing_2.png").convert_alpha()
            self.frames = [wing_1,wing_2]
            y_pos = 220
        elif type == 2:
            snail_1 = pygame.image.load("data/snail_1.png").convert_alpha()
            snail_2 = pygame.image.load("data/snail_2.png").convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 340
        elif type == 3:
            golem_1 = pygame.image.load("data/golem_1.png").convert_alpha()
            golem_2 = pygame.image.load("data/golem_2.png").convert_alpha()
            self.frames = [golem_1,golem_2]
            y_pos = 220
        elif type == 4:
            slime_1 = pygame.image.load("data/slime_1.png").convert_alpha()
            slime_2 = pygame.image.load("data/slime_2.png").convert_alpha()
            self.frames = [slime_1,slime_2]
            y_pos = 340 
        else:
            castle_1 = pygame.image.load("data/castle.png").convert_alpha()
            castle_2 = pygame.image.load("data/castle.png").convert_alpha()
            self.frames = [castle_1,castle_2]
            y_pos = 340
        self.animate_index = 0
        self.image = self.frames[self.animate_index]
        self.rect = self.image.get_rect(midbottom = (850,y_pos))
    
    def animate_state(self):      #check the index of the animations to make sure it's within available frames
        self.animate_index = self.animate_index + 0.1
        if self.animate_index >= len(self.frames):
            self.animate_index = 0
        self.image = self.frames[int(self.animate_index)]
    
    def update(self,level):               #update the actions/statuses (frames) of monsters
        self.animate_state()
        self.rect.x = self.rect.x - level
        self.check_out_frame() 
        
    def check_out_frame(self):      #when the monsters are out of frames, they despawn
        if self.rect.x <= -50:
            self.kill()

    
            
######################################### game operations #############################################
pygame.init()
pygame.display.set_caption('Rescue My Baby')  #set the title for the game
screen = pygame.display.set_mode((WIDTH,HEIGHT)) #create the game screen
score = 0
target_score = 0 

###sound effects
jump_sound = pygame.mixer.Sound("data/jump.mp3")
jump_sound.set_volume(0.1)    
hit_sound = pygame.mixer.Sound("data/swing_hit.mp3")
hit_sound.set_volume(0.1)

#all songs
intro_song = pygame.mixer.Sound("data/intro_song.mp3")
intro_song.set_volume(0.1)
game_song = pygame.mixer.Sound("data/game_song.mp3")
game_song.set_volume(0.04)
end_song = pygame.mixer.Sound("data/end_song.mp3")
end_song.set_volume(0.1)

###main game setup
monster_interval = pygame.USEREVENT + 1
pygame.time.set_timer(monster_interval,3500)  #spawn enemies every 3500 miliseconds
text_font = pygame.font.Font("data/letter_font.TTF",25)

def redrawScreen(time_type):
    if time_type == 1:
        screen.blit(background,(bgX,0))   #draw first background image
        screen.blit(background,(bgX_2,0))
    if time_type == 2:
        screen.blit(background_2,(bgX,0))   #draw first background image
        screen.blit(background_2,(bgX_2,0))
    if time_type == 3:
        screen.blit(background_3,(bgX,0))   #draw first background image
        screen.blit(background_3,(bgX_2,0))
    pygame.display.update()
        
background = pygame.image.load('data/desert.png').convert_alpha()
background_2 = pygame.image.load('data/desert_2.png').convert_alpha()
background_3 = pygame.image.load('data/desert_3.png').convert_alpha()
bgX = 0
bgX_2 = background.get_width()

castle = pygame.image.load("data/castle.png").convert_alpha()

game_speed = pygame.time.Clock()
player_moving_group = pygame.sprite.Group()
player = Player(120,340)
player_moving_group.add(player)  
monster_group = pygame.sprite.Group()

###home screen setup
intro_active = True
text_font_menu = pygame.font.Font("data/letter_font_2.ttf",15)
menu = pygame.image.load("data/grass.JPG").convert_alpha()
couple = pygame.image.load("data/couple.png").convert_alpha()
text_1 = text_font.render("Press Q to view instructions",False,"Orange")
text_2 = text_font.render("Press W to start game",False,"Orange")
text_3 = text_font_menu.render("Princess Mia",False,"Magenta")
text_4 = text_font_menu.render("Patrick",False,"Magenta")

###instruction screen setup
text_font_title_ins = pygame.font.Font("data/letter_font.TTF",40)
text_font_ins = pygame.font.Font("data/letter_font_2.ttf",30)
text_font_ins_2 = pygame.font.Font("data/letter_font.TTF",15)
text_title = text_font_title_ins.render("INSTRUCTIONS",False,"Orange")
text_ins_1 = text_font_ins.render("Press S for heavy attack",False,"Yellow")
text_ins_2 = text_font_ins.render("Press D for light attack",False,"Yellow")
text_ins_3 = text_font_ins.render("Press Space for jump",False,"Yellow")
text_ins_4 = text_font_ins_2.render("Press E to go back to Menu",False,"Red")
action_1 = pygame.image.load("data/player_attack_1.png").convert_alpha()
action_2 = pygame.image.load("data/player_attack_5.png").convert_alpha()
action_3 = pygame.image.load("data/player_jump_1.png").convert_alpha()

###end screen setup
text_font_title_end = pygame.font.Font("data/letter_font.TTF",50)
text_font_end_message = pygame.font.Font("data/letter_font_2.ttf",30)
go_back_font = pygame.font.Font("data/letter_font.TTF",15)
text_title_end_message = text_font_title_end.render("HAPPY ENDING!",False,"Yellow")
text_title_end_message_2 = text_font_end_message.render("You rescued the princess",False,"Blue")
action_end = pygame.image.load("data/hug.png").convert_alpha()
background_end = pygame.image.load("data/mountain.jpg").convert_alpha() 
go_back = go_back_font.render("Press A to go back to Menu",False,"Pink")
end_screen = False

##run the game
game_active = False
run = True
num_initial_hit = 0
num_after_hit = 0
tracker_text = text_font.render("",False,"Yellow")

monster_level = 4    #default monster speed
player_speed = 0.05 #default player speed
    
while run: #to keep the game going, we have to put all functions inside the while loop (game loop)
    while intro_active:
        target_score = random.randint(55,70) #random target score between 55 and 70 to find the princess
        intro_song.play(-1,fade_ms=3000)
        
        instruct_active = True
        screen.blit(menu,(0,0))
        screen.blit(text_1,(120,30))
        screen.blit(text_2,(180,80))
        screen.blit(text_3,(230,190))
        screen.blit(text_4,(480,190))
        screen.blit(couple,(300,150))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro_active = False
                pygame.quit()    #quit game
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  #open instruction page
                    while instruct_active:
                        screen.fill("Pink")
                        screen.blit(text_title,(195,15))
                        screen.blit(text_ins_1,(150,105))
                        screen.blit(text_ins_2,(150,205))
                        screen.blit(text_ins_3,(150,305))
                        screen.blit(action_1,(530,65))
                        screen.blit(action_2,(530,185))
                        screen.blit(action_3,(530,270))
                        screen.blit(text_ins_4,(10,380))
                        pygame.display.flip()
                        
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                instruct_active = False
                                pygame.quit()    #quit game
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_e:
                                    instruct_active = False #go back to main menu
                elif event.key == pygame.K_w: #start the game
                    intro_song.stop()
                    intro_active = False
                   
    game_song.play(-1)
    text = text_font.render(f"Score: {score}",False,"Red")
    if score == 10:
        tracker_text = text_font.render("WOW!",False,"Blue")
        monster_level = 5
    elif score == 20:
        tracker_text = text_font.render("GOOD!",False,"Green")
        monster_level = 6
    elif score == 30:
        tracker_text = text_font.render("GREAT!",False,"Yellow")
        monster_level = 7
    elif score == 40:
        tracker_text = text_font.render("AWESOME!",False,"Magenta")
        monster_level = 8
    elif score == 50:
        tracker_text = text_font.render("EXCELLENT!",False,"Orange")
        monster_level = 9   
    elif score == target_score:
        tracker_text = text_font.render("PRINCESSSS!",False,"Red")
        monster_level = 3
        game_song.fadeout(6000)     
        
    
    attack_status = False
    for event in pygame.event.get():   #detect the user input
        if event.type == monster_interval: 
            if score < target_score:
                monster_group.add(Monster(random.choice([1,2,3,4])))
            else:
                monster_group.add(Monster(5))

        if event.type == pygame.QUIT:  #if the user decides to quit the game (X)
            run = False
            pygame.quit()    #quit game
            sys.exit()           #truly terminate python process
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player.light_attack()
                attack_status = True
            elif event.key == pygame.K_d:
                player.heavy_attack()
                attack_status = True
            elif event.key == pygame.K_SPACE:
                pygame.mixer.Channel(0).play(jump_sound)
                player.jump()
                attack_status = False
                
    hit = pygame.sprite.spritecollide(player,monster_group,attack_status) #check if the monsters are killed or not. If yes, they vanish
    for x in hit:
        num_after_hit = num_initial_hit + 1
        
    if num_after_hit > num_initial_hit and attack_status == True and score < target_score:      #if player swings and hits monsters
        pygame.mixer.Channel(1).play(hit_sound)
        score = score + 1
    elif num_after_hit > num_initial_hit and attack_status == True and score == target_score:   #if player and caster collide and player swings
        end_screen = True
    elif num_after_hit > num_initial_hit and attack_status == False and score == target_score:  #if player and castle collide and player doesn't swing
        end_screen = True
    num_initial_hit = num_after_hit
    
    
    #update the display of the game
    player.run()
    player_moving_group.update(player_speed)
    
    #dynamic environment lightings
    if score < 20:
        redrawScreen(1)
    elif score < 40 and score >= 20:
        redrawScreen(2)
    elif score >= 40:
        redrawScreen(3)
        
    bgX = bgX - monster_level
    bgX_2 = bgX_2 - monster_level
    
    screen.blit(text,(10,0))
    screen.blit(tracker_text,(550,0))
    
    player_moving_group.draw(screen)

    monster_group.draw(screen)
    monster_group.update(monster_level)
    pygame.display.flip()
    
        
    if bgX < background.get_width() * -1:
        bgX = background.get_width()
    if bgX_2 < background.get_width() * -1:
        bgX_2 = background.get_width()
    
    while end_screen:
        #clear out all previous game sessions
        game_song.stop()
        monster_level = 4
        monster_group.empty()
        tracker_text = text_font.render("",False,"Blue")
        
        #end screen initiate
        end_score = go_back_font.render(f"Total Score: {score}",False,"Pink")
        end_song.play(-1,fade_ms=3000)
        screen.blit(background_end,(0,0))
        screen.blit(text_title_end_message,(130,10))
        screen.blit(text_title_end_message_2,(220,75))
        screen.blit(go_back,(10,380))
        screen.blit(action_end,(260,120))
        screen.blit(end_score,(600,380))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_screen = False
                pygame.quit()    #quit game
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    score = 0
                    end_song.stop()
                    end_screen = False
                    intro_active = True
                
    game_speed.tick(FPS)   #set game frame rate at 60fps
