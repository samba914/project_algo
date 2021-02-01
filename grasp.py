import fileinput
import heapq
import math
import random

"""
La fonction N(G,i) prend en paramètre le graphe G et le sommet i
La fonction retourne le nombre de voisin de i dans G
"""
def N(G,i):
    return len(G[i])

"""
La fonction getEdgesList(G) prend en paramètre le graphe G
et retourne la liste des arrêtes dans G
"""
def getEdgesList(G):
    Edges=[]
    for node in G:
      for voisin in G[node]:
         Edges.append([node, voisin])
    return Edges

"""
La fonction RN(i,G,C) prend en paramètre un sommet i,
un graphe G et C qui est un sous ensemble de G
Elle retourne costP-costN ou costN est le nombre de sommet avec qui i n'est pas voisin
et costP le nombre de voisin de i
"""
def RN(i,G,C):
    costP=0
    for node in C:
        if node in G[i]:
            costP=costP+1
    costN=len(C)-costP

    return costP-costN

def construction(G):
    K=random.randint(1,5)
    V=set()
    CL={}
    #récupération et stockage du nombre de voisins de chaque sommet dans un tableau  
    E=[]
    for node in G:
        V.add(node)
        #on va mettre dans le tableau le couple (n,u) ou u est le sommet et n le nombre de voisins de u
        heapq.heappush(E,(N(G,node),node))
    heapq._heapify_max(E)
    n=len(V)
    print(V)

    Kbest=K
    Kmin=round(max(Kbest-math.sqrt(n),1))
    Kmax=round(min(Kbest+math.sqrt(n),n))
    K=random.randint(Kmin,Kmax)

    for i in range(K):
        CL[i]=list()
        node=(heapq._heappop_max(E))[1]
        CL[i].append(node)
        V.remove(node)
    print(CL)
    while V:
        node=V.pop()
        selectedCl=0
        maxRn=RN(node,G,CL[selectedCl])
        for i in range(1,len(CL)):
            if(RN(node,G,CL[i])>maxRn):
                maxRn=RN(node,G,CL[i])
                selectedCl=i
        CL[selectedCl].append(node)

    print(CL)

    
        
       



    
    
    





def LocalSearch(G):
    #fonction à implementer
    print("localsearch")

#GRASP FONCTION
def grasp(G,Tmax):
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
    #1. find a way to extract data from the input file
    G={}
    for line in fileinput.input():
        line=line.split("\n")[0]
        l1=line.split(" ")
        n=0
        if l1[0]=="p" and l1[1]=="cep":
            n=int(l1[3])
        elif l1[0]!="c":
            key=int(l1[0])
            value=int(l1[1])
            if key not in G:
                G[key]=list()
            if value not in G:
                G[value]=list()
            G[key].append(value)
            G[value].append(key)
    #si il existe un sommet dont le degrés est nul on l'ajoute quand meme dans le dict
    for i in range(1,n+1):
        if i not in G.keys():
            G[i]=list() 

    
            
    #done
    #construction(G)
       
    #2. call the grasp fonction
    #3. write the solution in a output file