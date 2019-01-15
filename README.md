### Watershed

Le sujet retenu est la segmentation par ligne de partage des eaux. Ce dépôt propose une implémentation de l'article de [Soille and Vincent (1991)](https://pdfs.semanticscholar.org/a381/9dda9a5f00dbb8cd3413ca7422e37a0d5794.pdf) 

### Structure du dépôt 

Le dépôt contient : 
 - le fichier watershed.py qui contient l'algorithme de la LPE classique
 - un dossier de test qui montre les résultats obtenu.
 
 
 ### Documentation scientifique
 
 Le principe de base consiste à répresenter une image comme un relief topographique qui servira par la suite, a simuler un écoulement du niveau des eaux. 
 
 Les intensités de notre image (en niveau de gris) nous permettent d'obtenir une information "d'altitude". En effet, plus les pixels ont une valeur d'intensité blanche, plus l'altitude sera elevée. 

![Ligne de partage des eaux](https://xphilipp.developpez.com/articles/segmentation/regions/images/ws-shed.png)

Sur cette exemple, on voit deux bassins inondés. Lorsque la ligne se croise, elle est appelée : ligne de partage des eaux. Celle-ci permet la distinction entre deux régions.

Dans un premier temps, il faut récupérer l'altitude minimale et l'altitude maximale de notre image. Les pixels doivent être traité en fonction de leur intensité (on commence à partir d'une altitude faible et on augmente progressivement jusqu'à l'altitude max). Il faut donc au préalable avoir une image triée en fonction de son niveau d'intensité.

Ensuite, pour chaque niveau d'intensité, l'algorithme va récupérer les pixels correspondant au niveau d'eau courant :
Si le pixel n'est associé à aucune région, il faut créer une region et y associer le pixel actuel. Sinon, il faut faire croître la région auquel appartient le pixel. Il y a donc trois notions importantes :

#### Région correspondante au pixel courant
- Si le voisinage du pixel contient des LPE, alors le pixel appartient à la LPE
- Si le voisinage du pixel contient plusieurs régions, alors le pixel appartient à la LPE
- Si le voisinage du pixel contient une région commune, alors le pixel appartient à cette région 

#### Croissance d'une région
Lorsque l'on veut traiter un pixel, nous allons placer ses voisins dans une file d'attente. Ces pixels seront traités selon les règles énumérées précédemment. Après cette étape, le niveau d'eau est incrémenté.

#### Création d'une région

Lorsque la file d'attente est vide, on crée une nouvelle région et on lui associe le pixel courant. Ensuite, nous ajoutons ses voisins dans la file d'attente et on recommence le traitement en suivant les règles énoncées précédemment. 


### Documentation utilisateur

Pour lancer le programme, il suffit simplement de lancer la ligne de commande suivante : 
```
python watershed.py [input_image] [output_image] [seuillage] 
```

Le seuillage permettra de réduire l'écart d'intensité entre deux pixels. Cela permettra d'avoir moins de régions lors du résultat.
