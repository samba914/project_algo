import fileinput

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

def construction(G):
    #fonction à implémenter
    print("construction")




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
        if(l1[0]=="p" and l1[1]=="cep"):
            key=int(l1[2])
            value=int(l1[3])
            if key not in G:
                G[key]=list()
            G[key].append(value)
        elif l1[0]!="c":
            key=int(l1[0])
            value=int(l1[1])
            if key not in G:
                G[key]=list()
            G[key].append(value)
    print(G)
    #done
       
    #2. call the grasp fonction
    #3. write the solution in a output file