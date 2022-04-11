using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(menuName = "Boid/Behavior/Go Nearest Door")]
public class GoNearestDoorBehaviour : BoidBehavior
{
    public List<Transform> ExitZonePos;
    public Vector3 NearestExitZonePos = new Vector3(4000,4000,4000);

    public override Vector2 CalculateMove(BoidAgent agent, List<Transform> context, GameManagerBoid gameManager)
    {
        var objects = GameObject.FindGameObjectsWithTag("ExitZone");

        foreach(var obj in objects)
        {
            if(Vector3.Distance(obj.GetComponent<Transform>().position, agent.transform.position) < Vector3.Distance(NearestExitZonePos, agent.transform.position))
            {
                NearestExitZonePos = obj.GetComponent<Transform>().position;
            }
        }
        return NearestExitZonePos;
    }
}
