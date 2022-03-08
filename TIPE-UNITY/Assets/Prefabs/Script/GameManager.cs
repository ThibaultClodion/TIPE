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
        //Cas où le nombre de personnes sauvés est égal au nombre de personnes présentes
        if(HowManyHumanSpawn == HowManyPeopleSave)
        {
        }
        //Cas où il reste encore des gens à sauvés
        else
        {
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
        //Increment the variable of how many people spawn at total
        HowManyHumanSpawn++;

        //Instantiate the Game Object Human define by the public variable
        GameObject human_test = Instantiate(Human);

        //Give a random pos to the human
        pos = new Vector3(Random.Range(-10.0f, 10.0f), Random.Range(-5.0f, 5.0f), -0.1f);
        human_test.transform.localPosition = pos;
    }
}
