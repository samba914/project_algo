import fileinput
import heapq
import math
import random

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
            if (voisin, node) not in Edges:
                Edges.add((node, voisin))
    return Edges


"""
La fonction RN(i,G,C) prend en paramètre un sommet i,
un graphe G et C qui est un sous ensemble de G
Elle retourne costP-costN ou costN est le nombre de sommet avec qui i n'est pas voisin
et costP le nombre de voisin de i
"""


def RN(i, G, C):
    costP = 0
    for node in C:
        if node in G[i]:
            costP = costP+1
    costN = len(G)-costP

    return costP-costN

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
        heapq.heappush(E, (N(G, node), node))
    heapq._heapify_max(E)
    n = len(V)
 
    Kbest = K
    Kmin = round(max(Kbest-math.sqrt(n), 1))
    Kmax = round(min(Kbest+math.sqrt(n), n))
    K = random.randint(Kmin, Kmax)

    #on choisis les k premiers elements de V, chaque sommet sélectionné est le premier élément d’un nouveau groupe CL[i]
    for i in range(K):
        CL[i] = list()
        node = (heapq._heappop_max(E))[1]
        CL[i].append(node)
        V.remove(node)

    # tant que V n'est pas vide on choisis au hasard un sommet j dans V et on le met dans un cluster CL[i] de sorte que CL[i] maximizes RN(j,Ci) = cost+(j,Ci)−cost−(j,Ci)
    while V:
        node = V.pop()
        selectedCl = 0
        maxRn = RN(node, G, CL[selectedCl])
        lenCL = len(CL)
    
        for i in range(1, lenCL):
            if RN(node, G, CL[i]) > maxRn:
                maxRn = RN(node, G, CL[i])
                selectedCl = i

        if maxRn == ((-1)*n):
            CL[lenCL] = list()
            CL[lenCL].append(node)
        else:
            CL[selectedCl].append(node)
    
    Edges = getEdgesList(G)
    

    for k in range(len(CL)):
        for node in CL[k]:
            # toutes les arretes reliant des sommets qui ne sont pas dans le même cluster sont supprimées 
            for couple in set(Edges):
                u,v=couple
                if (u==node and v not in CL[k]) or (v==node and u not in CL[k]):
                    Edges.remove((u,v)) 

            # on lie tous les sommets d'un cluster pour former une clique
            for voisin in CL[k]:
                if node != voisin and ((node, voisin) not in Edges and (voisin, node) not in Edges):
                    Edges.add((node, voisin))

    return Edges


def LocalSearch(G):
    # fonction à implementer
    print("localsearch")

# GRASP FONCTION


def grasp(G, Tmax):
    """
    2: G∗ ← construction(G)
    3: tstart ← time()
    4: while time() − timestart < timemax do
    5:      G' ← construction(G)
    6:      G' ← Local Search(G')
    7:      if s(G') < s(G∗) then
    8:          G∗ ← G'
    9:      end if
    10: end while
    11: return G∗ as output
    12: end procedure
    """


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
    if(len(G)>0):
        construction(G)

    # 2. call the grasp fonction
    # 3. write the solution in a output file
