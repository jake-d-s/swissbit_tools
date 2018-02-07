import random

def roll(d=6, n=1, plus=0):
    rolls = []
    for i in range(n):
        rolls.append(random.randrange(1,d+1))
        
    print("Rolled " + str(n) + " d" + str(d) + " for " + str(rolls))
    total = sum(rolls) + plus
    print("Total = " + str(sum(rolls)) + " + " + str(plus))
    print("Total = " + str(total))
    return total
    
def modifier(stat):
    return stat // 2 - 5
    
class Character():
    
    def __init__(self):
        self.stats = {"STR" : 11, "DEX" : 20,  "CON" : 15, "INT" : 9, "WIS" : 18, "CHA" : 11}
        self.proficiency_bonus = 3
        self.skills = {"Athletics" : ("STR", 1),
                       "Acrobatics" : ("DEX", 1),
                       "Sleight of Hand" : ("DEX", 0),
                       "Stealth" : ("DEX", 1),
                       "Arcana" : ("INT", 0),
                       "History" : ("INT", 0),
                       "Investigation" : ("INT", 0),
                       "Nature" : ("INT", 0),
                       "Religion" : ("INT", 0),
                       "Animal Handling" : ("WIS", 0),
                       "Insight" : ("WIS", 0),
                       "Medicine" : ("WIS", 0),
                       "Perception" : ("WIS", 1),
                       "Survival" : ("WIS", 0),
                       "Deception" : ("CHA", 0),
                       "Intimidation" : ("CHA", 0),
                       "Performance" : ("CHA", 1),
                       "Persuasion" : ("CHA", 0) }
                            
    def roll_skill(self, skill, adv=0):

        print("Rolling " + skill)
        
        stat_bonus = modifier(self.stats[self.skills[skill][0]])
        proficiency_bonus = int(self.skills[skill][1] * self.proficiency_bonus)
        
        print("Bonus from " + self.skills[skill][0] + " : " + str(stat_bonus))
        print("Bonus from Proficiency : " + str(proficiency_bonus))
        total = roll(d=20, n=1, plus=(stat_bonus + proficiency_bonus))
        return total
        
    
if( __name__ == "__main__"):
    monk = Character()
    for skill in monk.skills:
        monk.roll_skill(skill)
        print()