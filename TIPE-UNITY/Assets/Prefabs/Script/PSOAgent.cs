using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PSOAgent : MonoBehaviour
{

    private GameManager GMScript;
    public float MaxSpeed;
    private float squareMaxSpeed;
    
    public float omega; //See the pseudo-Code of Quentin to understand

    private Vector2 minLocal; //Min position of this agent

    private void Awake()
    {
        GMScript = GameObject.Find("GameManager").GetComponent<GameManager>(); // In the Awake to avoid a problem of reference (believe me let it here)
    }

    // Start is called before the first frame update
    void Start()
    {
        squareMaxSpeed = MaxSpeed * MaxSpeed;
        Vector2 minLocal = (Vector2)transform.position;
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void Move()
    {
        Vector2 vitesse = omega * Random.Range(0.0f, 1.0f) * (minLocal - (Vector2)transform.position) + Random.Range(0f, 1f) * (GMScript.minGlobal[0] - (Vector2)transform.position);

        //Limit the maximum speed
        if (vitesse.sqrMagnitude > squareMaxSpeed)
        {
            vitesse = vitesse.normalized * MaxSpeed;
        }

        transform.up = vitesse;
        transform.position += (Vector3)vitesse * Time.deltaTime;

        //Il faut ensuite tester si l'agent atteint un min personel ou global (juste l'idée du code est là il manque la fonction à la place de magnitude)
        if(GMScript.batimentFunction(0, minLocal) > GMScript.batimentFunction(0, transform.position))
        {
            minLocal = (Vector2)transform.position;
        }
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.tag == "ExitZone")
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
