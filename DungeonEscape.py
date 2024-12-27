
import random
class Player:
    
    #Player Constructor
    def __init__(self, name): 
        self.name = name
        self.health = 100
        self.stamina = 50
        self.damage = 20
        self.xpos = 0
        self.ypos = 0
        self.kill_count = 0

    #Player Stats
    def __repr__(self):
        return self.name
   
    def show_stats(self):
        return "Here are {name} stats: /n Attack: {damage} /n Health: {health} /n Stamina: {stamina}.".format(name = self.name, damage = self.damage,
        health = self.health, stamina = self.stamina) 

    #Basic and Heavy Attacks
    def basic_attack(self, enemy):
        if self.stamina > 10:
            self.stamina -= 10
            enemy.health -= 20
            print("20 Damage done!")
            print(enemy.__repr__())
            print("Player Stamina: {stamina}".format(stamina = self.stamina))
        else:
            return "Not enough stamina!"
    
    def heavy_attack(self, enemy):
        if self.stamina > 20:
            self.stamina -= 20
            enemy.health -= 30
            print("30 damage done!")
            print(enemy.__repr__())
            print("Player Stamina: {stamina}".format(stamina = self.stamina))
        else:
            return "Not enough stamina!"
    
    #Regains Stamina
    def rest_up(self):
        print("You took a rest! Gain 20 stamina.")
        self.stamina += 20
        print(self.stamina)
    
    #Resets the player if they die
    def respawn(self):
        self.health = 100
        self.stamina = 50
    
    def potential_actions(self):
       print("""
        Movement: Enter W,A,S,D to move 
        Stats Checker: Enter S to view stats
        Inventory: Enter I to view items
        """)
    def move(self, key):
        if key in ("W","w"):
            if self.xpos > 0:
                self.xpos -= 1
                print("Player Moved!")
                return 1
            else:
                print("Cannot move in this direction: Try again")
                return 0
        elif key in ("A","a"):
            if self.ypos > 0:
                self.ypos -= 1
                print("Player Moved!")
                return 1
            else:
                print("Cannot move in this direction: Try again")
                return 0
        elif key in ("S","s"):
            if self.xpos < 6:
               self.xpos += 1
               print("Player Moved!")
               return 1
            else:
                print("Cannot move in this direction: Try again")
                return 0
        elif key in ("D","d"):
            if self.ypos < 6:
                self.ypos += 1
                print("Player Moved!")
                return 1
            else:
                print("Cannot move in this direction: Try again")
                return 0
        
    def use_potion(self, bag):
        for item in bag.bagspace:
            if isinstance(item, Potion):
                bag.bagspace.pop(item)
                player.health += 50
                return "Potion used!"
        else:
            return "No potions in bag!"
                        
    
class Inventory:
    
    def __init__(self):
        self.bagspace = [Potion, Potion, Potion, Potion, Potion]
        self.stone_count = 0
        
    
    def __repr__(self):
        return self.bagspace
    
    def add_item(self, item):
        self.bagspace.append(item)
    
    def remove_item(self, item):
        self.bagspace.pop(item)
    
    def view(self):
        for i in self.bagspace:
            print(i)
    
class Potion:
    def __init__(self):
        pass

    def __repr__(self):
        description = "A Potion heals the player for 20 health!"
        return description
class Key:
    def __init__(self):
        pass
    def __repr__(self):
        description = "A golden key. Must unlock something..."
class Castle:

    #Creates a 2D game world
    def __init__(self, rows, cols, player):
        self.game_world = [["-" for i in range(rows)] for j in range(cols)]
        self.game_world[player.xpos][player.ypos] = player
        

    def display_world(self):
        for i in self.game_world:
            print(i)
    
    def update_position(self, player, key):
        curr_x, curr_y = player.xpos, player.ypos
        moving = player.move(key)
        
        self.game_world[player.xpos][player.ypos] = player
        
        if moving == 1:
            self.game_world[curr_x][curr_y] = "-"
    
    def items_in_castle(self, player, bag):
        if self.game_world[0][6] == player:
            print("You have stumbled upon a storage room: Inside you notice a trap door with a lock:")
            print("On the lock you can enter three numbers from 0 to 9.")
            code = input("What numbers would you like to try:")

            if code == "835":
                print("CLICK!")
                print("The door has opened! You discover a chest that is glowing yellow:")
                print("Upon getting closer to the chest you notice another lock")
                if Key in bag:
                    print("CLICK!")
                    print("The chest opened and you found a glowing yellow stone. You decide to put it in your bag")
                    bag.stone_count += 1
            else:
                print("This code did not work. Must be clues somewhere...")
                return
    
        elif self.game_world[3][1] == player:
            print("You have entered the library!")
            print("You notice a figure reading a book!")
            print("Librarian: Oh my! Well hello there! I am the librarian of this castle hehe")
            print("Librarian: I am trying to crack this cipher but I cannot figure it out!")
            print("Librarian: The ciphertext is: \"Qtyo esp dezyp lyo qppo te ez esp Hpww!\"")
            decoded = input("Do you know what the ciphertext says: ")

            if decoded == "Find the stone and feed it to the Well!":
                print("Librarian: You cracked it! Well done!")
                print("Hmmm interesting, I actually happen to have a stone on me! I guess you deserve it for breaking the code")
                print("You have acquired a stone!")
                bag.stone_count += 1
            else:
                print("That text does not seem to make sense!")
                return
        
        elif self.game_world[4][3] == player:
            print("You have entered the Castle Courtyard")
            print("You notice a Well in the center of the Courtyard")

            if bag.stone_count == 3:
                print("The stone in your bag begin to vibrate")
                print("Suddenly they levitate out and fly into the well")
                print()
                print("VRRRRRRRAAAAAAROOOOOM!!!!")
                print("A giant stone beast has emerged from the well! You notice that within the beast is the face of the King!")
                return 3
        elif self.game_world[6][6] == player:
            print("You have reach the Throne Room!")
            print()
            print("You noticed an Enormous Warrior sitting on the King's Throne")
            print("Warrior: Welcome to my domain! Only worthy hero's are able to challenge me!")
            
            if player.kill_count == 20:
                print("Warrior: I see that fervent bloodlust in your eyes!")
                print("A fight to the death we shall have!")
                print("PREPARE YOURSELF FOR THE AFTERLIFE!!!")
                return 2
            else:
                print("Warrior: Prove yourself first and then return!")
                return
        
        elif self.game_world[5][0] == player:
            print("You have entered the Dungeon Cellars!")
            print("You look around and notice green goop.")
            print("You notice a trail of this goop further down the dungeon")
            print("As you get closer and closer you come upon a glowing blue stone")
            print("You go to grab but the goop begins to form!")
            print("GRARARAHAHAAHRHARHAH")

            BattleSimulator.boss_sim(player, SlimeKing(), bag, 1)
            return 1
        else:
            return "You traverse the halls!"
                 
      
class Mob:

    def __init__(self):
        self.name = "Slime"
        self.health = 40
        self.stamina = 50
        self.damage = 10
    
    def __repr__(self):
        return "This enemy has {hp}!".format(hp = self.health)
    
    def attack(self, player):
        self.stamina -= 10
        player.health -= 10
        print("10 damage done by the enemy!")
        print(player.health)

class Warrior:
    def __init__(self):
        self.name = "Ragnar \"Deathbringer\" Thorson"
        self.health = 80
        self.stamina = 100
        self.damage = 30
    
    def bloodlust(self, player):
        self.health += 10
        player.health -= self.damage

    def warriors_stance(self, player):
        self.health -= 20
        self.damage += 10
    

class StoneBeast:
    def __init__(self):
        self.name = "Glowing Behemoth"
        self.health = 200
        self.stamina = 1000
        self.damage = 1
    
    def dazed(self, player):
       chance = random.randint() * 100

       if chance > 50:
        print("You have been dazed by the light")
        player.stamina -= 15
        player.damage -= 1
    
    def slam(self, player):
        player.health -= self.damage
    
    def fireup(self):
        self.damage += 5
    
    def collossal_slam(self, player):
        self.health -= 30
        player.health -= 50

class SlimeKing:
    def __init__(self):
        self.name = "Slime King"
        self.health = 60
        self.damage = 10
        self.stamina = 50

    def divide(self):
        mob = Mob()
        BattleSimulator.battle_sim(player, mob, bag)
    
    def goo_shot(self, player):
        player.health -= self.damage
        player.stamina -= 10

    def slime_battle(self, chance, player):
        chance = random.randint() * 100
        if chance <= 20:
            self.divide(player)
        else:
            self.goo_shot(player)


       

class BattleSimulator:
    def __init__(self, player):
        self.hero = player

    def encounter(self):
        encounter_chance = random.random() * 100

        if encounter_chance >= 50.0:
            print("An enemy is preventing you from moving!")
            return 1
        else:
            return 0
        
    #Simulates a battle between an enemy mob and player.
    def battle_sim(self, player, enemy, bag): 

        while enemy.health > 0:
            action = input("Choose an action: (Attack: A, Rest: R, Heal: H)")
            if action == "A":
                attack_action = input("Basic Attack (B) or Heavy Attack (H)")
                if attack_action == "B":
                    player.basic_attack(enemy)
                    enemy.attack(player)
                elif attack_action == "H":
                    player.heavy_attack(enemy)
                    enemy.attack(player)
                
            elif action == "R":
                player.rest_up()
                enemy.attack(player)
            
            elif action == "H":
                player.use_potion(bag)
                enemy.attack(player)
            
            if enemy.health < 0:
                print('Enemy Defeated!')
                break
            if player.health < 0:
                print("You have been defeated!")
                player.respawn()
                break
    
    def boss_sim(self, player, boss, bag, key):
            chance = random.randint() * 100
        
            while boss.health > 0:
                if boss.name == "Slime King":
                    action = input("Choose an action: (Attack: A, Rest: R, Heal: H)")
                    if action == "A":
                        attack_action = input("Basic Attack (B) or Heavy Attack (H)")
                    if attack_action == "B":
                        player.basic_attack(boss)
                        boss.slime_battle(player)
                    elif attack_action == "H":
                        player.heavy_attack(boss)
                        boss.slime_battle(player)
                elif action == "R":
                    player.rest_up()
                    boss.slime_battle(player)
            
                elif action == "H":
                    player.use_potion(bag)
                    boss.slime_battle(player)
                
                if boss.health <= 0:
                    if boss.name == "Slime King":
                        player.stone_count += 1
                        print("The green goop began to dissolve leaving only a glowing blue stone")
                        print("You place the stone in your bag!")
                    
            



                 
                
                

            
                    

#Start of Game

print("Welcome Hero! Today is the day where we take back the Kings Castle from the evil Slimes!")
name = input("Firstly, What is your name: ")    #Prompts users player name
print("Welcome " + name + "!")
player = Player(name)          #Creates a Player object
bag = Inventory()              #Creates a Inventory object
castle = Castle(7,7, player)   #Creates a 7x7 2D game world with the player starting at the 0, 0 indexes
sim = BattleSimulator(player)  #Creates a battle between player and enemies  
print(castle.display_world())

print()
print("You are currently in the Entrance Hall of the Castle")
print()



#Main Game Loop
while True:

    next_move = input("Enter an action (Press H key to view potential actions):").strip().upper()
    
    if next_move == "H":
        print(player.potential_actions())

    elif next_move == "M":
        print(player.show_stats())

    elif next_move == "I":
        print(bag.view())

    elif next_move == "W" or next_move == "D" or next_move == "S" or next_move == "A":
        chance = sim.encounter()
        
        if chance == 1.0:
            mob = Mob()
            sim.battle_sim(player, mob, bag)

        castle.update_position(player, next_move)
        castle.items_in_castle(player, bag)
        castle.display_world()
    
    elif next_move == "P":
        print(castle.display_world())
    
    elif next_move == "Q":
        print("Thanks for playing!")
        break
        
    else:
        print("Invalid Command: Press H to view actions")

    print()
   
    





















