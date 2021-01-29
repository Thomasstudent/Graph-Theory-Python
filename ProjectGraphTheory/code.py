import pandas as pd
import numpy as np
import random

#Part Two of the ADSA project
def Coloring(NodeList,listeIndex):
    #We initialize an empty dictionnary
    ColList={}
    #We initialize 4 colors which will be used to colorise the graph
    colors=[1,2,3,4]

    #While all nodes are not colorize:
    while(len(listeIndex)>0):
        indexMaximum=listeIndex.pop()
        #We check the color of the neighbors of the actual node
        coloredNeighbors=[]
        for element in NodeList[indexMaximum]:
            for element1 in ColList.items():
                if element1[0]==element:
                    coloredNeighbors.append(element1[1])
        #We delete the color of the neighbors to the list of colors available
        colorsAvailable = [value for value in colors if value not in coloredNeighbors]
        #We colorize the node
        ColList[indexMaximum]=min(colorsAvailable)
    return ColList

def PartTwo():
    NodeList=[
        [1,4,5],
        [0,2,6],
        [1,3,7],
        [2,4,8],
        [0,3,9],
        [0,7,8],
        [1,8,9],
        [2,5,9],
        [3,5,6],
        [4,6,7],
    ]
    print("In this exercise we use the following adjacency list : ")
    print(NodeList)
    print("\n")

    #We initialize three empty lists
    PlayersWithSameColorThanPlayerOne=[]
    PlayersWithSameColorThanPlayerFour=[]
    PlayersWithSameColorThanPlayerFive=[]

    #We initialize three empty dictionnaries
    resultatOne={i:0 for i in range(0,10)}
    resultatFour={i:0 for i in range(0,10)}
    resultatFive={i:0 for i in range(0,10)}

    for i in range(0,400):
        #we are going to colorize the nodes in a random order.
        listeIndex=[0,1,2,3,4,5,6,7,8,9]
        random.shuffle(listeIndex)
        ColList=Coloring(NodeList,listeIndex)
        #We add the nodes with same color than node 1,node 4 or node 5 in the corresponding list.
        PlayersWithSameColorThanPlayerOne.extend([value[0] for value in ColList.items() if value[1]==ColList[1]])
        PlayersWithSameColorThanPlayerFour.extend([value[0] for value in ColList.items() if value[1]==ColList[4]])
        PlayersWithSameColorThanPlayerFive.extend([value[0] for value in ColList.items() if value[1]==ColList[5]])
    #We calculate how many times node appeared in the previous lists
    for i in range(0,10):
        resultatOne[i]+=PlayersWithSameColorThanPlayerOne.count(i)
        resultatFour[i]+=PlayersWithSameColorThanPlayerFour.count(i)
        resultatFive[i]+=PlayersWithSameColorThanPlayerFive.count(i)
    #We calculate percentages.
    for i in range(0,10):
        resultatOne[i]=round(((resultatOne[i]/400)*100),2)
        resultatFour[i]=round(((resultatFour[i]/400)*100),2)
        resultatFive[i]=round(((resultatFive[i]/400)*100),2)

    print("After {} iterations :".format(400))
    print("\n")
    print("These are the probabilities when the first importor is the player One : ")
    print(resultatOne)
    print("\n")
    print("These are the probabilities when the first importor is the player Four : ")
    print(resultatFour)
    print("\n")
    print("These are the probabilities when the first importor is the player Five : ")
    print(resultatFive)

#Part Three of ADSA project.
def Floyd_Warshall(map):
    shape=map.shape
    #matrixOfDistance is the output and it represents the length between
    #all the pairs of vertices
    matrixOfDistance=pd.DataFrame(np.zeros(shape),columns=map.columns,index=map.columns)
    #matrixOfPredecessor represent the parent of each node
    #we initiate it at 0
    matrixOfPredecessor=pd.DataFrame(np.zeros(shape),columns=map.columns,index=map.columns)
    #we initialise both of them
    for index in range(0,shape[0]):
        for column in range(0,shape[1]):
            #if there is no edge between vertice u and vertice v, the case [u,v]
            #will take the value 1000 (~ infinite)
            if index!=column and map.iloc[index,column]==0:
                matrixOfDistance.iloc[index,column]=1000
                matrixOfPredecessor.iloc[index,column]='None'
            elif map.iloc[index,column]>0:
                matrixOfDistance.iloc[index,column]=map.iloc[index,column]
                matrixOfPredecessor.iloc[index,column]=map.index[index]
            else:
                matrixOfPredecessor.iloc[index,column]='None'
    #We test all path between all rooms and we keep the shortest.
    for k in range(0,shape[0]):
        for i in range(0,shape[0]):
            for j in range(0,shape[0]):
                if matrixOfDistance.iloc[i,j]>matrixOfDistance.iloc[i,k]+matrixOfDistance.iloc[k,j]:
                    matrixOfDistance.iloc[i,j]=matrixOfDistance.iloc[i,k]+matrixOfDistance.iloc[k,j]
                    matrixOfPredecessor.iloc[i,j]=map.index[k]

    return matrixOfDistance,matrixOfPredecessor

def PartThree():
    names=['Upper Engine','Reactor','Security','Lower Engine','Medbay','Electrical','Cafeteria',
        'Storage','Weapons','O2','Navigation','Shields','Admin','Communication']

    #This is the adjacency matrix we use for players
    map = pd.DataFrame(np.array([[0,5.5,5,6.5,6,0,8.3,0,0,0,0,0,0,0],
                             [5.5,0,4,5.5,0,0,0,0,0,0,0,0,0,0],
                             [5,4,0,5,0,0,0,0,0,0,0,0,0,0],
                             [6.5,5.5,5,0,0,7.7,0,8.4,0,0,0,0,0,0],
                             [6,0,0,0,0,0,6.4,0,0,0,0,0,0,0],
                             [0,0,0,7.7,0,0,0,5.9,0,0,0,0,0,0],
                             [8.3,0,0,0,6.4,0,0,7,4.5,0,0,0,6.3,0],
                             [0,0,0,8.4,0,5.9,7,0,0,0,0,5.7,5.7,5.3],
                             [0,0,0,0,0,0,4.5,0,0,3.5,6.3,6.9,0,0],
                             [0,0,0,0,0,0,0,0,3.5,0,5.9,7.1,0,0],
                             [0,0,0,0,0,0,0,0,6.3,5.9,0,6.8,0,0],
                             [0,0,0,0,0,0,0,5.7,6.9,7.1,6.8,0,0,4],
                             [0,0,0,0,0,0,6.3,5.7,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,5.3,0,0,0,4,0,0]]),
                   columns=names, index=names)

    matrixOfDistance,matrixOfPredecessor=Floyd_Warshall(map)
    print("These results are for players :")
    print("\n")
    print("This is the adjacency matrix : ")
    print(map)
    print("\n")
    print("This is the distance between each rooms : ")
    print(matrixOfDistance)
    print("\n")
    print("This is the path between each rooms : ")
    print(matrixOfPredecessor)

    #This is the adjacency matrix we use for impostors
    map_impostors = pd.DataFrame(np.array([[0,0.001,5,6.5,6,0,8.3,0,0,0,0,0,0,0],
                             [0.001,0,4,0.001,0,0,0,0,0,0,0,0,0,0],
                             [5,4,0,5,0.001,0.001,0,0,0,0,0,0,0,0],
                             [6.5,0.001,5,0,0,7.7,0,8.4,0,0,0,0,0,0],
                             [6,0,0.001,0,0,0.001,6.4,0,0,0,0,0,0,0],
                             [0,0,0.001,7.7,0.001,0,0,5.9,0,0,0,0,0,0],
                             [8.3,0,0,0,6.4,0,0,7,4.5,4.4,4,3.1,0.001,0],
                             [0,0,0,8.4,0,5.9,7,0,0,0,0,5.7,5.7,5.3],
                             [0,0,0,0,0,0,4.5,0,0,3.5,0.001,6.9,4.5,0],
                             [0,0,0,0,0,0,4.4,0,3.5,0,5.9,7.1,4.4,0],
                             [0,0,0,0,0,0,4,0,0.001,5.9,0,0.001,4,0],
                             [0,0,0,0,0,0,3.1,5.7,6.9,7.1,0.001,0,3.1,4],
                             [0,0,0,0,0,0,0.001,5.7,4.5,4.4,4,3.1,0,0],
                             [0,0,0,0,0,0,0,5.3,0,0,0,4,0,0]]),
                   columns=names, index=names)

    matrixOfDistance_impostors,matrixOfPredecessor_impostors=Floyd_Warshall(map_impostors)
    print("These results are for impostors :")
    print("\n")
    print("This is the adjacency matrix : ")
    print(map)
    print("\n")
    print("This is the distance between each rooms : ")
    print(matrixOfDistance_impostors)
    print("\n")
    print("This is the path between each rooms : ")
    print(matrixOfPredecessor_impostors)


#Part Four of ADSA project:

def Hamiltonian(map,roomDepart):
    #We make a copy so modifications to the copy will not be reflected in the original map.
    mapCopy=map.copy()
    #We start our circuit with the first room
    hamiltonian_circuit=[roomDepart]
    roomActuelle=roomDepart
    #We stop when there are 15 rooms in the path (14 rooms of the map + 1 because it is a circuit )
    while(len(hamiltonian_circuit)<15):
        #We look at all the neighbors of the current room
        allNeighbors=mapCopy.loc[roomActuelle,:]
        #We order the neighbors by distance
        allNeighbors=allNeighbors.sort_values()
        #We only keep the neighbors which are connected to the current node
        allNeighbors=allNeighbors[allNeighbors>0]
        #If our current room does not have neighbors we stop
        if len(allNeighbors)==0:
            break
        #We obtain the name of the closest room
        roomNext=allNeighbors.index[0]
        #If the closest room is the first room, we take the second closest one if there is one
        if roomNext==roomDepart and len(hamiltonian_circuit)!=15:
            try:
                roomNext=allNeighbors.index[1]
            except:
                break
        #We delete the path between the current node and the other nodes
        mapCopy.loc[:,roomNext]=0
        roomActuelle=roomNext
        hamiltonian_circuit.append(roomActuelle)

    if len(hamiltonian_circuit)==15:
        print("We find an Hamiltonian Circuit : ")
        print(hamiltonian_circuit)
    else:
        print("There is no Hamiltonian Circuit from {}".format(roomDepart))
        print(hamiltonian_circuit)

def HamiltonianC(map,roomDepart):
    #We make a copy so modifications to the copy will not be reflected in the original map.
    mapCopy=map.copy()
    #We initialize some variables
    compteur=0
    time=0
    hamiltonian_path=[]
    roomNext=roomDepart
    #We stop when there are 14 room in the path.
    while(compteur<14):
        #We delete the path between the current room and the other rooms.
        mapCopy.loc[:,roomNext]=0
        hamiltonian_path.append(roomNext)
        #We look at all the neighbors of the current room
        ligne=mapCopy.loc[roomNext,:]
        #We order the neighbors by distance
        ligne=ligne.sort_values()
        #We only keep the neighbors which are connected to the current node
        ligne=ligne[ligne>0]
        #If our current room does not have neighbors we stop
        if len(ligne)==0:
            break
        #We obtain the name and distance of the closest room
        roomNext=ligne.index[0]
        time=time+ligne[0]
        compteur=compteur+1

    if compteur==13:
        print("There is an hamiltian path from {}, duration :{} seconds".format(roomDepart,round(time,2)))
        print(hamiltonian_path)

def PartFour():

    names=['Upper Engine','Reactor','Security','Lower Engine','Medbay','Electrical','Cafeteria',
        'Storage','Weapons','O2','Navigation','Shields','Admin','Communication']

    map = pd.DataFrame(np.array([[0,5.5,5,6.5,6,0,8.3,0,0,0,0,0,0,0],
                                 [5.5,0,4,5.5,0,0,0,0,0,0,0,0,0,0],
                                 [5,4,0,5,0,0,0,0,0,0,0,0,0,0],
                                 [6.5,5.5,5,0,0,7.7,0,8.4,0,0,0,0,0,0],
                                 [6,0,0,0,0,0,6.4,0,0,0,0,0,0,0],
                                 [0,0,0,7.7,0,0,0,5.9,0,0,0,0,0,0],
                                 [8.3,0,0,0,6.4,0,0,7,4.5,0,0,0,6.3,0],
                                 [0,0,0,8.4,0,5.9,7,0,0,0,0,5.7,5.7,5.3],
                                 [0,0,0,0,0,0,4.5,0,0,3.5,6.3,6.9,0,0],
                                 [0,0,0,0,0,0,0,0,3.5,0,5.9,7.1,0,0],
                                 [0,0,0,0,0,0,0,0,6.3,5.9,0,6.8,0,0],
                                 [0,0,0,0,0,0,0,5.7,6.9,7.1,6.8,0,0,4],
                                 [0,0,0,0,0,0,6.3,5.7,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,5.3,0,0,0,4,0,0]]),
                       columns=names, index=names)

    print("This is the adjacency matrix : ")
    print(map)
    print("\n")

    #We start from each rooms
    for element in names:
        Hamiltonian(map,element)
    print("\n")
    for element in names:
        HamiltonianC(map,element)


if __name__=='__main__':
    exercise=2
    if exercise==1:
        print("Exercise 1")
    elif exercise==2:
        print("Exercise 2 : ")
        PartTwo()
    elif exercise==3:
        print("Exercice 3 : ")
        PartThree()
    elif exercise==4:
        print("Exercice 4 : ")
        PartFour()
    else:
        print("End")
