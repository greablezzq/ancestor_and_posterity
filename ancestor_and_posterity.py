import random
import numpy as np
import matplotlib.pyplot as plt
# parameters
P_FINDWIFE = 0.85
AVER_KIDS_FOR_EACH_FAMILY = 2.5
INITIAL_MEN = 100
GENERATION = 100


class Man:
    def __init__(self, family, generation):
        self.family = family
        self.generation = generation
        self.couldfindWife = False
    
    def findWife(self):
        if(random.random()<P_FINDWIFE):
            self.couldfindWife = True
        return self.couldfindWife

    def giveBirth(self):
        woman = 0
        man = 0
        if(self.couldfindWife):
            kids = np.random.poisson(AVER_KIDS_FOR_EACH_FAMILY)
            for i in range(kids):
                if(random.random()<0.5):
                    woman += 1
                else:
                    self.family.addNewMan(self, Man(self.family, self.generation + 1))
                    man += 1
        return [woman, man]

class Family:
    def __init__(self, index):
        self.index = index
        self.hasPosterity = True
        self.manList = [[] for i in range(GENERATION+1)]
        self.manList[0].append(Man(self, 0))
        self.generation = 0

    def addNewMan(self, father, man):
        self.hasPosterity = True
        self.manList[self.generation+1].append(man)

    def goToNextGeneration(self):
        if(self.hasPosterity):
            self.generation += 1
            self.hasPosterity = False
    

def main():
    families = [Family(i) for i in range(INITIAL_MEN)]
    women=[0 for i in range(GENERATION + 1)]
    men=[0 for i in range(GENERATION + 1)]
    women[0] = INITIAL_MEN
    men[0] = INITIAL_MEN
    familiesWithPosterity=[0 for i in range(GENERATION)]
    menForEachFamily=[[] for i in range(GENERATION)]
    averMenForEachFamily=[0 for i in range(GENERATION)]
    for g in range(GENERATION):
        print("第" + str(g) + "代：男人"+str(men[g])+"人；女人"+str(women[g])+"人")
        for f in families:
            if(True):
                for m in f.manList[g]:
                    if(women[g]>0):
                        if(m.findWife()):
                            women[g] -= 1
                    children = m.giveBirth()
                    women[g+1] += children[0]
                    men[g+1] += children[1]
        for f in families:
            if(f.hasPosterity):
                familiesWithPosterity[g] += 1
                menForEachFamily[g].append(len(f.manList[g+1]))
        print("有"+str(familiesWithPosterity[g])+"个家庭有后代")
        averMenForEachFamily[g]=men[g+1]/familiesWithPosterity[g]
        for f in families:
            f.goToNextGeneration()
    print("这"+str(familiesWithPosterity[GENERATION - 1])+"个家族的下一代男人数分别为：")
    print(menForEachFamily[-1])
    plt.figure()
    plt.title("Families with posterity")
    plt.plot(familiesWithPosterity)
    plt.xlabel("Generation")
    plt.ylabel("Amount")
    plt.savefig("Families with posterity.png")
    plt.show()
    

    plt.figure()
    plt.title("Population(male)")
    plt.plot(men[1:GENERATION+1],label="Population")
    plt.plot(averMenForEachFamily, label="Average population for each family")
    plt.xlabel("Generation")
    plt.savefig("Average population for each family.png")
    plt.show()
    

main()