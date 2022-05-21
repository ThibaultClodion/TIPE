using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using System.IO;

public class GameManager : MonoBehaviour
{

    //Define How many humans spawn at the start of simulation
    [Range(1f, 500f)]
    public int HowManyHumanSpawn;

    //Variable to know how many peoples were saves
    public int HowManyPeopleSave = 0;

    //Time during the simulation
    public float timer;

    /*[Range(1f, 10f)]
    public float neighborRadius = 1.5f;*/

    //Define the GameObject for the text
    public TextMeshProUGUI CptPeopleSaveText;
    public TextMeshProUGUI TimerText;

    //Define if the simulation is on going or not
    private bool isSimulating = false;

    //List of exit time for data
    public List<float> exit_times;

    List<Human> humans = new List<Human>();
    public Human HumanPrefab;

    //Position of ExitZone
    public List<Transform> ExitZonePos; // minimum pos reach by swarm


    // Update is called once per frame
    void Update()
    {
        //Code to start the simulation
        if (Input.GetKeyDown(KeyCode.Space))
        {
            DestroyAllHuman(); //Destroy all the boids on the map

            humans = new List<Human>(); //Reset the humans list


            SpawnHuman(HowManyHumanSpawn); // Create the amount of human who need to spawn

            //Reset the exit_times
            exit_times = new List<float>();
            timer = 0; //Reset the timer
            HowManyPeopleSave = 0; // Reset the number of people save
            Time.timeScale = 1; // This allow the peoples to move
            isSimulating = true;
        }


        //Everybody are safe, end of the simulation
        if (HowManyHumanSpawn == HowManyPeopleSave)
        {
            //This test permit to not save twice the data
            if (isSimulating == true)
            {
                SaveCSV(timer); //Save and Change the CSV
            }
            isSimulating = false; //The simulation is finish

            //Need to be update because the last survivant won't be count if it's not update
            CptPeopleSaveText.text = "N: " + HowManyPeopleSave.ToString() + "/" + HowManyHumanSpawn.ToString();

            DestroyAllHuman(); //Destroy all the boids on the map

            humans = new List<Human>(); //Reset the humans list


            SpawnHuman(HowManyHumanSpawn); // Create the amount of human who need to spawn

            //Reset the exit_times
            exit_times = new List<float>();
            timer = 0; //Reset the timer
            HowManyPeopleSave = 0; // Reset the number of people save
            Time.timeScale = 1; // This allow the peoples to move
            isSimulating = true;
        }

        //Not everybody are safe and the simulation is not finish
        else if (isSimulating)
        {
            //Update the Timer
            timer += Time.deltaTime;
            TimerText.text = "t: " + timer.ToString("n2") + "s";

            //Update the People Save text
            CptPeopleSaveText.text = "N: " + HowManyPeopleSave.ToString() + "/" + HowManyHumanSpawn.ToString();

            //Color the human in function of density
            //Coloration();

            //Permit the movement
            //Movement();

        }

        else if (isSimulating == false)
        {
            Time.timeScale = 0; // If the simulation don't start nobody move
        }
    }

    //Create "number" human with the model define in the public variable 
    void SpawnHuman(int number)
    {
        for (int i = 0; i < number; i++)
        {
            Vector3 pos_Agent = new Vector3(Random.Range(3, 67), 0.85f, Random.Range(-32, -3));
            Human newAgent = Instantiate(HumanPrefab, pos_Agent,
                Quaternion.Euler(Vector3.forward * Random.Range(0f, 360f)), transform);

            newAgent.name = "Agent" + i;

            newAgent.Move(DefineClosestExitZone(pos_Agent));

            humans.Add(newAgent);
        }
    }

    void DestroyAllHuman() // Destroy all the boids on the map
    {
        GameObject[] gameObjects = GameObject.FindGameObjectsWithTag("Human");

        for (var i = 0; i < gameObjects.Length; i++)
        {
            Destroy(gameObjects[i]);
        }
    }

    /*
     * void Coloration()
    {
        foreach (Human human in humans)
        {
            if (human != null)
            {
                List<Transform> context = GetNearbyObjects(human);

                //Fade the color from yellow to red with the density
                human.GetComponent<SpriteRenderer>().color = Color.Lerp(Color.yellow, Color.red, context.Count / 50f);
            }
        }
    }

    List<Transform> GetNearbyObjects(Human agent)
    {
        List<Transform> context = new List<Transform>();
        Collider2D[] contextColliders = Physics2D.OverlapCircleAll(agent.transform.position, neighborRadius);
        foreach (Collider2D c in contextColliders)
        {
            if (c != agent)
            {
                context.Add(c.transform);
            }
        }
        return context;
    }
    */

    Transform DefineClosestExitZone(Vector3 humanPos)
    {
        int i = 0;
        int min_i = 0;
        float min = Vector3.Distance(ExitZonePos[0].position, humanPos);
        foreach(Transform exitZone in ExitZonePos)
        {
            if(min > Vector3.Distance(exitZone.position, humanPos))
                {
                min_i = i;
                min = Vector3.Distance(exitZone.position, humanPos);
                }
            i++;
        }
        return ExitZonePos[min_i];
    }

    /*
    void Movement()
    {
        foreach (Human agent in humans)
        {
            if (agent != null)
            {
                agent.Move(ExitZonePos[0]); // Normally Move was call without argument
            }
        }
    }
    */

    void SaveCSV(float timerOfExit)
    {
        //Path of the file
        string path = "C:/Users/darkz/Desktop/TIPE/Data/" + GameObject.FindGameObjectWithTag("Building").name + ".csv";
        
        //Create File if it doesn't exist
        if(!File.Exists(path))
        {
            File.WriteAllText(path, "Nombre Personnes;Temps Sortie Final;");
            for(int i = 0; i < HowManyHumanSpawn; i++)
            {
                File.AppendAllText(path, "Personne " + i.ToString() + ";");
            }
            File.AppendAllText(path, "\n");
        }

        //Add the new values
        File.AppendAllText(path, HowManyHumanSpawn.ToString() + ";" + timerOfExit.ToString() + ";");

        foreach(float time in exit_times)
        {
            File.AppendAllText(path, time.ToString() + ";");
        }
        File.AppendAllText(path, "\n");
    }
}
