using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ReachExitZone : MonoBehaviour
{
    //define the GameObject of the exit Zone
    private GameObject exitZone;

    //define the GameObject and the script of the GameManager
    private GameObject gameManager;
    private GameManager gameManagerScript;

    public List<float> exit_times;

    // Start is called before the first frame update
    void Start()
    {
        //Define the variables to find beetween GameObject
        exitZone = GameObject.Find("ExitZone");
        gameManager = GameObject.Find("GameManager");
        gameManagerScript = gameManager.GetComponent<GameManager>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if(collision.gameObject.name == "ExitZone")
        {
            //Change the public variable, to add a people save
            gameManagerScript.HowManyPeopleSave ++;

            //Get the time when the people exit (to make stats)
            exit_times.Add(gameManagerScript.timer);

            Debug.Log("test");

            //Destroy the object if it goes to the exit zone
            Destroy(gameObject);
        }
    }
}
