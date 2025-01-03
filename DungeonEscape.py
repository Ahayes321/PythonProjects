
import random
import sys

from Demos.mmapfile_demo import offset


class Player:
    
    #Player Constructor
    def __init__(self, name): 
        self.name = name
        self.health = 100
        self.stamina = 50
        self.damage = 20
        self.xpos = 0
        self.ypos = 0
        self.kill_count = 20



    #Shows the players name. Used for display.
    def __repr__(self):
        return self.name

   #Shows a list of stats that the player has.
    def show_stats(self):
        return "Here are {name} stats: /n Attack: {damage} /n Health: {health} /n Stamina: {stamina}.".format(name = self.name, damage = self.damage,
        health = self.health, stamina = self.stamina) 

    #Basic and Heavy Attacks
    def basic_attack(self, enemy):
        if self.stamina >= 10:
            self.stamina -= 10
            enemy.health -= 20
            print()
            print("20 Damage done!")
            print(enemy.__repr__())
            print("Player Stamina: {stamina}".format(stamina = self.stamina))
        else:
            return "Not enough stamina!"
    
    def heavy_attack(self, enemy):
        if self.stamina >= 20:
            self.stamina -= 20
            enemy.health -= 30
            print()
            print("30 damage done!")
            print(enemy.__repr__())
            print("Player Stamina: {stamina}".format(stamina = self.stamina))
        else:
            return "Not enough stamina!"
    
    #Regains Stamina
    def rest_up(self):
        print("You took a rest! Gain 20 stamina.")
        self.stamina += 20
        return "Player Stamina: {stamina}".format(stamina = self.stamina)
    
    #Resets the player if they die
    def game_over(self):
        if self.health <= 0:
            print("You have been slain!")
            print("Game Over!")
            exit("Returning to Main Menu")

    #Displays the actions that a player can take
    def potential_actions(self):
       print("""
        Movement: Enter W,A,S,D to move 
        Stats Checker: Enter S to view stats
        Inventory: Enter I to view items
        """)

    #This method allows the player to move up, down, left, or right. Uses WASD.
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

    #Allows the player to use a Potion and heal.
    def use_potion(self, bag):
        return bag.use_potion(self)
                        
#Keeps track of the number of Potions available to use.
class Inventory:

    #Constructor
    def __init__(self):
        self.bagspace = [Potion, Potion, Potion, Potion, Potion]
        self.stone_count = 3
        
    #Shows amount of potions
    def __repr__(self):
        for i in range(len(self.bagspace)):
            print(str(i + 1) + ". Potion")
        return ""

    #Adds an items to the bag
    def add_item(self, item):
        self.bagspace.append(item)


    #Heals the player and removes the potion from the bag.
    def use_potion(self, player):
        if self.bagspace:
            self.bagspace.pop(0)
            player.health += 50
            if player.health > 100:
                player.health = 100
            return "Potion Used!"
        return "No valid Potion!"

#Used to heal player
class Potion:
    def __init__(self):
        pass

    def __repr__(self):
        description = "Potion"
        return description

#Used to decode ciphertext.
class CipherDecoder:
    def __init__(self):
        self.name = "Decoder"
    def __repr__(self):
        description = "Decodes ciphertext!"
        return description

    #Takes in a message and an offset and decodes the given message.
    def caesar_decode(self,message, offset):
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
        new_message = []
        for symbol in message:
            if symbol in alphabet:
                new_message.append(alphabet[(alphabet.index(symbol) + offset) % 26]) #Uses mod 26 to stay within bounds of the alphabet list
            else:
                new_message.append(symbol)  # If string is not a letter then it does not offset.

        return "".join(new_message)
class Castle:

    #Creates a 2D game world
    def __init__(self, rows, cols, player):
        self.game_world = [["-" for i in range(rows)] for j in range(cols)]
        self.game_world[player.xpos][player.ypos] = player

        #Booleans that indicate whether an event in the castle has been completed or not.
        self.SK_complete = False
        self.WK_complete = False
        self.SB_complete = False

        #Potion events
        self.P5 = False
        self.P10 = False
        self.P15 = False
        self.P20 = False
        
    #Displays the game world as a 2D array
    def display_world(self):
        for i in self.game_world:
            print(i)
        return ""

    #Updates where the player is positioned in the game world
    def update_position(self, player, key):
        curr_x, curr_y = player.xpos, player.ypos
        moving = player.move(key)
        
        self.game_world[player.xpos][player.ypos] = player
        
        if moving == 1:
            self.game_world[curr_x][curr_y] = "-"

    #This method triggers events within the castle.
    def items_in_castle(self, player, bag):
        boss_arena = BattleSimulator(player)
        SK_complete = False

        self.numbers_in_castle(player, bag)

        #Triggers a lock puzzle
        if self.game_world[0][6] == player:
            print("You have stumbled upon a storage room: Inside you notice a trap door with a lock:")
            print("On the lock you can enter three numbers from 0 to 9.")
            code = input("What numbers would you like to try:")

            if code == "835":   #If correct lock code is determined. You get a stone
                print("CLICK!")
                print("The door has opened! You discover a chest that is glowing yellow:")
                print("You open the chest a find a bright yellow stone.")
                print()
                print("You take the stone!")
                bag.stone_count += 1
            else:
                print("This code did not work. Must be clues somewhere...")
                return

        #Triggers an event with a caesar cipher. Must provide an offset and determine the code.
        elif self.game_world[3][1] == player:
            print("You have entered the library!")
            print("You notice a figure reading a book!")
            print("Librarian: Oh my! Well hello there! I am the librarian of this castle hehe")
            print("Librarian: I am trying to crack this cipher but I cannot figure it out!")
            print("Librarian: The ciphertext is: \"qtyo esp dezypd lyo qppo te ez esp hpww!\"")


            if self.WK_complete:    #If the Warrior has been defeated
                print()
                print("Librarian: Is that a cipher device!")
                print("If only we knew what the offset was")

                offset = input("What offset would you like to use?") #The offset of the cipher

                if offset == "15":
                    decoder = CipherDecoder()
                    print(decoder.caesar_decode("qtyo esp dezyp lyo qppo te ez esp hpww!", 15)) #Decodes the encrypted message with the correct offset.
                else:
                    print("This offset did nothing!")

            decoded = input("Do you know what the ciphertext says: ")


            if decoded == "find the stones and feed it to the well!": #Gain a stone if correct message is found
                print("Librarian: You cracked it! Well done!")
                print("Hmmm interesting, I actually happen to have a stone on me! I guess you deserve it for breaking the code")
                print("You have acquired a stone!")
                bag.stone_count += 1
            else:
                print("That text does not seem to make sense!")
                return

        #Triggers ending fight if all three stones have been collected in the castle
        elif self.game_world[4][3] == player:
            print("You have entered the Castle Courtyard")
            print("You notice a Well in the center of the Courtyard")
            print(bag.stone_count)

            if bag.stone_count == 3:
                print("The stones in your bag begin to vibrate")
                print("Suddenly they levitate out and fly into the well")
                print()
                print("VRRRRRRRAAAAAAROOOOOM!!!!")
                print("A giant stone beast has emerged from the well! You notice that within the beast is the face of the King!")
                print()
                boss_arena.stonebeast_sim(player, StoneBeast(), bag) #Triggers StoneBeast boss fight
                return 3

        #Triggers event with the Warrior King. Must have defeated 15 enemies before you are able to trigger the event fully.
        elif self.game_world[6][6] == player and self.WK_complete == False:
            print("You have reach the Throne Room!")
            print()
            print("You noticed an Enormous Warrior sitting on the King's Throne")
            print("Warrior: Welcome to my domain! Only worthy hero's are able to challenge me!")
            
            if player.kill_count == 20:
                print("Warrior: I see that fervent bloodlust in your eyes!")
                print("A fight to the death we shall have!")
                print("PREPARE YOURSELF FOR THE AFTERLIFE!!!")

                boss_arena.warriorking_sim(player, Warrior(), bag)
                self.WK_complete = True
                return 2
            else:
                print("Warrior: Prove yourself first and then return!")
                return
        
        elif self.game_world[5][0] == player and self.SK_complete == False:
            print("You have entered the Dungeon Cellars!")
            print("You look around and notice green goop.")
            print("You notice a trail of this goop further down the dungeon")
            print("As you get closer and closer you come upon a glowing blue stone")
            print("You go to grab but the goop begins to form!")
            print("GRARARAHAHAAHRHARHAH")

            boss_arena.slimeking_sim(player, SlimeKing(), bag)
            self.SK_complete = True
            return 1

        elif self.game_world[4][4] == player:
            print("As you are walking through the halls you notice a sign")
            print("The Alchemist Lab")
            print("You decide to enter the lab")
            print()
            print("Alchemist: Oooooo a newcomer I see!")
            print("Alchemist: You look very beat up oh no oh no!")
            print("I can offer you some potions for slime residue")

            if player.kill_count >= 5 and self.P5 == False:
                print("Oh yes! Thank you!")
                print("Potion for you!")
                five_kill_potion = Potion()
                bag.add_item(five_kill_potion)
                self.P5 = True

            if player.kill_count >= 10 and self.P10 == False:
                print("Oh yes! Thank you!")
                print("Potion for you!")
                print()
                ten_kill_potion = Potion()
                bag.add_item(ten_kill_potion)
                self.P10 = True

            if player.kill_count >= 15 and self.P15 == False:
                print("Oh yes! Thank you!")
                print("Potion for you!")
                print()
                fifteen_kill_potion = Potion()
                bag.add_item(fifteen_kill_potion)
                self.P15 = True

            if player.kill_count >= 20 and self.P20 == False:
                print("Oh yes! Thank you!")
                print("Potion for you!")
                print()
                twenty_kill_potion = Potion()
                bag.add_item(twenty_kill_potion)
                self.P20 = True

            if self.WK_complete:
                print("Oh I see you defeated that brute in the Kings halls!")
                print("You deserve a Potion for that too!")
                print()
                warrior_potion = Potion()
                bag.add_item(warrior_potion)

            if self.SK_complete:
                print("Oh!! This is a rare slime residue!")
                print("Two Potions for you!")
                print()
                slimeking1_potion = Potion()
                slimeking2_potion = Potion()

                bag.add_item(slimeking1_potion)
                bag.add_item(slimeking2_potion)


        else:
            return "You traverse the halls!"

    def numbers_in_castle(self, player, bag):
        if self.game_world[0][2] == player:
            print("You arrive at the garrison offices. You notice a desk full of papers.")
            print("On the paper you notice a bright number in red")
            print()
            print("8")
            print()

        elif self.game_world[6][2] == player:
            print("You arrive to a bedroom chambers.")
            print("You notice a small note on a side table")
            print("On the note you notice a bright number in red")
            print()
            print("3")
            print()

        elif self.game_world[2][5] == player:
            print("You arrive to the kitchen.")
            print("In the kitchen you notice a bright number in red posted on door.")
            print()
            print("5")
            print()

        elif self.game_world[4][4] == player and self.SK_complete and self.WK_complete:
            print("Alchemist: Oh what device do you have there!")
            print("Alchemist: Well if it isn't my old cipher device!")
            print("Alchemist: The cipher device allows you to decode hidden messages.")
            print("Alchemist: However you need to know the offset of the numbers")
            print()
            print("Alchemist: I'm not sure who used it last but the King always would use set the device to 15")
            print("Alchemist: His security measures were not the best...")



      
class Mob:

    def __init__(self):
        self.name = "Slime"
        self.health = 40
        self.stamina = 50
        self.damage = 10
    
    def __repr__(self):
        return "This enemy has {hp} HP!".format(hp = self.health)
    
    def attack(self, player):
        self.stamina -= 10
        player.health -= 10
        print()
        print("10 damage done by the {name}!".format(name = self.name))
        print("{name} HP: {health}".format(name= player.name, health= player.health))

class Warrior:
    def __init__(self):
        self.name = "Ragnar \"Deathbringer\" Thorson"
        self.health = 40
        self.stamina = 100
        self.damage = 30

    def __repr__(self):
        return "Warrior HP: {health}".format(health = self.health)
    
    def bloodlust(self, player):
        print("The Warror unleashed a mountain of rage!")

        self.health += 10
        player.health -= self.damage
        print(self)
        print()
        print("Player damaged! {health} HP!".format(health=player.health))

    def warriors_stance(self, player):
        print("The warrior took a more aggressive posture!")

        self.health -= 20
        self.damage += 10

        print(self)
        print("Player Health: {health} HP!".format(health=player.health))
    
    def warrior_battle(self, chance, player):
        chance = random.randint(0, 101)
        if chance <= 30 and self.health > 30:
            self.warriors_stance(player)
        else:
            self.bloodlust(player)

class StoneBeast:
    def __init__(self):
        self.name = "Glowing Behemoth"
        self.health = 60
        self.stamina = 1000
        self.damage = 1
    
    def dazed(self, player):
       chance = random.randint(0, 101)

       if chance > 50:
        print("You have been dazed by the light")
        print("Player damaged! {health} HP!".format(health=player.health))
        print("You seem more tired: Stamina: {stam}").format(stam=player.stamina)
        player.stamina -= 15
        player.damage -= 10
    
    def slam(self, player):
        print("The beast slams its arms down!")
        print("Player damaged! {health} HP!".format(health=player.health))
        player.health -= self.damage
    
    def fireup(self):
        print("The fire burns within the beast")
        self.damage += 5
    
    def collossal_slam(self, player):
        print("The beast slams its whole body down!")
        print()
        print("Player damaged! {health} HP!".format(health=player.health))
        self.health -= 30
        player.health -= 50

    def stone_battle(self, chance, player):
        chance = random.randint(0, 101)
        if chance <= 25:

            self.dazed(player)
        elif chance > 25 and chance <= 50:
            self.collossal_slam(player)
        elif chance > 50 and chance <= 75:
            self.slam(player)
        else:
            self.fireup()

class SlimeKing:
    def __init__(self):
        self.name = "Slime King"
        self.health = 60
        self.damage = 10
        self.stamina = 50

    def __repr__(self):
        return "{name} HP: {health}".format(name = self.name, health = self.health)

    def divide(self):
        mob = Mob()
        battle_arena = BattleSimulator(player)
        print("The Slime King divided spawning a slime minion!")
        battle_arena.battle_sim(player, mob, bag)
        print("Minion Defeated!")

    def goo_shot(self, player):
        player.health -= self.damage
        player.stamina -= 10
        print()
        print("Slime King spits goo at you!")
        print("Player damaged! {health} HP!".format(health = player.health))

    def slime_battle(self, chance, player):
        chance = random.randint(0, 101)
        if chance <= 20:
            self.divide()
        else:
            self.goo_shot(player)


class BattleSimulator:
    def __init__(self, player):
        self.hero = player

    def encounter(self):
        encounter_chance = random.random() * 100

        if encounter_chance >= 100: #SWITCH AFTER
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

                elif attack_action == "H":
                    player.heavy_attack(enemy)

                
            elif action == "R":
                player.rest_up()
                enemy.attack(player)
            
            elif action == "K":
                player.use_potion(bag)
                enemy.attack(player)
            
            if enemy.health < 0:
                print()
                break

            enemy.attack(player)
            if player.health <= 0:
                player.game_over()

    #Simulates a battle between the Slime King boss and player
    def slimeking_sim(self, player, boss, bag):
        
            while boss.health > 0:

                action = input("Choose an action: (Attack: A, Rest: R, Heal: K)")

                if action == "A":
                    attack_action = input("Basic Attack (B) or Heavy Attack (H): ").strip().upper()
                    if attack_action == "B":
                        result = player.basic_attack(boss)
                        if result:  # If insufficient stamina
                            print(result)
                    elif attack_action == "H":
                        result = player.heavy_attack(boss)
                        if result:  # If insufficient stamina
                            print(result)

                elif action == "R":
                    player.rest_up()

            
                elif action == "K":
                    player.use_potion(bag)

                if boss.health <= 0:
                    bag.stone_count += 1
                    print("The green goop began to dissolve leaving only a glowing blue stone")
                    print("You place the stone in your bag!")
                    return ""

                boss.slime_battle(0, player)

                if player.health <= 0:
                    player.game_over()
                    return ""

    #Simulates a battle between the Warrior King and the player
    def warriorking_sim(self, player, boss, bag):
        chance = random.randint(0, 101)

        while boss.health > 0:

            action = input("Choose an action: (Attack: A, Rest: R, Heal: K)")

            if action == "A":
                attack_action = input("Basic Attack (B) or Heavy Attack (H)")
                if attack_action == "B":
                    player.basic_attack(boss)
                elif attack_action == "H":
                    player.heavy_attack(boss)

            elif action == "R":
                player.rest_up()


            elif action == "K":
                player.use_potion(bag)

            if boss.health <= 0:
                print("The warrior fell to one knee.")
                print()
                print("Warrior: You are strong! I did not expect this to be the day I was slain!")
                print("Warrior: As a token for beating me take this! I looted it from the library, it could be useful.")
                print("You placed the device in your bag!")
                decoder = CipherDecoder()
                bag.add_item(decoder)

                return ""

            boss.warrior_battle(0, player)
            if player.health <= 0:
                player.game_over()
                print("You have been defeated!")

    #Simulates a battle between the StoneBeast and the player
    def stonebeast_sim(self, player, boss, bag):
        while boss.health > 0:

            action = input("Choose an action: (Attack: A, Rest: R, Heal: K)")

            if action == "A":
                attack_action = input("Basic Attack (B) or Heavy Attack (H)")
                if attack_action == "B":
                    player.basic_attack(boss)
                elif attack_action == "H":
                    player.heavy_attack(boss)

            elif action == "R":
                player.rest_up()


            elif action == "K":
                player.use_potion(bag)

            if boss.health <= 0: #If you beat the boss
                print("The beasts begins to crumble!")
                print("All that remains is the King. You approach him.")
                print("King: Thank you! You saved this kingdom!")
                print()
                exit("Congrats! You have completed the game!")

            boss.stone_battle(0, player)

            if player.health <= 0:
                player.game_over()
                print("You have been defeated!")


#Start of Game

print("Welcome Hero! Today is the day where we take back the Kings Castle from the evil Slimes!")
name = input("Firstly, What is your name: ")  #Prompts users player name
print()
print("Welcome " + name + "!")
player = Player(name)          #Creates a Player object
bag = Inventory()              #Creates a Inventory object
castle = Castle(7,7, player)   #Creates a 7x7 2D game world with the player starting at the 0, 0 indexes
sim = BattleSimulator(player) #Creates a battle between player and enemies
print()
print("Here is a map of the Castle:")
print()
print(castle.display_world())

print()
print("You are currently in the Entrance Hall of the Castle")
print()



#Main Game Loop
while True:

    next_move = input("Enter an action (Press Z key to view potential actions):").strip().upper()
    
    if next_move == "Z":
        print(player.potential_actions())

    elif next_move == "M":
        print(player.show_stats())

    elif next_move == "I":
        print(bag.__repr__())

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
   
    





















