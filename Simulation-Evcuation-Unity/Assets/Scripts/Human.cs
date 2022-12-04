using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class Human : MonoBehaviour
{

    private GameManager GMScript;

    private NavMeshAgent navMeshAgent;

    private void Awake()
    {
        navMeshAgent = GetComponent<NavMeshAgent>();

        GMScript = GameObject.Find("GameManager").GetComponent<GameManager>();
    }

    // Start is called before the first frame update
    void Start()
    {
        NavMesh.avoidancePredictionTime = 0.5f;
    }

    public void Deplacer(Transform pos)
    {
        //Le d�tail sur les avantages et incov�nient des solutions est dans mes notes.

        /*/ Solution 1 : Des gens se bloquent ou sont lent, finalement avec les modifications faites �a � l'air pas mal
        // Si il y a une ou deux valeurs a ecarter c'est pas grave
        NavMeshPath path = new NavMeshPath();
        navMeshAgent.CalculatePath(pos.position, path);
        navMeshAgent.SetPath(path);*/

        // Solution 2 : le calcul est parfois tr�s long et plus le batiment est complexe plus il le serra surement
        //navMeshAgent.SetDestination(pos.position);

        // Solution 3 : optimal

        NavMeshPath path = new NavMeshPath();
        navMeshAgent.CalculatePath(pos.position, path);
        navMeshAgent.SetPath(path);


        navMeshAgent.SetDestination(pos.position);

    }

    private void OnTriggerEnter(Collider Autre)
    {
        //Si l'humain entre dans une zone de sortie
        if (Autre.tag == "ExitZone")
        {
            //L'humain consid�r� est sorti de la pi�ce.
            GMScript.NombreHumainsSauve++;

            //Ajout du temps de sortie de cet individu � la liste des temps de sortie.
            GMScript.temps_sorties.Add(GMScript.temps);

            //Destruction de l'objet pour ne pas surcharger la sc�ne.
            Destroy(gameObject);
        }
    }
}