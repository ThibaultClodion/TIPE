using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class GameManager : MonoBehaviour
{
    //Define the GameObject use for the Fire
    public GameObject Fire;

    //Define How many humans spawn at the start of simulation
    [Range(1f, 500f)]
    public int HowManyHumanSpawn;

    //Variable to know how many peoples were saves
    public int HowManyPeopleSave = 0;

    //Time during the simulation
    public float timer;

    [Range(1f, 10f)]
    public float neighborRadius = 1.5f;

    //Define the GameObject for the text
    public TextMeshProUGUI CptPeopleSaveText;
    public TextMeshProUGUI TimerText;

    //Define if the simulation is on going or not
    private bool isSimulating = false;

    //List of exit time for data
    public List<float> exit_times;

    //All these variables are for the PSO algorthims
    //Position of ExitZone
    public List<GameObject> ExitsZone = new List<GameObject>();
    public List<Vector2> minGlobal = new List<Vector2>(); // minimum pos reach by swarm

    List<PSOAgent> humans = new List<PSOAgent>(); //Possibility to make a list of list to have different zone further
    public PSOAgent HumanPrefab;



    // Start is called before the first frame update
    void Start()
    {
        int i = 0;
        foreach(GameObject ExitZone in ExitsZone)
        {
            minGlobal.Add(ExitsZone[i].transform.position);
            i++;
        }

    }

    // Update is called once per frame
    void Update()
    {
        //Code to start the simulation
        if (Input.GetKeyDown(KeyCode.Space))
        {
            DestroyAllHuman(); //Destroy all the boids on the map

            humans = new List<PSOAgent>(); //Reset the humans list

            //StopTheFire(); //Stop the fire

            SpawnHuman(HowManyHumanSpawn); // Create the amount of human who need to spawn
            //StartTheFire(); //Start the Fire

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
            isSimulating = false; //The simulation is finish

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

            //Color the human in function of density
            Coloration();

            //Permit the movement
            Movement();
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
            PSOAgent newAgent = Instantiate(HumanPrefab,
                new Vector3(Random.Range(-28f, 34f), Random.Range(-16.5f, 16.5f), -0.1f),
                Quaternion.Euler(Vector3.forward * Random.Range(0f, 360f)), transform);

            newAgent.name = "Agent" + i;
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

    void StartTheFire()
    {
        //Instantiate a fire, for now, the position is not important
        Instantiate(Fire);
    }

    void StopTheFire()
    {
        //Here the name of the Fire which spawned is "Fire(Clone)"
        GameObject gameObject = GameObject.Find("Fire(Clone)");
        Destroy(gameObject); // Destroy the fire
    }

    void Coloration()
    {
        foreach (PSOAgent human in humans)
        {
            if (human != null)
            {
                List<Transform> context = GetNearbyObjects(human);

                //Fade the color from yellow to red with the density
                human.GetComponent<SpriteRenderer>().color = Color.Lerp(Color.yellow, Color.red, context.Count / 50f);
            }
        }
    }

    List<Transform> GetNearbyObjects(PSOAgent agent)
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
        foreach (PSOAgent agent in humans)
        {
            if (agent != null)
            {
                agent.Move();
            }
        }
    }

    public float batimentFunction(int WhichExitZone, Vector2 pos)
    {
        Vector2 Distance = minGlobal[WhichExitZone] - pos;
        return Distance.magnitude * Distance.magnitude;
    }
}
