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
    public float timer = 0;

    public float SpawnCollisionCheckRadius;

    //Define the GameObject for the text
    public TextMeshProUGUI CptPeopleSaveText;
    public TextMeshProUGUI TimerText;


    //List of exit time for data
    public List<float> exit_times = new List<float>();

    List<Human> humans = new List<Human>();
    public Human HumanPrefab;

    private List<Transform> humans_destination = new List<Transform>();

    //Position of ExitZone
    public List<Transform> ExitZonePos; // minimum pos reach by swarm

    private void Start()
    {

        SpawnHuman(HowManyHumanSpawn); // Create the amount of human who need to spawn
    }

    // Update is called once per frame
    void Update()
    {
        //Update the Timer
        timer += Time.deltaTime;
        TimerText.text = "t: " + timer.ToString("n2") + "s";

        //Update the People Save text
        CptPeopleSaveText.text = "N: " + HowManyPeopleSave.ToString() + "/" + HowManyHumanSpawn.ToString();

        //Everybody are safe, end of the simulation, restart
        if (HowManyHumanSpawn == HowManyPeopleSave)
        {
            Reset(true); //Reset de manière normale
        }

        if(timer > 35)
        {
            Reset(false); //Permet de Reset si le temps est trop long au cas où il y est un bug
        }

        //Allow to Take Screenshot when "P" is press
        if (Input.GetKeyDown(KeyCode.P))
        {
            TakeScreenshot();
        }

    }

    private void Reset(bool SaveResult)
    {
        HowManyPeopleSave = 0; // Reset the number of people save

        if (SaveResult == true)
        {
            SaveCSV(); //Save and Change the CSV
        }
        if(SaveResult == false)
        {
            DestroyAllHuman();
        }
        humans = new List<Human>(); //Reset the humans list
        humans_destination = new List<Transform>(); //Reset the humans_destination list
        exit_times = new List<float>(); //Reset the exit_times


        SpawnHuman(HowManyHumanSpawn); // Create the amount of human who need to spawn

        timer = 0; //Reset the timer
    }


    //Create "number" human with the model define in the public variable 
    void SpawnHuman(int number)
    {
        for (int i = 0; i < number; i++)
        {
            //Define where the agent can spawn and create a random Vector 3D to spawn i'm at this point.
            Vector3 pos_Agent = new Vector3(Random.Range(0f, 70f), 0.85f, Random.Range(-35f, 0f));

            // Permit to avoid the fact that peoples spawn on other people or table
            // The 3 represent the Layer that is not considered by CheckSphere (here the Ground layer because we want people to be able to spawn on the ground)
            while (Physics.CheckSphere(pos_Agent, SpawnCollisionCheckRadius, 3))
            {
                pos_Agent = new Vector3(Random.Range(0f, 70f), 0.85f, Random.Range(-35f, 0f));
            }

            Human newAgent = Instantiate(HumanPrefab, pos_Agent,
            Quaternion.Euler(Vector3.forward * Random.Range(0f, 360f)), transform);

            newAgent.name = "Agent" + i;

            Transform Closest_destination = DefineClosestExitZone(pos_Agent); // Store the nearest destination of all agents
            newAgent.Move(Closest_destination);

            humans_destination.Add(Closest_destination);
            humans.Add(newAgent);
        }
    }

    Transform DefineClosestExitZone(Vector3 humanPos)
    {
        Transform bestTarget = null;
        float min_dist = Mathf.Infinity;

        foreach (Transform exitZone in ExitZonePos)
        {
            Vector3 direction = exitZone.position - humanPos;
            float dSqrToTarget = direction.sqrMagnitude;

            if (dSqrToTarget < min_dist)
            {
                min_dist = dSqrToTarget;
                bestTarget = exitZone;
            }
        }
        return bestTarget;
    }
    

    void SaveCSV()
    {
        //Path of the file
        string path = "C:/Users/darkz/Desktop/TIPE/Data/" + GameObject.FindGameObjectWithTag("Building").name + ".csv";

        //Create File if it doesn't exist
        if (!File.Exists(path))
        {
            for (int i = 0; i < HowManyHumanSpawn; i++)
            {
                File.AppendAllText(path, "Personne " + i.ToString() + ";");
            }
            File.AppendAllText(path, "\n");
        }

        foreach (float time in exit_times)
        {
            File.AppendAllText(path, time.ToString() + ";");
        }

        File.AppendAllText(path, "\n");
    }

    public void TakeScreenshot()
        {
        string timeNow = System.DateTime.Now.ToString("dd-MMMM-yyyy HHmmss");

        ScreenCapture.CaptureScreenshot("C:/Users/darkz/Desktop/TIPE/Document pour présentation etc/Screenshot - Unity/" + GameObject.FindGameObjectWithTag("Building").name + "  " + timeNow + ".png");
        }

    void DestroyAllHuman() // Destroy all the boids on the map
    {
        GameObject[] gameObjects = GameObject.FindGameObjectsWithTag("Human");

        for (var i = 0; i < gameObjects.Length; i++)
        {
            Destroy(gameObjects[i]);
        }
    }
}

/*
 private void Coloration()
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

    void Movement()
    {
        int i = 0;
        foreach (Human agent in humans)
        {
            if (agent != null)
            {
                agent.Move(humans_destination[i]);
            }
            i++;
        }
    }
*/