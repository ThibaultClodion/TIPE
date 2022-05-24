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

        //Color the human in function of density
        //Coloration();


        //Everybody are safe, end of the simulation, restart
        if (HowManyHumanSpawn == HowManyPeopleSave)
        {
            Reset();
        }
    }

    private void Reset()
    {
        HowManyPeopleSave = 0; // Reset the number of people save
        SaveCSV(timer); //Save and Change the CSV

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
            Vector3 pos_Agent = new Vector3(Random.Range(2.5f, 67.5f), 0.85f, Random.Range(-32.5f, -2.5f));

            // Permit to avoid the fact that peoples spawn on other people or table etc
            while (Physics.CheckSphere(pos_Agent, SpawnCollisionCheckRadius, 3))
            {
                pos_Agent = new Vector3(Random.Range(2.5f, 67.5f), 0.85f, Random.Range(-32.5f, -2.5f));
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
    

    void SaveCSV(float timerOfExit)
    {
        //Path of the file
        string path = "C:/Users/darkz/Desktop/TIPE/Data/" + GameObject.FindGameObjectWithTag("Building").name + ".csv";

        //Create File if it doesn't exist
        if (!File.Exists(path))
        {
            File.WriteAllText(path, "Nombre Personnes;Temps Sortie Final;");
            for (int i = 0; i < HowManyHumanSpawn; i++)
            {
                File.AppendAllText(path, "Personne " + i.ToString() + ";");
            }
            File.AppendAllText(path, "\n");
        }

        //Add the new values
        File.AppendAllText(path, HowManyHumanSpawn.ToString() + ";" + timerOfExit.ToString() + ";");

        foreach (float time in exit_times)
        {
            File.AppendAllText(path, time.ToString() + ";");
        }
        File.AppendAllText(path, "\n");
    }

    /*
void DestroyAllHuman() // Destroy all the boids on the map
{
    GameObject[] gameObjects = GameObject.FindGameObjectsWithTag("Human");

    for (var i = 0; i < gameObjects.Length; i++)
    {
        Destroy(gameObjects[i]);
    }
}

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
            agent.after20Sec(humans_destination[i]); // Normally Move was call without argument
        }
        i++;
    }
}
*/
}