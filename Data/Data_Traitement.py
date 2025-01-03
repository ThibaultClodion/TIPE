import matplotlib.pyplot as plt

nb_personnes = 200


def Extraire_Donnees(nom_fichier):
    """
    Entrée : le nom d'un fichier csv dont on veut extraire les données

    Sortie:
    - nb_experience : entier du nombre d'expérience faite
    - dernieres_sortie : tableau contenant les derniers temps de sortie pour chaque simulation
    - temps_sortie : matrice dont les lignes correspondent aux temps de sortie par ordre croissant d'une simulation
    """
    with open(nom_fichier, 'r', encoding='latin-1') as f:
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
            dernieres_sortie.append(
                liste_ligne[nb_personnes - 1])  # Le dernier temps de sortie correspond à la dernière colonne
            temps_sortie.append(liste_ligne[2:])

    return nb_experience, dernieres_sortie, temps_sortie


def nb_survivant_temps(nom_fichier, pas, nouvelle_figure=True, axes=None, axes_i=-1, axes_j=-1):
    """
    Entrée :
    - filename : le nom d'un fichier csv dont on veut extraire les données
    - pas : pas du temps pour le graphique de sortie
    - new_figure : booléen déterminant si on veut que le plot soit sur une nouvelle figure.
    - fig & axs : figure et axes sur lequel on veut mettre le nouveau plot
    - axs_i & axs_j : indice du subplot sur lequel on veut afficher le plot. (supposé valide)

    Sortie : Affichage d'un graphique du nombre de personnes non sortie en fonction du temps
    (La précision de la courbe dépend du pas considéré)
    (L'endroit où le graphe est affiché dépend des paramètres donnés).
    """
    ## Traitement des données ##

    nb_exp, derniers_sortie, temps_sortie = Extraire_Donnees(nom_fichier)

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
    # De plus il faut moyenner les valeurs obtenues car on veut qu'au maximum il y est  nb_personnes non sortie

    nb_non_sorties = [nb_personnes - item / nb_exp for item in nb_non_sorties]

    # Ajout de 20 valeurs dans nb_non_sorties et tab_pas
    # Ceci pour que les graphes ne finissent pas "brutalement"
    for i in range(1, 21):
        nb_non_sorties.append(nb_non_sorties[ind_nb_non_sorties])
        tab_pas.append(pas * (ind_nb_non_sorties + i))

    # Calcul du temps moyen de la dernière sortie
    moyenne_derniere_sortie = sum(derniers_sortie) / nb_exp

    # Calcul du dernier temps de sortie observée
    max_derniere_sortie = max(derniers_sortie)

    if nouvelle_figure:
        ## Affichage des Graphes ##
        plt.figure()
        plt.plot(tab_pas, nb_non_sorties)  # Graphe principal (celui voulu)

        # Ajout sur le graphe de la moyenne de la dernière sortie et du dernier temps de sortie
        plt.axvline(moyenne_derniere_sortie, c='r', ls='--',
                    label='Temps dernière sortie en moyenne : {:.2f}'.format(moyenne_derniere_sortie))
        plt.axvline(max_derniere_sortie, c='g', ls='--',
                    label='Temps dernière sortie : {:.2f}'.format(max_derniere_sortie))

        plt.title("Nombre de personnes non sortie en fonction du temps pour le batiment : \n" + nom_fichier)

        # Noms des axes
        axes = plt.gca()
        axes.set_ylabel("Nombre de personnes non sortie")
        axes.set_xlabel("t (s)")

        plt.legend()
        plt.grid()

    else:
        ## Affichage des Graphes ##
        axes[axes_i, axes_j].plot(tab_pas, nb_non_sorties)  # Graphe principal (celui voulu)

        # Ajout sur le graphe de la moyenne de la dernière sortie et du dernier temps de sortie
        axes[axes_i, axes_j].axvline(moyenne_derniere_sortie, c='r', ls='--',
                                     label='Temps dernière sortie en moyenne : {:.2f}'.format(moyenne_derniere_sortie))
        axes[axes_i, axes_j].axvline(max_derniere_sortie, c='g', ls='--',
                                     label='Temps dernière sortie : {:.2f}'.format(max_derniere_sortie))

        axes[axes_i, axes_j].set_title(
            "Nombre de personnes non sortie en fonction du temps pour le batiment : \n" + nom_fichier)

        # Noms des axes
        axes[axes_i, axes_j].set_ylabel("Nombre de personnes non sortie")
        axes[axes_i, axes_j].set_xlabel("t (s)")

        axes[axes_i, axes_j].legend()
        axes[axes_i, axes_j].grid()


def histogramme_dernier_temps(nom_fichier, nouvelle_figure=True, axes=None, axes_i=-1, axes_j=-1):
    """
    Entrée :
    - filename : le nom d'un fichier csv dont on veut extraire les données
    - new_figure : booléen déterminant si on veut que le plot soit sur une nouvelle figure.
    - fig & axs : figure et axes sur lequel on veut mettre le nouveau plot
    - axs_i & axs_j : indice du subplot sur lequel on veut afficher le plot. (supposé valide)

    Sortie : Affichage d'un histogramme des derniers temps de sortie en fonction du n° de la simulation
    """
    ## Traitement des données ##

    _, derniers_sortie, _ = Extraire_Donnees(nom_fichier)

    ## Affichage des graphes ##
    if nouvelle_figure:
        plt.figure()

        plt.bar([i for i in range(0, len(derniers_sortie))], derniers_sortie)

        plt.title(
            "Temps de la dernière sortie pour le bâtiment en fonction de la simulation considérée : \n" + nom_fichier)
        # Noms des axes
        axes = plt.gca()
        axes.set_ylabel("Dernier temps de sortie")
        axes.set_xlabel("n° simulation")

        # plt.legend()  # Ici pas besoin d'utiliser plt.legend() car il n'y a aucune legende à afficher.
        plt.grid()

    else:

        axes[axes_i, axes_j].bar([i for i in range(0, len(derniers_sortie))], derniers_sortie)

        axes[axes_i, axes_j].set_title("Temps de la dernière sortie pour le bâtiment en fonction de la simulation "
                                       "considérée : \n" + nom_fichier)

        # Noms des axes
        axes[axes_i, axes_j].set_ylabel("Dernier temps de sortie")
        axes[axes_i, axes_j].set_xlabel("n° simulation")

        # plt.legend()  # Ici pas besoin d'utiliser plt.legend() car il n'y a aucune legende à afficher.
        axes[axes_i, axes_j].grid()


def compare_moyenne_dernier_sortie(nom_fichier, nouvelle_figure=True, axes=None, axes_i=-1, axes_j=-1):
    """
    Entrée :
    - filenames: un tableau avec les noms des fichiers csv associées aux buildings à comparer
    - new_figure : booléen déterminant si on veut que le plot soit sur une nouvelle figure.
    - fig & axs : figure et axes sur lequel on veut mettre le nouveau plot
    - axs_i & axs_j : indice du subplot sur lequel on veut afficher le plot. (supposé valide)

    Sortie : Un graphe comparant la moyenne des derniers temps de sortie pour les bâtiment données en entrée.
    """
    ## Traitement des données ##
    dernieres_sorties = []

    for i in range(0, len(nom_fichier)):
        nb_experience, ligne, _ = Extraire_Donnees(nom_fichier[i])
        dernieres_sorties.append(sum(ligne) / nb_experience)

    print(dernieres_sorties)

    ## Affichage des graphes ##
    if nouvelle_figure:
        plt.figure()

        plt.bar([i for i in range(1, len(dernieres_sorties) + 1)], dernieres_sorties)

        plt.title(
            "Comparaison des temps moyens de dernière sortie en fonction des bâtiments")
        # Noms des axes
        axes = plt.gca()
        axes.set_ylabel("Temps moyen de dernière sortie")
        axes.set_xlabel("N° du bâtiment")

        # Affichage d'une ligne horizontale corresponant au temps minimale
        axes.axhline(min(dernieres_sorties), c='r', ls='--',
                     label='Minimum: {:.2f} s -> Batiment n°{}'.format(
                         min(dernieres_sorties),
                         dernieres_sorties.index(
                             min(dernieres_sorties)) + 1))

        # Permet d'avoir que des entiers en abcisse
        axes.xaxis.get_major_locator().set_params(integer=True)
        plt.legend()
        plt.grid()

    else:
        axes[axes_i, axes_j].bar([i for i in range(1, len(dernieres_sorties) + 1)], dernieres_sorties)

        axes[axes_i, axes_j].set_title(
            "Comparaison des temps moyens de dernière sortie en fonction des bâtiments")

        # Noms des axes
        axes[axes_i, axes_j].set_ylabel("Temps moyen de dernière sortie")
        axes[axes_i, axes_j].set_xlabel("N° du bâtiment")

        # Affichage d'une ligne horizontale corresponant au temps minimale
        axes[axes_i, axes_j].axhline(min(dernieres_sorties), c='r', ls='--',
                                     label='Minimum: {:.2f} s -> Batiment n°{}'.format(
                                         min(dernieres_sorties),
                                         dernieres_sorties.index(
                                             min(dernieres_sorties)) + 1))

        # Permet d'avoir que des entiers en abcisse
        axes[axes_i, axes_j].xaxis.get_major_locator().set_params(integer=True)
        axes[axes_i, axes_j].legend()
        axes[axes_i, axes_j].grid()


def compare_max_dernier_sortie(nom_fichier, nouvelle_figure=True, axes=None, axes_i=-1, axes_j=-1):
    """
    Entrée :
    - filenames: un tableau avec les noms des fichiers csv associées aux buildings à comparer
    - new_figure : booléen déterminant si on veut que le plot soit sur une nouvelle figure.
    - fig & axs : figure et axes sur lequel on veut mettre le nouveau plot
    - axs_i & axs_j : indice du subplot sur lequel on veut afficher le plot. (supposé valide)

    Sortie : Un graphe comparant le maximum des derniers temps de sortie pour les bâtiment données en entrée.
    """
    ## Traitement des données ##
    max_sorties = []

    for i in range(0, len(nom_fichier)):
        nb_experience, ligne, _ = Extraire_Donnees(nom_fichier[i])
        max_sorties.append(max(ligne))

    print(max_sorties)

    ## Affichage des graphes ##
    if nouvelle_figure:
        plt.figure()

        plt.bar([i for i in range(1, len(max_sorties) + 1)], max_sorties)

        plt.title(
            "Comparaison des temps maximales de dernière sortie en fonction des bâtiments")
        # Noms des axes
        axes = plt.gca()
        axes.set_ylabel("Temps maximale de dernière sortie")
        axes.set_xlabel("N° du bâtiment")

        # Affichage d'une ligne horizontale corresponant au temps minimale
        axes.axhline(min(max_sorties), c='r', ls='--',
                     label='Minimum: {:.2f} s -> Batiment n°{}'.format(
                         min(max_sorties),
                         max_sorties.index(
                             min(max_sorties)) + 1))

        # Permet d'avoir que des entiers en abcisse
        axes.xaxis.get_major_locator().set_params(integer=True)
        plt.legend()
        plt.grid()

    else:
        axes[axes_i, axes_j].bar([i for i in range(1, len(max_sorties) + 1)], max_sorties)

        axes[axes_i, axes_j].set_title(
            "Comparaison des temps maximales de dernière sortie en fonction des bâtiments")

        # Noms des axes
        axes[axes_i, axes_j].set_ylabel("Temps maximale de de dernière sortie")
        axes[axes_i, axes_j].set_xlabel("N° du bâtiment")

        # Affichage d'une ligne horizontale corresponant au temps minimale
        axes[axes_i, axes_j].axhline(min(max_sorties), c='r', ls='--',
                                     label='Minimum: {:.2f} s -> Batiment n°{}'.format(
                                         min(max_sorties),
                                         max_sorties.index(
                                             min(max_sorties)) + 1))

        # Permet d'avoir que des entiers en abcisse
        axes[axes_i, axes_j].xaxis.get_major_locator().set_params(integer=True)
        axes[axes_i, axes_j].legend()
        axes[axes_i, axes_j].grid()


def compare_min_dernier_sortie(nom_fichier, nouvelle_figure=True, axes=None, axes_i=-1, axes_j=-1):
    """
    Entrée :
    - filenames: un tableau avec les noms des fichiers csv associées aux buildings à comparer
    - new_figure : booléen déterminant si on veut que le plot soit sur une nouvelle figure.
    - fig & axs : figure et axes sur lequel on veut mettre le nouveau plot
    - axs_i & axs_j : indice du subplot sur lequel on veut afficher le plot. (supposé valide)

    Sortie : Un graphe comparant le minimum des derniers temps de sortie pour les bâtiment données en entrée.
    """
    ## Traitement des données ##
    min_sorties = []

    for i in range(0, len(nom_fichier)):
        nb_experience, ligne, _ = Extraire_Donnees(nom_fichier[i])
        min_sorties.append(min(ligne))

    print(min_sorties)

    ## Affichage des graphes ##
    if nouvelle_figure:
        plt.figure()

        plt.bar([i for i in range(1, len(min_sorties) + 1)], min_sorties)

        plt.title(
            "Comparaison des temps minimales de dernière sortie en fonction des bâtiments")
        # Noms des axes
        axes = plt.gca()
        axes.set_ylabel("Temps minimale de dernière sortie")
        axes.set_xlabel("N° du bâtiment")

        # Affichage d'une ligne horizontale corresponant au temps minimale
        axes.axhline(min(min_sorties), c='r', ls='--',
                     label='Minimum: {:.2f} s -> Batiment n°{}'.format(
                         min(min_sorties),
                         min_sorties.index(
                             min(min_sorties)) + 1))

        # Permet d'avoir que des entiers en abcisse
        axes.xaxis.get_major_locator().set_params(integer=True)
        plt.legend()
        plt.grid()

    else:
        axes[axes_i, axes_j].bar([i for i in range(1, len(min_sorties) + 1)], min_sorties)

        axes[axes_i, axes_j].set_title(
            "Comparaison des temps minimales de dernière sortie en fonction des bâtiments")

        # Noms des axes
        axes[axes_i, axes_j].set_ylabel("Temps minimales de de dernière sortie")
        axes[axes_i, axes_j].set_xlabel("N° du bâtiment")

        # Affichage d'une ligne horizontale corresponant au temps minimale
        axes[axes_i, axes_j].axhline(min(min_sorties), c='r', ls='--',
                                     label='Minimum: {:.2f} s -> Batiment n°{}'.format(
                                         min(min_sorties),
                                         min_sorties.index(
                                             min(min_sorties)) + 1))

        # Permet d'avoir que des entiers en abcisse
        axes[axes_i, axes_j].xaxis.get_major_locator().set_params(integer=True)
        axes[axes_i, axes_j].legend()
        axes[axes_i, axes_j].grid()


def comparaison_solution_Move():
    """Comparaison des Solutions 1, 2, 3 pour la fonction Move"""

    ## Affichage de la figure 1 ##
    figure, axes = plt.subplots(2, 2)
    nb_survivant_temps('2 door + 250 tables uniform with Solution 1.csv', 0.1, False, axes, 0, 0)
    nb_survivant_temps('2 door + 250 tables uniform with Solution 2.csv', 0.1, False, axes, 0, 1)
    nb_survivant_temps('2 door + 250 tables uniform with Solution 3.csv', 0.1, False, axes, 1, 0)

    # Ajuste le placement des plot et affichage
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
    plt.show(block=False)

    ## Affichage de la figure 2 ##
    figure, axes = plt.subplots(2, 2)
    histogramme_dernier_temps('2 door + 250 tables uniform with Solution 1.csv', False, axes, 0, 0)
    histogramme_dernier_temps('2 door + 250 tables uniform with Solution 2.csv', False, axes, 0, 1)
    histogramme_dernier_temps('2 door + 250 tables uniform with Solution 3.csv', False, axes, 1, 0)

    # Ajuste le placement des plot et affichage
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
    plt.show(block=False)

    ## Affiche tous les plot ##
    plt.show()


def comparaison_10_premier_bat():
    noms_fichier = ['1. couloir 1m.csv',
                    '2. couloir 1m50.csv',
                    '3. couloir libre.csv',
                    '4. 5 Personnes max par bureau.csv',
                    '5. 10 Personnes max par bureau.csv',
                    '6. 20 Personnes max par bureau.csv',
                    '7. 30 Personnes max par bureau.csv',
                    '8. 1 Porte par bureau.csv',
                    '9. 2 Porte par bureau.csv',
                    '10. 3 Porte par bureau.csv',
                    '11. 4 Porte par bureau.csv'
                    ]

    ## Affichage de la figure 1 ##
    fig, axs = plt.subplots(2, 2)
    compare_moyenne_dernier_sortie(noms_fichier, False, axs, 0, 0)
    compare_max_dernier_sortie(noms_fichier, False, axs, 0, 1)
    compare_min_dernier_sortie(noms_fichier, False, axs, 1, 0)

    # Ajuste le placement des plot et affichage
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
    plt.show()


def comparaison(noms_fichier):
    ## Affichage de la figure 1 ##
    figure, axes = plt.subplots(2, 2)
    compare_moyenne_dernier_sortie(noms_fichier, False, axes, 0, 0)
    compare_max_dernier_sortie(noms_fichier, False, axes, 0, 1)
    compare_min_dernier_sortie(noms_fichier, False, axes, 1, 0)

    # Ajuste le placement des plot et affichage
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
    plt.show()


def nombre_personne_sauve(nom_fichier, temps_fin, pas=0.01):
    """
    Entrée :
    - filename : le nom d'un fichier csv dont on veut extraire les données
    - pas : pas du temps pour le graphique de sortie

    Sortie :  - Affichage d'un graphique du nombre de personnes non sorties en moyenne en fonction du temps avec une barre
    au temps valant temps_fin (pour voir le nombre de personnes mortes ou sauvés après ce temps)
              - Affichage dans le shell du nombre de personnes pas sortie avec le temps : temps_fin
    (La précision de la courbe dépend du pas considéré)

    """
    ## Traitement des données ##

    nb_exp, derniers_sortie, temps_sortie = Extraire_Donnees(nom_fichier)

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

            tab_pas.append(round(pas * ind_nb_non_sorties, len(str(pas))))

    # A ce moment nb_non_sorties comptient pour chaque pas le nombres de personnes sortie
    # Il faut donc "inverser la signification de ce tableau" car on veut le nombre de personne non sortie
    # De plus il faut moyenner les valeurs obtenues car on veut qu'au maximum il y est  nb_personnes non sortie

    nb_non_sorties = [nb_personnes - item / nb_exp for item in nb_non_sorties]

    # Ajout de 20 valeurs dans nb_non_sorties et tab_pas
    # Ceci pour que les graphes ne finissent pas "brutalement"
    for i in range(1, 21):
        nb_non_sorties.append(nb_non_sorties[ind_nb_non_sorties])
        tab_pas.append(pas * (ind_nb_non_sorties + i))

    # Calcul du temps moyen de la dernière sortie
    moyenne_derniere_sortie = sum(derniers_sortie) / nb_exp

    # Calcul du dernier temps de sortie observée
    max_derniere_sortie = max(derniers_sortie)

    ## Valeur du nombre de personnes non sorties avec temps_fin ##
    temps_fin = round(temps_fin, len(str(pas)))  # On arrondi la valeur en fonction du temps pour être sur qu'il est présent dans tab_pas
    indice_temps_fin = tab_pas.index(temps_fin)  # On récupère l'indice du temps associé à temps fin

    nb_non_sauve = round(nb_non_sorties[indice_temps_fin], 2)

    print("Nombre de personnes non sauvés (en moyenne) avant temps_fin : ", nb_non_sauve, "personnes")
    print("Nombre de personnes non sauvés (en pourcentage) avant temps_fin", (nb_non_sauve / nb_personnes)*100, "%")

    ## Affichage des Graphes ##
    plt.figure()
    plt.plot(tab_pas, nb_non_sorties)  # Graphe principal (celui voulu)

    # Ajout sur le graphe de la moyenne de la dernière sortie et du dernier temps de sortie
    plt.axvline(temps_fin, c='r', ls='--',
                label='Temps de fin : {:.2f}'.format(temps_fin))
    plt.axhline(nb_non_sauve, c='r', ls='--',
                label='Nb personnes non sauvés : {:.2f}'.format(nb_non_sauve))

    plt.title("Nombre de personnes non sortie en fonction du temps pour le batiment : \n" + nom_fichier)

    # Noms des axes
    axes = plt.gca()
    axes.set_ylabel("Nombre de personnes non sortie")
    axes.set_xlabel("t (s)")

    plt.legend()
    plt.grid()
    plt.show()


#nombre_personne_sauve('Batiment Initial.csv', 22.22)

def main():
    noms_fichier = ['Batiment Initial.csv',
                    'Batiment Hypothèse 3..csv',
                    'Batiment Hypothèse 5..csv',
                    'Batiment Hypothèse 6..csv',
                    'Batiment Hypothèse 1..csv',
                    'Batiment 4.1.csv',
                    'Batiment 4.2.csv',
                    ]

    comparaison(noms_fichier)
    plt.show()

main()