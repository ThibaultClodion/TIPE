using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using System.IO;

public class GameManager : MonoBehaviour
{

    //Définit le nombre de personnes qui apparaît au début de la simulation
    [Range(1f, 500f)]
    public int NombreHumainsTotal;

    //Booléen permettant de savoir si les personnes apparaissent aléatoirement ou non
    public bool ApparaitAleatoirement;

    //Booléen permettant de savoir si on veut enregistrer les données ou non
    public bool sauvegarderDonnees;

    //Variable pour connaître le nombre d'humains sauvés
    public int NombreHumainsSauve = 0;

    //Variable pour connaitre le temps à tout moment de la simulation
    public float temps = 0;
    public float temps_max;

    //Variable permettant de ne pas avoir de collision au lancement de la simulation
    public float RayonDeNonCollision;

    //Variables liés au texte affiché à l'écran
    public TextMeshProUGUI NombrePersonneSauveTexte;
    public TextMeshProUGUI TempsTexte;


    //Liste des temps de sortie pour la récupération de données
    public List<float> temps_sorties = new List<float>();

    //Liste des humains et Prefab les définissant
    public List<Human> humains_non_aleatoire = new List<Human>();
    private List<Human> humains = new List<Human>();
    public Human HumainPrefab;

    //Liste des destination choisit par les humains (même indice que ceux de la liste "humains")
    private List<Transform> humains_destination = new List<Transform>();

    //Positions des sorties
    public List<Transform> positions_sortie;

    private void Start()
    {
        ApparitionHumain(NombreHumainsTotal, ApparaitAleatoirement); //Fait apparaître les humains
    }

    // Update is called once per frame
    void Update()
    {
        //Mise à jour du temps
        temps += Time.deltaTime;
        TempsTexte.text = "t: " + temps.ToString("n2") + "s";

        //Mise à jour du texte du nombre de personnes sauvé
        NombrePersonneSauveTexte.text = "N: " + NombreHumainsSauve.ToString() + "/" + NombreHumainsTotal.ToString();

        //Tout le monde à évacué, la simulation recommence normalement
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
        NombreHumainsSauve = 0; //Reset du nombre de personnes sauvé

        if (SauvergarderResultat == true)
        {
            SauvegardeCSV(); //Sauvergarde du CSV
        }
        if(SauvergarderResultat == false)
        {
            DestructionHumains(); //Destruction des humains restants (car si on ne sauvegarde pas les données c'est qu'il y a eu un problème)
        }

        humains = new List<Human>(); //Reset de la liste des humains
        humains_destination = new List<Transform>(); //Reset de la liste des destinations choisit par les humains
        temps_sorties = new List<float>(); //Reset la liste des temps de sortie


        ApparitionHumain(NombreHumainsTotal, ApparaitAleatoirement); // Fait apparaître les humains

        temps = 0; //Reset le temps à 0
    }

    //Créer le nombre d'humains voulus
    void ApparitionHumain(int nombreHumains, bool apparaitAleatoirement)
    {
        if(apparaitAleatoirement)
        {
            for (int i = 0; i < nombreHumains; i++)
            {
                //Définit où l'humain apparaît
                Vector3 Position_Hum = new Vector3(Random.Range(0f, 70f), 0.85f, Random.Range(-35f, 0f));

                // Permet d'éviter les collisions à l'apparition
                // Le "3" dans la fonction représente le Layer non considéré par CheckSphere (ici il s'agit du sol, car on veut que les humais apparaîssent sur le sol)
                while (Physics.CheckSphere(Position_Hum, RayonDeNonCollision, 3))
                {
                    //On attribue une nouvelle position aléatoire à l'agent.
                    Position_Hum = new Vector3(Random.Range(0f, 70f), 0.85f, Random.Range(-35f, 0f));
                }

                Human Humain = Instantiate(HumainPrefab, Position_Hum, Quaternion.Euler(Vector3.forward * Random.Range(0f, 360f)), transform);

                Humain.name = "Agent" + i;

                Transform MeilleureDestination = PositionSortiePlusProche(Position_Hum); // Permet de connaître la position de la sortie la plus proche.
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

                Transform MeilleureDestination = PositionSortiePlusProche(Position_Hum); // Permet de connaître la position de la sortie la plus proche.
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

        //Création du fichier si il n'existe pas
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

    //Effectue une capture d'écran à la date et l'heure actuelle
    public void CaptureDEcran()
        {
        string Date = System.DateTime.Now.ToString("dd-MMMM-yyyy HHmmss");

        ScreenCapture.CaptureScreenshot("C:/Users/darkz/Desktop/TIPE/Document pour présentation etc/Screenshot - Unity/" + GameObject.FindGameObjectWithTag("Building").name + "  " + Date + ".png");
        }

    //Détruit tous les GameObject dont le Tag est "Human"
    void DestructionHumains()
    {
        GameObject[] gameObjects = GameObject.FindGameObjectsWithTag("Human");

        for (var i = 0; i < gameObjects.Length; i++)
        {
            Destroy(gameObjects[i]);
        }
    }
}