using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu (menuName = "Boid/Behavior/Cohesion")]
public class CohesionBehavior : BoidBehavior
{
    public override Vector2 CalculateMove(BoidAgent agent, List<Transform> context, GameManager gameManager)
    {
       //if no neighbors, return no adjustement
       if(context.Count == 0)
        {
            return Vector2.zero;
        }

        //add all points together and average
        Vector2 cohesionMove = Vector2.zero;

        foreach(Transform item in context)
        {
            cohesionMove += (Vector2)item.position;
        }

        cohesionMove /= context.Count;

        //create offset from agent position
        cohesionMove -= (Vector2)agent.transform.position;

        return cohesionMove;
    }
}
