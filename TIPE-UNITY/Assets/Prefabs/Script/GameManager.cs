using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class GameManager : MonoBehaviour
{
    //Define the GameObject use for Human
    public GameObject Human;

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




    // Start is called before the first frame update
    void Start()
    {
        for (int i = 0; i < HowManyHumanSpawn; i++)
        {
            CreateHuman();
        }

    }

    // Update is called once per frame
    void Update()
    {
        //Everybody are safe
        if(HowManyHumanSpawn == HowManyPeopleSave)
        {
            Debug.Log("Tout le monde est sauvé");

            //Need to be update because the last survivant won't be count if it's not update
            CptPeopleSaveText.text = "N: " + HowManyPeopleSave.ToString() + "/" + HowManyHumanSpawn.ToString();
        }
        //Not everybody are safe
        else
        {
            //Cas où il reste encore des gens à sauvés
            //Update the Timer
            timer += Time.deltaTime;
            TimerText.text = "t: " + timer.ToString("n2") + "s";

            //Update the People Save text
            CptPeopleSaveText.text = "N: " + HowManyPeopleSave.ToString() + "/" + HowManyHumanSpawn.ToString();
        }

    }

    //Create a Human with the model define in the public variable 
    void CreateHuman()
    {
        //Instantiate the Game Object Human define by the public variable
        GameObject human_test = Instantiate(Human, new Vector3(Random.Range(-10.0f, 10.0f), Random.Range(-5.0f, 5.0f), -0.1f), new Quaternion(0,0,0,0));
    }
}
