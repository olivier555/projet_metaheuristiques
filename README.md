# Algorithme génétique pour le problème de couvertur connexe minimum dans les réseaux de capteurs



## Librairies nécessaires

Le code utilise les librairies suivantes:
* numpy
* matplotlib
* random
* pandas
* timeit
* copy
* scipy
* re

## Lancer le code

### Charger les données du problèmes

On utilise la class Data située dans data.py.

Cette classe doit être initialisé avec R_com et R_sens.
De plus, si l'on veut créer une grille, il faut fournir nb_rows et nb_columns.
Si l'on veut charger les points depuis un fichier, on doit fournir file_name

"""
__init__(self, r_com, r_sens, nb_rows = None, nb_columns = None, file_name = None)
"""

### Lancer l'heuristique

La fonction a utiliser pour lancer l'heuristique est optimize dans le fichier optimize.py.
On doit fourniré également les différents paramètres de l'heuristiques

"""
optimize(data, nb_population, nb_iter_max, t_max, p_mutation_min, p_mutation_max, prop_children_kept, stagnancy_max)
"""

## Fichiers

* data: classe contenant les données du problème
* elementar_timings:
* fusion: classe permettant de fusionner deux solution. Elle est utilisée dans l'algorithme génétique.
* genetic: fonction contenant l'algorithme génétique et la définition de la fonction de mutation.
* graph: class contenant une structure de graphe
* greedy_connect:
* initial_path_finder: classe permettant de créer des solutions réalisables
* local_search: fonction supprimant les capteurs inutiles à une solution
* lower_bound_founder: classe permettant de calculer une borne inférieure au problème
* optimize: fonction pour lancer l'heuristique complète. Le fichier contient également les fonctions permettant de créer la population initiale et le post-traitement pour la meilleure solution.
* plot_timings:
* search_two_to_one: classe permettant de remplacer des couples de capteurs par un seul capteur dans une solution
* solution: classe contenant la structure d'une solution et les tests permettant de savoir si elle est réalisable.
* switch: classe permettant de déplacer les capteurs d'une solution
* test_timing:
* visualization: classe permettant de visualiser une solution.