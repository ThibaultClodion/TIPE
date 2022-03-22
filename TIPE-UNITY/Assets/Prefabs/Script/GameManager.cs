using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class GameManager : MonoBehaviour
{
    //Define the GameObject use for Human
    public GameObject Human;

    //Define the GameObject use for the Fire
    public GameObject Fire;

    //Define How many humans spawn at the start of simulation
    public int HowManyHumanSpawn;

    //Use for Randomize the pos of spawn of Human
    private Vector2 pos;

    //Variable to know how many peoples were saves
    public int HowManyPeopleSave = 0;

    //Time during the simulation
    private float timer;

    //Define the GameObject for the text
    public TextMeshProUGUI CptPeopleSaveText;
    public TextMeshProUGUI TimerText;

    //Define if the simulation is on going or not
    private bool isSimulating = false;

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        //Code to start the simulation
        if (Input.GetKeyDown(KeyCode.Space))
        {
            DestroyAllHuman(); //Destroy all the human on the map
            StopTheFire(); //Stop the fire

            CreateHuman(HowManyHumanSpawn); // Create the amount of human who need to spawn
            StartTheFire(); //Start the Fire

            timer = 0; //Reset the timer
            HowManyPeopleSave = 0; // Reset the number of people save
            Time.timeScale = 1; // This allow the peoples to move
            isSimulating = true;
        }


        //Everybody are safe, end of the simulation
        if (HowManyHumanSpawn == HowManyPeopleSave)
        {
            isSimulating = false; //The simulation is finish

            Debug.Log("Tout le monde est sauvé");

            //Need to be update because the last survivant won't be count if it's not update
            CptPeopleSaveText.text = "N: " + HowManyPeopleSave.ToString() + "/" + HowManyHumanSpawn.ToString();
        }

        //Not everybody are safe and the simulation is not finish
        else if (isSimulating)
        {
            //Update the Timer
            timer += Time.deltaTime;
            TimerText.text = "t: " + timer.ToString("n2") + "s";

            //Update the People Save text
            CptPeopleSaveText.text = "N: " + HowManyPeopleSave.ToString() + "/" + HowManyHumanSpawn.ToString();
        }

        else if (isSimulating == false)
        {
            Time.timeScale = 0; // If the simulation don't start nobody move
        }
    }

    //Create a Human with the model define in the public variable 
    void CreateHuman(int number)
    {
        for (int i = 0; i < number; i++)
        {
            //Instantiate the Game Object Human define by the public variable
            GameObject human = Instantiate(Human, new Vector3(Random.Range(-10.0f, 10.0f), Random.Range(-5.0f, 5.0f), -0.1f), new Quaternion(0, 0, 0, 0));
        }
    }

    void DestroyAllHuman() // Destroy all the humans on the map
    {
        GameObject[] gameObjects = GameObject.FindGameObjectsWithTag("Human");

        for (var i = 0; i < gameObjects.Length; i++)
        {
            Destroy(gameObjects[i]);
        }
    }

    void StartTheFire()
    {
        //Instantiate a fire, for now, the position is not important
        Instantiate(Fire);
    }

    void StopTheFire()
    {
        GameObject gameObject = GameObject.Find("Fire");
        Destroy(gameObject); // Destroy the fire
    }
}
