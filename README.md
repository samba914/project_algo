Pour compiler le projet en PYTHON3 :
- Il faut mettre d'abord le fichier qui contient le graphe d'entrée (Ex : test.gr) dans le même repertoire que le fichier grasp.py
Note : Le fichier test.gr doit contenir uniquement : 
- une ligne commençant par 'p cep ' pour ensuite indiquer uniquement le nombre de sommets puis le nombre d'arêtes
- des lignes commençant par 'c' puis un commentaire 
- des lignes détermininant une arête en détaillant uniquement les extrémités de l'arête (chaque arête ne peut pas avoir une valeur supérieure que le nombre d'arête et on ne doit pas indiquer deux fois la même arête)
- les arêtes sont séparées par un espace


-Pour compiler le projet, ouvrez le terminal et tapez la commande :

"python3 graps.py < ne_nom_du_fichier_contenat_le_graphe > solution"

ex :  "python3 graps.py < test.gr> solution.txt"

La solution obtenue va être écrite dans le fichier solution.txt.

Attention !! il ne faut pas lancer juste: "python3 graps.py" pour éviter tout éventuel bug