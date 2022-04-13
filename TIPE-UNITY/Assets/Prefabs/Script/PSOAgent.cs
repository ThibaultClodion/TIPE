using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PSOAgent : MonoBehaviour
{

    private GameManager gameManagerScript;

    private Vector2 minLocal; //Min position of this agent

    private void Awake()
    {
        gameManagerScript = GameObject.Find("GameManager").GetComponent<GameManager>(); // In the Awake to avoid a problem of reference (believe me let it here)
    }

    // Start is called before the first frame update
    void Start()
    {
        Vector2 minLocal = (Vector2)transform.position;
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void Move()
    {
        Vector2 minLocal = (Vector2)transform.position; // For now we don't consider the minlocal

        Vector2 vitesse = Random.Range(0.0f, 1.0f) * (minLocal - (Vector2)transform.position) + Random.Range(0f, 1f) * (gameManagerScript.minGlobal - (Vector2)transform.position);
        transform.up = vitesse;
        transform.position += (Vector3)vitesse * Time.deltaTime;

        //Il faut ensuite tester si l'agent atteint un min personel ou global (juste l'idée du code est là il manque la fonction à la place de magnitude)
        /*if(minLocal.magnitude < ((Vector2)transform.position).magnitude)
        {
            minLocal = (Vector2)transform.position;
             if(minLocal.magnitude > (gameManagerScript.minGlobal.magnitude))
                {
                    gameManagerScript.minGlobal = minLocal;
                }
        }*/
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.name == "ExitZone")
        {
            //Change the public variable, to add a people save
            gameManagerScript.HowManyPeopleSave++;

            //Get the time when the people exit (to make stats)
            gameManagerScript.exit_times.Add(gameManagerScript.timer);

            //Destroy the object if it goes to the exit zone
            Destroy(gameObject);
        }
    }

}
