### Watershed

Le sujet retenu est la segmentation par ligne de partage des eaux. Ce dépôt propose une implémentation de l'article de [Soille and Vincent (1991)](https://pdfs.semanticscholar.org/a381/9dda9a5f00dbb8cd3413ca7422e37a0d5794.pdf) 

### Structure du dépôt 

Le dépôt contient : 
 - le fichier watershed.py qui contient l'algorithme de la LPE classique
 - un dossier de test qui montre les résultats obtenu.
 
 
 ### Documentation scientifique
 
 Le principe de base consiste à répresenter une image comme un relief topographique qui servira par la suite, a simuler un écoulement du niveau des eaux. 
 
 Les intensités de notre image (en niveau de gris) nous permettent d'obtenir une information "d'altitude". En effet, plus les pixels ont une valeur d'intensité blanche, plus l'altitude sera elevée. 
