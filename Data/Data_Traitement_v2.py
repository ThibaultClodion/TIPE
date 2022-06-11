import matplotlib.pyplot as plt


def extract_data(filename):
    """
    Entrée : le nom d'un fichier csv dont on veut extraire les données

    Sortie:
    - nb_experience : entier du nombre d'expérience faite
    - dernieres_sortie : tableau contenant les derniers temps de sortie pour chaque simulation
    - temps_sortie : matrice dont les lignes correspondent aux temps de sortie par ordre croissant d'une simulation
    """
    with open(filename, 'r', encoding='latin-1') as f:
        dernieres_sortie = []  # Dernier temps de sortie par simulation
        temps_sortie = []  # Chaque ligne correspond aux temps de sorties par ordre croissant d'une simulation

        # Lecture des lignes
        lignes = f.read().splitlines()

        # Nombres de simulations effectuées
        nb_experience = len(lignes) - 1

        for ligne in lignes[1:]:  # A partir de la deuxième ligne du csv car on considère pas les titres

            # Récupération de la ligne sous forme de tableaux
            liste_ligne = [float(x.replace(',', '.')) for x in ligne.split(";") if x != '']

            # Ajout des données aux tableaux
            dernieres_sortie.append(liste_ligne[249])  # Le dernier temps de sortie correspond à la dernière colonne
            temps_sortie.append(liste_ligne[2:])

    return nb_experience, dernieres_sortie, temps_sortie


def nb_survivant_temps(filename, pas):
    """
    Entrée :
    - filename : le nom d'un fichier csv dont on veut extraire les données
    - pas : pas du temps pour le graphique de sortie

    Sortie : Affichage d'un graphique du nombre de personnes non sortie en fonction du temps
    (La précision de la courbe dépend du pas considéré)
    """
    ## Traitement des données ##

    nb_exp, derniers_sortie, temps_sortie = extract_data(filename)

    # Traitement pour obtenir un grand tableau temps_sortie triée par temps croissant
    temps_sortie = [item for sublist in temps_sortie for item in sublist]
    temps_sortie.sort()
    longueur_temps_sortie = len(temps_sortie)

    nb_non_sorties = [0]  # Tableau comptant le nombre de personne non sortie par pas
    tab_pas = [0]  # Tableau contenant les différent temps considérés (qu'on incrémente par le pas)

    ind_nb_non_sorties = 0  # Permet de savoir quel indice du tableau est a considérée
    ind_temps = 0  # Permet de savoir quel temps est à considérer

    while ind_temps != longueur_temps_sortie:  # Dans ce cas plus pratique d'une boucle for

        if temps_sortie[ind_temps] - ind_nb_non_sorties * pas <= pas:
            # Cas où le temps considérée est dans un intervalle du pas
            nb_non_sorties[ind_nb_non_sorties] += 1
            ind_temps += 1

        else:
            # Cas où le temps considérée dépasse l'intervalle du pas
            nb_non_sorties.append(nb_non_sorties[ind_nb_non_sorties])

            ind_nb_non_sorties += 1

            tab_pas.append(pas * ind_nb_non_sorties)

    # A ce moment nb_non_sorties comptient pour chaque pas le nombres de personnes sortie
    # Il faut donc "inverser la signification de ce tableau" car on veut le nombre de personne non sortie
    # De plus il faut moyenner les valeurs obtenues car on veut qu'au maximum il y est 250 personnes non sortie

    nb_non_sorties = [250 - item / nb_exp for item in nb_non_sorties]

    # Ajout de 20 valeurs dans nb_non_sorties et tab_pas
    # Ceci pour que les graphes ne finissent pas "brutalement"
    for i in range(1, 21):
        nb_non_sorties.append(nb_non_sorties[ind_nb_non_sorties])
        tab_pas.append(pas * (ind_nb_non_sorties + i))

    # Calcul du temps moyen de la dernière sortie
    moyenne_derniere_sortie = sum(derniers_sortie) / nb_exp

    # Calcul du dernier temps de sortie observée
    max_derniere_sortie = max(derniers_sortie)

    ## Affichage des Graphes ##
    plt.figure()
    plt.plot(tab_pas, nb_non_sorties)  # Graphe principal (celui voulu)

    # Ajout sur le graphe de la moyenne de la dernière sortie et du dernier temps de sortie
    plt.axvline(moyenne_derniere_sortie, c='r', ls='--',
                label='Temps dernière sortie en moyenne : {:.2f}'.format(moyenne_derniere_sortie))
    plt.axvline(max_derniere_sortie, c='g', ls='--',
                label='Temps dernière sortie : {:.2f}'.format(max_derniere_sortie))

    plt.title("Nombre de personnes non sortie en fonction du temps pour le batiment : \n" + filename)

    # Noms des axes
    axes = plt.gca()
    axes.set_ylabel("Nombre de personnes non sortie")
    axes.set_xlabel("t (s)")

    plt.legend()
    plt.grid()


def histogramme_dernier_temps(filename):
    ## Traitement des données ##

    nb_exp, derniers_sortie, temps_sortie = extract_data(filename)

    ## Affichage des graphes ##
    plt.figure()

    plt.bar([i for i in range(0, len(derniers_sortie))], derniers_sortie)

    plt.title("Temps de la dernière sortie pour le bâtiment en fonction de la simulation considérée : \n" + filename)
    # Noms des axes
    axes = plt.gca()
    axes.set_ylabel("Dernier temps de sortie")
    axes.set_xlabel("n° simulation")

    #plt.legend()
    plt.grid()


def main():
    # nb_survivant_temps('Building 2 door, 250 tables uniform with Solution 1.csv', 0.1)
    # nb_survivant_temps('Building 2 door, 250 tables uniform with Solution 2.csv', 0.1)
    # nb_survivant_temps('Building 2 door, 250 tables uniform with Solution 3.csv', 0.1)

    histogramme_dernier_temps('Building 2 door, 250 tables uniform with Solution 1.csv')
    histogramme_dernier_temps('Building 2 door, 250 tables uniform with Solution 2.csv')
    histogramme_dernier_temps('Building 2 door, 250 tables uniform with Solution 3.csv')

    plt.show()


main()
