using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using System.IO;

public class GameManager : MonoBehaviour
{

    //D�finit le nombre de personnes qui appara�t au d�but de la simulation
    [Range(1f, 500f)]
    public int NombreHumainsTotal;

    //Bool�en permettant de savoir si les personnes apparaissent al�atoirement ou non
    public bool ApparaitAleatoirement;

    //Bool�en permettant de savoir si on veut enregistrer les donn�es ou non
    public bool sauvegarderDonnees;

    //Variable pour conna�tre le nombre d'humains sauv�s
    public int NombreHumainsSauve = 0;

    //Variable pour connaitre le temps � tout moment de la simulation
    public float temps = 0;
    public float temps_max;

    //Variable permettant de ne pas avoir de collision au lancement de la simulation
    public float RayonDeNonCollision;

    //Variables li�s au texte affich� � l'�cran
    public TextMeshProUGUI NombrePersonneSauveTexte;
    public TextMeshProUGUI TempsTexte;


    //Liste des temps de sortie pour la r�cup�ration de donn�es
    public List<float> temps_sorties = new List<float>();

    //Liste des humains et Prefab les d�finissant
    public List<Human> humains_non_aleatoire = new List<Human>();
    private List<Human> humains = new List<Human>();
    public Human HumainPrefab;

    //Liste des destination choisit par les humains (m�me indice que ceux de la liste "humains")
    private List<Transform> humains_destination = new List<Transform>();

    //Positions des sorties
    public List<Transform> positions_sortie;

    private void Start()
    {
        ApparitionHumain(NombreHumainsTotal, ApparaitAleatoirement); //Fait appara�tre les humains
    }

    // Update is called once per frame
    void Update()
    {
        //Mise � jour du temps
        temps += Time.deltaTime;
        TempsTexte.text = "t: " + temps.ToString("n2") + "s";

        //Mise � jour du texte du nombre de personnes sauv�
        NombrePersonneSauveTexte.text = "N: " + NombreHumainsSauve.ToString() + "/" + NombreHumainsTotal.ToString();

        //Tout le monde � �vacu�, la simulation recommence normalement
        if (NombreHumainsTotal == NombreHumainsSauve && sauvegarderDonnees == true)
        {
            Reapparition(true);
        }
        else if( NombreHumainsTotal == NombreHumainsSauve && sauvegarderDonnees == false)
        {
            Reapparition(false);
        }

        //Si la simulation met trop de temps (il y a un disfonctionnement), elle se relance alors.
        if(temps > temps_max)
        {
            Reapparition(false);
        }

        //Permet de prendre des captures d'images en appuyant sur "P"
        if (Input.GetKeyDown(KeyCode.P))
        {
            CaptureDEcran();
        }

    }

    private void Reapparition(bool SauvergarderResultat)
    {
        NombreHumainsSauve = 0; //Reset du nombre de personnes sauv�

        if (SauvergarderResultat == true)
        {
            SauvegardeCSV(); //Sauvergarde du CSV
        }
        if(SauvergarderResultat == false)
        {
            DestructionHumains(); //Destruction des humains restants (car si on ne sauvegarde pas les donn�es c'est qu'il y a eu un probl�me)
        }

        humains = new List<Human>(); //Reset de la liste des humains
        humains_destination = new List<Transform>(); //Reset de la liste des destinations choisit par les humains
        temps_sorties = new List<float>(); //Reset la liste des temps de sortie


        ApparitionHumain(NombreHumainsTotal, ApparaitAleatoirement); // Fait appara�tre les humains

        temps = 0; //Reset le temps � 0
    }

    //Cr�er le nombre d'humains voulus
    void ApparitionHumain(int nombreHumains, bool apparaitAleatoirement)
    {
        if(apparaitAleatoirement)
        {
            for (int i = 0; i < nombreHumains; i++)
            {
                //D�finit o� l'humain appara�t
                Vector3 Position_Hum = new Vector3(Random.Range(0f, 70f), 0.85f, Random.Range(-35f, 0f));

                // Permet d'�viter les collisions � l'apparition
                // Le "3" dans la fonction repr�sente le Layer non consid�r� par CheckSphere (ici il s'agit du sol, car on veut que les humais appara�ssent sur le sol)
                while (Physics.CheckSphere(Position_Hum, RayonDeNonCollision, 3))
                {
                    //On attribue une nouvelle position al�atoire � l'agent.
                    Position_Hum = new Vector3(Random.Range(0f, 70f), 0.85f, Random.Range(-35f, 0f));
                }

                Human Humain = Instantiate(HumainPrefab, Position_Hum, Quaternion.Euler(Vector3.forward * Random.Range(0f, 360f)), transform);

                Humain.name = "Agent" + i;

                Transform MeilleureDestination = PositionSortiePlusProche(Position_Hum); // Permet de conna�tre la position de la sortie la plus proche.
                Humain.Deplacer(MeilleureDestination);

                humains_destination.Add(MeilleureDestination);
                humains.Add(Humain);
            }
        }
        else
        {
            for(int i = 0; i < nombreHumains; i++)
            {
                Vector3 Position_Hum = humains_non_aleatoire[i].transform.position;

                Human Humain = Instantiate(HumainPrefab, Position_Hum, Quaternion.Euler(Vector3.forward * Random.Range(0f, 360f)), transform);

                Humain.name = "Agent" + i;

                Transform MeilleureDestination = PositionSortiePlusProche(Position_Hum); // Permet de conna�tre la position de la sortie la plus proche.
                Humain.Deplacer(MeilleureDestination);

                humains_destination.Add(MeilleureDestination);
                humains.Add(Humain);
            }
        }
    }

    // Renvoie la position de la sortie la plus proche de la position "PositionDepart"
    Transform PositionSortiePlusProche(Vector3 PositionDepart)
    {
        Transform PositionProche = null;
        float Distance_minimale = Mathf.Infinity;

        foreach (Transform Sorties in positions_sortie)
        {
            Vector3 direction = Sorties.position - PositionDepart;
            float DistanceActuel = direction.sqrMagnitude;

            if (DistanceActuel < Distance_minimale)
            {
                Distance_minimale = DistanceActuel;
                PositionProche = Sorties;
            }
        }
        return PositionProche;
    }
    

    void SauvegardeCSV()
    {
        //Chemin du fichier
        string chemin = "C:/Users/darkz/Desktop/TIPE/Data/" + GameObject.FindGameObjectWithTag("Building").name + ".csv";

        //Cr�ation du fichier si il n'existe pas
        if (!File.Exists(chemin))
        {
            for (int i = 0; i < NombreHumainsTotal; i++)
            {
                File.AppendAllText(chemin, "Personne " + i.ToString() + ";");
            }
            File.AppendAllText(chemin, "\n");
        }

        foreach (float temps in temps_sorties)
        {
            File.AppendAllText(chemin, temps.ToString() + ";");
        }

        File.AppendAllText(chemin, "\n");
    }

    //Effectue une capture d'�cran � la date et l'heure actuelle
    public void CaptureDEcran()
        {
        string Date = System.DateTime.Now.ToString("dd-MMMM-yyyy HHmmss");

        ScreenCapture.CaptureScreenshot("C:/Users/darkz/Desktop/TIPE/Document pour pr�sentation etc/Screenshot - Unity/" + GameObject.FindGameObjectWithTag("Building").name + "  " + Date + ".png");
        }

    //D�truit tous les GameObject dont le Tag est "Human"
    void DestructionHumains()
    {
        GameObject[] gameObjects = GameObject.FindGameObjectsWithTag("Human");

        for (var i = 0; i < gameObjects.Length; i++)
        {
            Destroy(gameObjects[i]);
        }
    }
}