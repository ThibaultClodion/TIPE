using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class Human : MonoBehaviour
{

    private GameManager GMScript;
    public Transform movePositionTransform;

    private NavMeshAgent navMeshAgent;
    private void Awake()
    {
        navMeshAgent = GetComponent<NavMeshAgent>();

        GMScript = GameObject.Find("GameManager").GetComponent<GameManager>(); // In the Awake to avoid a problem of reference (believe me let it here)
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    public void Move()
    {
        navMeshAgent.destination = movePositionTransform.position;
    }

    private void OnTriggerEnter(Collider other)
    {
        Debug.Log("Work");
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
