using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Collider2D))]
public class BoidAgent : MonoBehaviour
{

    Collider2D boidCollider;
    public Collider2D BoidCollider { get { return boidCollider; } }

    private GameManagerBoid gameManagerScript;

    // Start is called before the first frame update
    void Start()
    {
        boidCollider = GetComponent<Collider2D>();
        gameManagerScript = GameObject.Find("GameManager").GetComponent<GameManagerBoid>();
    }

    public void Move(Vector2 velocity)
    {
        transform.up = velocity;
        transform.position += (Vector3)velocity * Time.deltaTime;
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


