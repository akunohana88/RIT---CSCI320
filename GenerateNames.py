import random


def randomPairing(id1, id2):
    file = open("generatedNamed", "w+")
    made = set()
    for i in range(400):
        j = random.randrange(1, len(id1))
        k = random.randrange(1, len(id2))
        if (j,k) not in made:
        #made.append((j,k))
            made.add((j,k))
            file.writelines(str(id1[j]) +","+ str(id2[k]) +"\n")