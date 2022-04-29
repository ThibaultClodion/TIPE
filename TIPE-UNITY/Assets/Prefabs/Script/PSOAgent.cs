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

    private bool InObstacleCollider = false;

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

        if(InObstacleCollider == true)
        {
            //It is necessary to make the avoidment "smartly"
            //Here it's brainless, agent just going up
            vitesse = vitesse + new Vector2(0f, 15f);
        }

        //Limit the maximum speed
        if (vitesse.sqrMagnitude > squareMaxSpeed)
        {
            vitesse = vitesse.normalized * MaxSpeed;
        }

        transform.up = vitesse;
        transform.position += (Vector3)vitesse * Time.deltaTime;

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

        if (collision.gameObject.tag == "Obstacle")
        {
            InObstacleCollider = true;
        }
    }
    private void OnTriggerExit2D(Collider2D collision)
    {
   

        InObstacleCollider = false;

        //Use the position to run to the "nearest coin of the box of the exit" 
        Vector2 size = collision.offset;
        Vector3 centerPoint = new Vector3(collision.offset.x, collision.offset.y, 0f);
        Vector3 worldPos = transform.TransformPoint(collision.offset);

        float top = worldPos.y + (size.y / 2f);
        float btm = worldPos.y - (size.y / 2f);
        float left = worldPos.x - (size.x / 2f);
        float right = worldPos.x + (size.x / 2f);

        Vector3 topLeft = new Vector3(left, top, worldPos.z);
        Vector3 topRight = new Vector3(right, top, worldPos.z);
        Vector3 btmLeft = new Vector3(left, btm, worldPos.z);
        Vector3 btmRight = new Vector3(right, btm, worldPos.z);
    }

}
