# Fire Emblem Heroes Summon Count Simulator
# Given an input of the focus character colors, the type of banner, and the number of orbs
# This project aims to visualize the expected number of copies of a target character.


# V 0.1
# We want to let this program generate a circle.
# We're going to have to add the data for the content/characters.

# Here we add the data for which characters are available in which pools.
# We have those in the 5-star pool, the 4-star special pool, and finally the 3-4 star regular pool.
# We'll have one type of banner, which is a usual 3%/3%/3%/55%/36% for the 5* Focus/5*/4* Special/4*/3*


# V 0.2
# We want to let the program ask what color you want to target, by asking it an order of priority.
# After which, it will want to check whether or not the order is valid (no repeating, only 0 to 3)
# Then, given something like 300 orbs, we try to do a summoning session until orbs are gone.
# We then report the number of targets that we have.

# V 0.3
# We now have the following things to do:
# 1) Change the number of focus units. We must have one.
# 2) We can ask the kind of banner it is. There are a couple of types to consider:
#   a) Legendary Banner [8/0/0/3/55/34]
#   b) Revival Banner [4/2/0/3/52/36]
#   c) Regular Banner [3/3/0/3/55/36]
#   d) 4-star Focus Banner [3/3/3/3/52/36]
#   e) Double Special Heroes [6/0/3/3/54/34]
#   f) Legendary Hero Remix Banner [6/0/0/3/55/36] ?? we will want to double-check.
# In hindsight I think starting with this would've been better.
# For now, we ignore the requirements except for the existence of a 4-color focus.
# We just have found a problem:
#   The game is not able to determine or differentiate which ones are the real target in the case of color-sharing.
#   The solution may be that we just roll the dice when it gets the corret color, to figure out if the person got what they're looking for.

# V 0.4 - Coming soon
# The idea here is to add pity rates, and either calculate the sums and the variances, or we add a graph. This might be harder, unfortunately, but we can learn it.
# To calculate pity rates, we want to count the number of non-focus or non 5-star units that we have.
# We then need to alter the pull rates, so we want to make a function for this.

import random
import math

# We will have the following dictionaries. Not sure how much it's needed, but we might as well.

# We define a summoning circle class.
class SummoningCircle:
    def __init__(self, color, rarity):
        self.color = color
        self.rarity = rarity

rarity_dict = {
    0: "5-star Focus",
    1: "5-star Non-Focus",
    2: "4-star Focus",
    3: "4-star Special",
    4: "4-star Non-Focus",
    5: "3-star Non-Focus",
}

color_dict = {
    0: "Red",
    1: "Blue",
    2: "Green",
    3: "Colorless",
}

# We then have a set of lists for the numbers above:

char_pool = [
    [1, 1, 1, 1],
    [33, 31, 25, 19],
    [0, 0, 0, 0],
    [38, 25, 20, 16],
    [36, 38, 29, 40],
    [36, 38, 29, 40]
]

pull_rate = [3, 3, 0, 3, 55, 36] #This is a basic/generic one. We are making a dictionary for a better one:

pullrate_dict = {
    0: [8, 0, 0, 3, 55, 34],
    1: [4, 2, 0, 3, 52, 36],
    2: [3, 3, 0, 3, 55, 36],
    3: [3, 3, 3, 3, 52, 36],
    4: [6, 0, 0, 3, 54, 34],
    5: [6, 0, 0, 3, 55, 36] 
}

bannertype_dict = {
    0: "Legendary",
    1: "Revival",
    2: "Regular",
    3: "4-Star Focus",
    4: "Double Special",
    5: "Legendary Remix"  
}

def newPullRate(count, bannertype):
    #Given a pity count, and the base list (which might be an actual list or just the original value where we extract pullrate from)
    #We spit out a new list for the correct values.
    #First, we do the simplest one:
    start = [0, 0, 0, 0, 0, 0]
    finish = [0, 0, 0, 0, 0, 0]
    total_5star_increase = 0
    if count >= 120:
        finish[0] = 100 * pullrate_dict[bannertype][0] / partialSum(pullrate_dict[bannertype], 1)
        finish[1] = 100 * pullrate_dict[bannertype][1] / partialSum(pullrate_dict[bannertype], 1)
        finish[2] = 0
        finish[3] = 0
        finish[4] = 0
        finish[5] = 0
    else:
        total_5star_increase = math.floor(count/5.0) * 0.5
        finish[0] = (partialSum(pullrate_dict[bannertype], 1) + total_5star_increase) * pullrate_dict[bannertype][0] / partialSum(pullrate_dict[bannertype], 1)
        finish[1] = (partialSum(pullrate_dict[bannertype], 1) + total_5star_increase) * pullrate_dict[bannertype][1] / partialSum(pullrate_dict[bannertype], 1)
        finish[2] = (100 - partialSum(pullrate_dict[bannertype], 1) - total_5star_increase) * pullrate_dict[bannertype][2] / (100 - partialSum(pullrate_dict[bannertype], 1))
        finish[3] = (100 - partialSum(pullrate_dict[bannertype], 1) - total_5star_increase) * pullrate_dict[bannertype][3] / (100 - partialSum(pullrate_dict[bannertype], 1))
        finish[4] = (100 - partialSum(pullrate_dict[bannertype], 1) - total_5star_increase) * pullrate_dict[bannertype][4] / (100 - partialSum(pullrate_dict[bannertype], 1))
        finish[5] = (100 - partialSum(pullrate_dict[bannertype], 1) - total_5star_increase) * pullrate_dict[bannertype][5] / (100 - partialSum(pullrate_dict[bannertype], 1))
        print("Final Rates:" + str(finish))
        print("Pullrate_dict: " + str(pullrate_dict[bannertype]))
    return finish
        


def orbCost(summon):
    val = 0
    if summon == 0:
        val = 5
    elif summon == 4:
        val = 3
    else:
        val = 4
    return val

def partialSum(array, endvalue):
    sum = 0
    i = 0
    # We count from array's value 0 to endvalue.
    for value in array:
        if i <= endvalue:
            sum += value
        i = i + 1
    return sum

def SummonResult():
    rarityluck = random.uniform(0, 100)
    rarity = 0
    color = 0
    i = 0
    raritycheck = 0
    while i < 6 and raritycheck == 0:
        if rarityluck <= partialSum(pull_rate, i):
            rarity = i
            raritycheck = 1
        i = i + 1
    j = 0
    colorcheck = 0
    colorluck = random.randint(1, partialSum(char_pool[rarity], 3))
    while j < 4 and colorcheck == 0:
        if colorluck <= partialSum(char_pool[rarity], j):
            color = j
            colorcheck = 1
        j = j + 1     
    result = [rarity, color]
    return result
    
def SummonCircle():
    # This summoning circle will allow us to call in five summoning orbs.
    i = 0
    circle_color = [0, 0, 0, 0, 0]
    circle_rarity = [0, 0, 0, 0, 0]
    while i < 5:
        sumres = SummonResult()
        circle_color[i] = sumres[1]
        circle_rarity[i] = sumres[0]
        i = i + 1
    full_circle = SummoningCircle(circle_color, circle_rarity)
    return full_circle
        
def SummonSimulationResult(starting_orbs):
    #Takes an input of the orbs you have.
    orbs = starting_orbs
    focus_summoned = 0
    pity_count = 0 # Fortunately the pity count resets at the end of each circle instead of each summon.
    # We then do summoning sessions while we can still do them
    while orbs >= 5:
        #We summon a circle:
        print("The pity count is: " + str(pity_count))
        pull_rate = newPullRate(pity_count, bannertype)
        print(pull_rate);
        circle = SummonCircle();
        print(circle.color)
        print(circle.rarity)
        # We wanna check if we've summoned at least one before we leave. We also wanna keep a count of how many we summon in the session.
        summons = 0
        i = 0
        j = 0
        while summons == 0:
            while i <= 3:
                circle_target = summon_order[i]
                j = 0
                #The following condition translates to the following:
                #Either you're summoning on the target color you want, 
                #or you're just wanting to summon so you can get out of the circle because there are none of the color you want.
                while j <= 4 and (i == 0 or (i > 0 and summons == 0)) and orbs >= orbCost(summons):
                    if circle.color[j] == summon_order[i]:
                        print("Paying " + str(orbCost(summons)) + " to summon the " + str(j+1) + "th orb.")
                        print("It's a " + rarity_dict[circle.rarity[j]])
                        orbs -= orbCost(summons)
                        summons += 1
                        if circle.rarity[j] == 0 and summon_order[0] == circle.color[j]: #This is a 5 - star focus unit.
                            # V 0.3: We roll the dice if the color we summoned is the actual unit we want:
                            pity_count = 0
                            targetcheck = random.randint(1, char_pool[0][summon_order[0]])
                            if targetcheck == 1:
                                focus_summoned += 1
                                print("It's the target character!")
                        elif circle.rarity[j] == 1:
                            pity_count -= 20 #Setting it to zero was the old version of the pity rate, but I believe it usually reduces it by 1%, so that's minus 20.
                        elif circle.rarity[j] == 2 and summon_order[0] == circle.color[j] and target_is_fourstar: #This is a 4 - star focus unit.
                            # V 0.3: We roll the dice if the color we summoned is the actual unit we want:
                            pity_count += 1
                            targetcheck = random.randint(1, char_pool[2][summon_order[0]])
                            if targetcheck == 1:
                                focus_summoned += 1
                                print("It's the target character!")
                        else:
                            pity_count += 1
                        
                    j += 1
                i += 1
    return focus_summoned
################################
# This is the start of the code:
################################

# We ask the kind of banner that we are dealing with:
bannertype_is_valid = False
bannertype = 0
fourstar_is_required = False;
while bannertype_is_valid == False:
    print("Please specify the kind of banner: ")
    print("0 - Legendary Banner [8% Focus]")
    print("1 - Revival Banner [4% Focus]")
    print("2 - Regular Banner [3% Focus]")
    print("3 - 4-Star Focus Banner [3% Focus, 4-Star Focus required]")
    print("4 - Double Special Heroes Banner [6% Focus, 4-Star Focus required]")
    print("5 - Legendary Hero Remix Banner [6% Focus]")
    bannertype = int(input())
    if bannertype <= 5:
        pull_rate = pullrate_dict[bannertype]
        bannertype_is_valid = True
        if bannertype == 3 or bannertype == 4:
            fourstar_is_required = True
    else:
        print("Invalid banner type.")

        
# We ask the set of 5-star focus units that we have:
fivestar_pool_is_valid = False
focus_pool_fivestar = [0, 0, 0, 0]
while fivestar_pool_is_valid == False:
    print("Please input the number of (red, blue, green, and colorless) 5-star focus units (4 Inputs):")
    focus_pool_fivestar[0] = int(input())
    focus_pool_fivestar[1] = int(input())
    focus_pool_fivestar[2] = int(input())
    focus_pool_fivestar[3] = int(input())
    if partialSum(focus_pool_fivestar, 3) >= 1:
        fivestar_pool_is_valid = True
        char_pool[0] = focus_pool_fivestar
        print(char_pool)
    else:
        print("Invalid set. Must have at least one 5-star focus unit.")

# We ask for the set of 4-star focus units if it is required.
focus_pool_fourstar = [0, 0, 0, 0]
fourstar_pool_is_valid = False

if fourstar_is_required == True:
    fourstar_pool_is_valid = False
    while fourstar_pool_is_valid == False:
        print("The banner type requires a four-star pool. \nPlease enter the number of (red, blue, green, and colorless) 4-star focus units (4 Inputs):")
        focus_pool_fourstar[0] = int(input())
        focus_pool_fourstar[1] = int(input())
        focus_pool_fourstar[2] = int(input())
        focus_pool_fourstar[3] = int(input())
        if partialSum(focus_pool_fourstar, 3) >= 1:
            fourstar_pool_is_valid = True
            char_pool[2] = focus_pool_fourstar
            print(char_pool)
        else:
            print("Invalid set. Must have at least one 4-star focus unit.")
        

# This set will ask for the order of summoning priority. The assumption is the first one is the target.
order_is_valid = False
summon_order = [0, 0, 0, 0]
color_check = [0, 0, 0, 0]
target_is_fourstar = False
fourstar_check_input = 0
while order_is_valid == False:
    print("Please input the order of summoning (4 Inputs): ")
    print("(0 = Red, 1 = Blue, 2 = Green, 3 = Colorless)")
    summon_order[0] = int(input())
    summon_order[1] = int(input())
    summon_order[2] = int(input())
    summon_order[3] = int(input())
    i = 0
    j = 0
    while i <= 3:
        j = 0
        while j <= 3:
            if summon_order[i] == j:
                color_check[j] += 1
            j += 1
        i += 1
    if color_check == [1, 1, 1, 1]:
        order_is_valid = True
        # We give a check whether or not the target is a 4-star unit.
        if char_pool[2][summon_order[0]] >= 1:
            print("Is your target character also a 4-star focus unit?")
            print("1 - Yes. \nelse - No.")
            fourstar_check_input = int(input())
            if fourstar_check_input == 1:
                target_is_fourstar = True
    else:
        print("Order is invalid.")
        color_check = [0, 0, 0, 0]
        

#We start with 1000 simulations:
i = 1
full_results = []
while i <= 1:
    full_results.append(SummonSimulationResult(300))
    print("Simulation number: " + str(i))
    i += 1
    
full_results.sort()
print(full_results)
        
input("Press ENTER to continue.")