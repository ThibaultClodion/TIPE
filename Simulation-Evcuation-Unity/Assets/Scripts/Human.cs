using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class Human : MonoBehaviour
{

    private GameManager GMScript;

    private NavMeshAgent navMeshAgent;

    public Transform ExitZoneWantedPosition;
    private void Awake()
    {
        navMeshAgent = GetComponent<NavMeshAgent>();

        GMScript = GameObject.Find("GameManager").GetComponent<GameManager>(); // In the Awake to avoid a problem of reference (believe me let it here)
    }

    // Start is called before the first frame update
    void Start()
    {
        NavMesh.avoidancePredictionTime = 0.5f;
    }

    public void Move(Transform pos)
    {
        //Le détail sur les avantages et incovénient des solutions est dans mes notes.

        /*/ Solution 1 : Des gens se bloquent ou sont lent, finalement avec les modifications faites ça à l'air pas mal
        // Si il y a une ou deux valeurs a ecarter c'est pas grave
        NavMeshPath path = new NavMeshPath();
        navMeshAgent.CalculatePath(pos.position, path);
        navMeshAgent.SetPath(path);*/

        // Solution 2 : le calcul est parfois très long et plus le batiment est complexe plus il le serra surement
        //navMeshAgent.SetDestination(pos.position);

        // Solution 3 
         
        NavMeshPath path = new NavMeshPath();
        navMeshAgent.CalculatePath(pos.position, path);
        navMeshAgent.SetPath(path);
        

        navMeshAgent.SetDestination(pos.position);
        
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "ExitZone")
        {
            //Change the public variable, to add a people save
            GMScript.HowManyPeopleSave++;

            //Get the time when the people exit (to make stats)
            GMScript.exit_times.Add(GMScript.timer);

            //Destroy the object if it goes to the exit zone
            Destroy(gameObject);
        }
    }
}