import matplotlib.pyplot as plt

""" Importation des données"""
nb_agents = []  # Nombres de personnes
derniere_sortie = []  # Correspond au temps de la dernière personne sortie
temps_sortie = []  # Chaque ligne correspond aux temps de sorties des personnes

filename = "Building With 2 door.csv"  # Le nom du fichier est changeable selon le fichier considéré

with open(filename, 'r', encoding='latin-1')as f:
    # Lecture des lignes
    lignes = f.read().splitlines()
    nb_experience = len(lignes) - 1  # Combien de simulations on été faite
    # Recupération des données
    for ligne in lignes[1:]:  # à Partir de la deuxième ligne car on ne considère pas les titres des colonnes
        # Récupération des champs séparés par des ';' dans ce cas
        liste_ligne = [float(x.replace(',', '.')) for x in ligne.split(";") if x != '']
        # Ajout des données aux tableaux des datas
        nb_agents.append(liste_ligne[0])
        derniere_sortie.append(liste_ligne[1])
        temps_sortie.append(liste_ligne[2:])

"""Traitement des données"""

""" Courbe des temps de sorties pour chaque simulation
for i in range(len(temps_sortie)):
    plt.plot([i for i in range(250)], temps_sortie[i])
    
plt.grid()
plt.show()
"""

"""Histogramme, nombre de personnes sorties par tranche de 1 seconde (pas très efficace en terme de complexité mais 
fonctionnel 
all_temps_sortie = [round(item) for sublist in temps_sortie for item in sublist]
nombre_personne = [0 for i in range(0, max(all_temps_sortie))]
temps_sortie = [i for i in range(0, max(all_temps_sortie))]
for temp in all_temps_sortie:
    nombre_personne[temp - 1] += 1

plt.bar(temps_sortie, nombre_personne, color='b')
plt.grid()
plt.show()"""

""" Graphique du nombre de personnes non sorties avant un temps t donnée"""

## Calcul/Traitement Des Données ##
temps_sortie_sort = [item for sublist in temps_sortie for item in sublist]
temps_sortie_sort.sort()

nb_non_sorties = [0]
pas_t = 0.1  # pas du temps pour le graphique
tab_pas_t = [0]

ind_nb_non_sortie = 0
ind_temps = 0

# Calcul du nombres de survivants par pas "pas_t"
while ind_temps != len(temps_sortie_sort):
    if temps_sortie_sort[ind_temps] - ind_nb_non_sortie * pas_t <= pas_t:
        nb_non_sorties[ind_nb_non_sortie] += 1
        ind_temps += 1
    else:
        nb_non_sorties.append(nb_non_sorties[ind_nb_non_sortie])
        ind_nb_non_sortie += 1
        tab_pas_t.append(pas_t * ind_nb_non_sortie)

# Moyennage du nombres de survivants par le nombre d'expérience réalisé
# Et 250 - x car on considère le nombre de personnes non sorties pas le nombre de personnes sorties.
nb_non_sorties_moyenne = [250 - item / nb_experience for item in nb_non_sorties]

# Ajout de 20 valeurs dans nb_non_sorties_moyenne et tab_pas_t pour les graphes
for i in range(0, 20):
    nb_non_sorties_moyenne.append(nb_non_sorties_moyenne[ind_nb_non_sortie])
    tab_pas_t.append(pas_t * (ind_nb_non_sortie + i))

# Calcul du temps moyen de la dernière sortie
moyenne_derniere_sortie = sum(derniere_sortie) / nb_experience
# Calcul du dernier temps de sortie observée
max_derniere_sortie = max(derniere_sortie)

## Affichage des Graphes ##
plt.plot(tab_pas_t, nb_non_sorties_moyenne)

# Ajout de la moyenne de la derniere sortie
plt.axvline(moyenne_derniere_sortie, c='r', ls='--',
            label='Temps dernière sortie en moyenne : {:.2f}'.format(moyenne_derniere_sortie))
plt.axvline(max_derniere_sortie, c='g', ls='--',
            label='Temps dernière sortie : {:.2f}'.format(max_derniere_sortie))
plt.legend()
plt.grid()
plt.show()
