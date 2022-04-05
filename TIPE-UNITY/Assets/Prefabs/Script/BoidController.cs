using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoidController : MonoBehaviour
{
    //Parameters of the boids
    public int SwarmIndex;
    public float NoClumpingRadius;
    public float LocalAreaRadius;
    public float Speed;
    public float SteeringSpeed;

    //define the GameObject of the exit Zone
    private GameObject exitZone;

    //define the GameObject and the script of the GameManager
    private GameObject gameManager;
    private GameManager gameManagerScript;
    // Start is called before the first frame update
    void Start()
    {
        //Find the exitZone and the gameManagerScript
        exitZone = GameObject.Find("ExitZone");
        gameManager = GameObject.Find("GameManager");
        gameManagerScript = gameManager.GetComponent<GameManager>();
    }

    // Update is called once per frame
    void Update()
    {

    }
    public void SimulateMovement(List<BoidController> other, float time)
    {
        //default vars
        var steering = Vector3.zero;

        //apply steering
        if (steering != Vector3.zero)
            transform.rotation = Quaternion.RotateTowards(transform.rotation, Quaternion.LookRotation(steering), SteeringSpeed * time);

        //move 
        transform.position += transform.TransformDirection(new Vector3(-Speed, 0, 0)) * time;
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.name == "ExitZone")
        {
            //Change the public variable, to add a people save
            gameManagerScript.HowManyPeopleSave++;

            //Get the time when the people exit (to make stats)
            gameManagerScript.exit_times.Add(gameManagerScript.timer);

            Debug.Log("test");

            //Destroy the object if it goes to the exit zone
            Destroy(gameObject);
        }
    }
}
