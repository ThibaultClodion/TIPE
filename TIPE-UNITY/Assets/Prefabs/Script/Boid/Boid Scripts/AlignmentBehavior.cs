using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(menuName = "Boid/Behavior/Alignement")]
public class AlignmentBehavior : BoidBehavior
{
    public override Vector2 CalculateMove(BoidAgent agent, List<Transform> context, GameManagerBoid gameManager)
    {
        //if no neighbors, maintain currenet alignement
        if (context.Count == 0)
        {
            return agent.transform.up;
        }

        //add all points together and average
        Vector2 alignementMove = Vector2.zero;

        foreach (Transform item in context)
        {
            alignementMove += (Vector2)item.transform.up;
        }

        alignementMove /= context.Count;

        return alignementMove;
    }
}
