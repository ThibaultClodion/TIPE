using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HumanControlByMe : MonoBehaviour
{

    private Rigidbody2D humanRb;

    private GameManager gameManagerScript;

    // Start is called before the first frame update
    void Start()
    {
        humanRb = GetComponent<Rigidbody2D>();

        gameManagerScript = GameObject.Find("GameManager").GetComponent<GameManager>();
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            humanRb.velocity = new Vector2(7f, 0f);
        }        
        else if (Input.GetKeyDown(KeyCode.LeftArrow))
        {
            humanRb.velocity = new Vector2(-7f, 0f);
        }        
        else if (Input.GetKeyDown(KeyCode.UpArrow))
        {
            humanRb.velocity = new Vector2(0f, 7f);
        }        
        else if (Input.GetKeyDown(KeyCode.DownArrow))
        {
            humanRb.velocity = new Vector2(0f, -7f);
        }
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.tag == "ExitZone")
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
