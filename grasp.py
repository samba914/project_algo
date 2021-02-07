import fileinput
import heapq
import math
import random
import time

"""
la fonction constructDict(Edges) prend en paramètre une liste d'arretes Edges et n le nombre de sommets
Elle retourne le graphe construit à l'aide de Edges
"""


def constructDict(Edges, n):
    G = {}

    for edge in Edges:
        key = int(edge[0])
        value = int(edge[1])
        if key not in G:
            G[key] = list()
        if value not in G:
            G[value] = list()
        G[key].append(value)
        G[value].append(key)
    for i in range(1, n+1):
        if i not in G.keys():
            G[i] = list()
    return G


"""
La fonction N(G,i) prend en paramètre le graphe G et le sommet i
La fonction retourne le nombre de voisin de i dans G
"""


def N(G, i):
    return len(G[i])


"""
La fonction getEdgesList(G) prend en paramètre le graphe G
et retourne la liste des arrêtes dans G
"""


def getEdgesList(G):
    Edges = set()
    for node in G:
        for voisin in G[node]:
            if (voisin,node) not in Edges:
                Edges.add((node,voisin))
    return Edges


"""
La fonction costP(i,G,C) prend en paramètre un sommet i,
un graphe G et C qui est un sous ensemble de G 
Elle renvoie costP, le nombre de voisin de i dans C
"""


def costP(i, G, C):
    costP = 0
    for node in C:
        if node in G[i]:
            costP = costP+1
    return costP


"""
La fonction costN(i,G,C) prend en paramètre un sommet i,
un graphe G et C qui est un sous ensemble de G 
Elle renvoie costN, le nombre de sommet avec qui i n'est pas voisin dans C 
"""


def costN(i, G, C):
    costN = len(C)-costP(i, G, C)
    return costN


"""
La fonction RN(i,G,C) prend en paramètre un sommet i,
un graphe G et C qui est un sous ensemble de G
Elle retourne costP-costN 
"""


def RN(i, G, C):
    return costP(i, G, C)-costN(i, G, C)


"""
construction(G) prend en paramètre un graphe G, et renvoie une solution du clustering de G de facon a avoir un ensemble de clique 
"""


def construction(G):
    K = random.randint(1, 5)
    V = set()
    CL = {}
    # récupération et stockage du nombre de voisins de chaque sommet dans un tableau
    E = []
    for node in G:
        V.add(node)
        # on va mettre dans le tableau le couple (n,u) ou u est le sommet et n le nombre de voisins de u
        heapq.heappush(E, (N(G,node),node))
    heapq._heapify_max(E)
    n = len(V)

    Kbest = K
    Kmin = round(max(Kbest-math.sqrt(n), 1))
    Kmax = round(min(Kbest+math.sqrt(n), n))
    K = random.randint(Kmin, Kmax)

    # on choisis les k premiers elements de V, chaque sommet sélectionné est le premier élément d’un nouveau groupe CL[i]
    for i in range(K):
        CL[i] = list()
        node = (heapq._heappop_max(E))[1]
        CL[i].append(node)
        V.remove(node)

    # tant que V n'est pas vide on choisis au hasard un sommet j dans V et on le met dans un cluster CL[i] de sorte que CL[i] maximizes RN(j,Ci) = cost+(j,Ci)−cost−(j,Ci)
    while V:
        node = V.pop()
        selectedCl = 0
        maxRn = RN(node,G,CL[selectedCl])
        lenCL = len(CL)

        for i in range(1, lenCL):
            if RN(node, G, CL[i]) > maxRn:
                maxRn = RN(node, G, CL[i])
                selectedCl = i
        # si d(node)=0 : node qui est le sommet en cours de traitement alors on met node dans un cluster à lui seul
        if len(G[node]) == 0:
            CL[lenCL] = list()
            CL[lenCL].append(node)
        else:
            CL[selectedCl].append(node)

    Edges = getEdgesList(G)

    for k in range(len(CL)):
        for node in CL[k]:
            # toutes les arretes reliant des sommets qui ne sont pas dans le même cluster sont supprimées
            for couple in set(Edges):
                u, v = couple
                if (u == node and v not in CL[k]) or (v == node and u not in CL[k]):
                    Edges.remove((u,v))

            # on lie tous les sommets d'un cluster pour former une clique
            for voisin in CL[k]:
                if node != voisin and ((node,voisin) not in Edges and (voisin,node) not in Edges):
                    Edges.add((node,voisin))

   # print(constructDict(Edges,n))
    return Edges, CL


def sumCost(C, VpC):
    sumCost = 0
    for i in C:
        sumCost = sumCost+costP(i, G, VpC)
    return sumCost


def LocalSearch(G, CL):

    V = set()
    for node in G:
        V.add(node)
    n = len(V)
    selectedCLIndex = 0
    maxsumCost = sumCost(CL[selectedCLIndex], V-set(CL[selectedCLIndex]))
    for i in range(1, len(CL)):
        sumcost = sumCost(CL[i], V-set(CL[i]))
        if sumcost > maxsumCost:
            selectedCLIndex = i
            maxsumCost = sumcost

    selectedCL = list(CL[selectedCLIndex])
    # Local search empty cluster
   
    if len(CL[selectedCLIndex]) > 1 or (len(CL[selectedCLIndex]) == 1 and len(G[CL[selectedCLIndex][0]]) != 0):
        nodeSeen = []
        while CL[selectedCLIndex] and len(nodeSeen) < len(CL[selectedCLIndex]):
            node = CL[selectedCLIndex].pop(0)
            
            if node not in nodeSeen:
                nodeSeen.append(node)
            maxCostSelectedClIndex = 0
            maxCost = costP(node, G, CL[0])
            for i in range(1, len(CL)):
                costp = costP(node, G, CL[i])
                if costp > maxCost:
                    maxCostSelectedClIndex = i
                    maxCost = costp

            CL[maxCostSelectedClIndex].append(node)
    
    # End Local search empty cluster
    solution1=constructGraphWithCL(CL,G)

    # Local search Split cluster
    selectedCLIndex = 0
    maxsumCost = sumCost(CL[selectedCLIndex], V-set(CL[selectedCLIndex]))
    for i in range(1, len(CL)):
        sumcost = sumCost(CL[i], V-set(CL[i]))
        if sumcost > maxsumCost:
            selectedCLIndex = i
            maxsumCost = sumcost
    
    Edges = getEdgesList(G)
    F = []
    if random.randint(0,1)==0:
        op=1
    else:
        op=-1
    if len(CL[selectedCLIndex]) > 2 :
        seenCouple = set()
        for node in CL[selectedCLIndex]:
            for voisin in CL[selectedCLIndex]:
                if node != voisin and (voisin,node) not in seenCouple and ((node,voisin) not in Edges and (voisin,voisin) not in Edges):
                    # on calcule cos+(i,C)+cos+(j,C) ou cos+(i,C)-cos+(j,C) en sachant que i et j ne sont pas voisins dans G
                    costIJ = costP(node, G, CL[selectedCLIndex])+op*costP(voisin, G, CL[selectedCLIndex])
                    heapq.heappush(F, (abs(costIJ), (node,voisin)))
                    seenCouple.add((node,voisin))

        heapq._heapify_max(F)
        # on prend le coupe (i,j) tel que cost+(i,C) et cost+(j,C) est le plus grand dans C

        if len(F) > 0:
            nodei, nodej = heapq._heappop_max(F)[1]
            lenCL = len(CL)
            CL[selectedCLIndex].remove(nodei)
            CL[selectedCLIndex].remove(nodej)
            CL[lenCL] = list()
            CL[lenCL+1] = list()
            CL[lenCL].append(nodei)
            CL[lenCL+1].append(nodej)
            while CL[selectedCLIndex]:
                node = CL[selectedCLIndex].pop()

                if RN(node, G, CL[lenCL]) > RN(node, G, CL[lenCL+1]):
                    CL[lenCL].append(node)
                else:
                    CL[lenCL+1].append(node)
  
    if solutionCost(G,constructGraphWithCL(CL,G))[0]<solutionCost(G,solution1)[0]:
        return constructGraphWithCL(CL,G)
    else:
        return solution1


    
    # END Local search Split cluster

def constructGraphWithCL(CL,G):
    Edges=getEdgesList(G)
    for k in range(len(CL)):
        for node in CL[k]:
            # toutes les arretes reliant des sommets qui ne sont pas dans le même cluster sont supprimées
            for couple in set(Edges):
                u, v = couple
                if (u == node and v not in CL[k]) or (v == node and u not in CL[k]):
                    Edges.remove((u,v))

            # on lie tous les sommets d'un cluster pour former une clique
            for voisin in CL[k]:
                if node != voisin and ((node,voisin) not in Edges and (voisin,node) not in Edges):
                    Edges.add((node,voisin))
    return constructDict(Edges, n)

    # fonction à implementer


def solutionCost(G, G1):
    EdgeG = getEdgesList(G)
    EdgeG1 = getEdgesList(G1)
    compareG1G = EdgeG.symmetric_difference(EdgeG1)
    for couple in EdgeG:
        node, voisin = couple
        if (node,voisin) in compareG1G and (voisin,node) in compareG1G:
            compareG1G.remove((node,voisin))
            compareG1G.remove((voisin,node))
    return len(compareG1G),compareG1G


def current_time():
    return round(time.time() * 1000)

# GRASP FONCTION


def grasp(G, Tmax):

    G1 = constructDict(construction(G)[0], len(G))
    timestart = current_time()
    while current_time()-timestart < Tmax:
        G2 = LocalSearch(G, construction(G)[1])
        if solutionCost(G, G2)[0] < solutionCost(G, G1)[0]:
            G1 = G2

    return G1


if __name__ == '__main__':
    # 1. find a way to extract data from the input file
    G = {}
    for line in fileinput.input():
        line = line.split("\n")[0]
        l1 = line.split(" ")

        if l1[0] == "p" and l1[1] == "cep":
            n = int(l1[2])
        elif l1[0] != "c":
            key = int(l1[0])
            value = int(l1[1])
            if key not in G:
                G[key] = list()
            if value not in G:
                G[value] = list()
            G[key].append(value)
            G[value].append(key)
    # s'il existe un sommet dont le degrés est nul on l'ajoute quand meme dans le dict
    for i in range(1, n+1):
        if i not in G.keys():
            G[i] = list()
    

    # done
    if(len(G) > 0):
        
        G1 = grasp(G, 10000)
        
        for coupl in solutionCost(G, G1)[1]:
            print(coupl[0],coupl[1])

        # print(LocalSearch(G,construction(G)[1]))

    # 2. call the grasp fonction
    # 3. write the solution in a output file
