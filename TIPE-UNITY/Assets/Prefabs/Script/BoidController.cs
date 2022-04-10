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
        var steering = Vector2.zero;


        //3 Rules for boids
        Vector2 separationDirection = Vector2.zero;
        int separationCount = 0;

        Vector2 alignmentDirection = Vector2.zero;
        int alignmentCount = 0;

        Vector2 cohesionDirection = Vector2.zero;
        int cohesionCount = 0;

        var leaderBoid = other[0];
        var leaderAngle = 180f;

        foreach (BoidController boid in other)
        {
            //skip self
            if (boid == this || boid == null)
                continue;

            var distance = Vector2.Distance(boid.transform.position, this.transform.position);

            //identify local neighbour
            if (distance < NoClumpingRadius)
            {
                separationDirection += (Vector2)boid.transform.position - (Vector2)transform.position;
                separationCount++;
            }
            if (distance < LocalAreaRadius)
            {
                alignmentDirection += (Vector2)boid.transform.forward;
                alignmentCount++;

                cohesionDirection += (Vector2)boid.transform.position - (Vector2)transform.position;
                cohesionCount++;

                //identify leader
                var angle = Vector3.Angle(boid.transform.position - transform.position, transform.forward);
                if(angle < leaderAngle && angle < 90f)
                {
                    leaderBoid = boid;
                    leaderAngle = angle;
                }
            }
        }

        //calculate average
        if (separationCount > 0)
        {
            separationDirection /= separationCount;
        }
        if (cohesionCount > 0)
        {
            cohesionDirection /= cohesionCount;
        }
        if(alignmentCount > 0)
        {
            alignmentDirection /= alignmentCount;
        }


        //flip
        separationDirection = -separationDirection;
 
        //apply to steering and weigthed rules
        steering += separationDirection.normalized;
        steering += alignmentDirection.normalized;
        steering += cohesionDirection.normalized;

        //local leader, I comment it, because it was not better i thought
        /*if (leaderBoid != null)
            steering += (Vector2)(leaderBoid.transform.position - transform.position).normalized;*/

        //apply steering
        if (steering != Vector2.zero) {
        transform.rotation = Quaternion.RotateTowards(transform.rotation, Quaternion.LookRotation(steering), SteeringSpeed * time);
        transform.rotation = new Quaternion(0, 0, transform.rotation.z, transform.rotation.w);
        }

        //move
        transform.position += transform.TransformDirection(new Vector2(-Speed, 0)) * time;

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
