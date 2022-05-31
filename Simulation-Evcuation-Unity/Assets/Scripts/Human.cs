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
        //Solution 1 : Avantage: calcul plus rapide 
        NavMeshPath path = new NavMeshPath();
        navMeshAgent.CalculatePath(pos.position, path);
        navMeshAgent.SetPath(path);

        /* Solution 2 : Avantage: Les personnes ne se retrouvent pas bloqué quand on les poussent parfois
         * Pour celle là il faut prendr en compte le fait qu'il y a un temps de calcul non négligeable.
         */
        //navMeshAgent.SetDestination(pos.position);
        
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