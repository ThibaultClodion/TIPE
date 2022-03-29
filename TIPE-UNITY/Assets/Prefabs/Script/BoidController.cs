using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoidController : MonoBehaviour
{
    //Parameters of the boids
    public int SwarmIndex;
    public float NoClumpingRadius;
    public float LocalAreaRadius;
    public float Speed;
    public float SteeringSpeed;
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }
    public void SimulateMovement(List<BoidController> other, float time)
    {
        //default vars
        var steering = Vector3.zero;

        //apply steering
        if (steering != Vector3.zero)
            transform.rotation = Quaternion.RotateTowards(transform.rotation, Quaternion.LookRotation(steering), SteeringSpeed * time);

        //move 
        transform.position += transform.TransformDirection(new Vector3(Speed, 0, 0)) * time;
    }
}
