using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(menuName = "Boid/Behavior/Stay In Radius")]
public class StayInRadiusBehavior : BoidBehavior
{
    public Vector2 center;
    public float radius  = 5.0f;


    public override Vector2 CalculateMove(BoidAgent agent, List<Transform> context, GameManagerBoid gameManager)
    {
        Vector2 centerOffset = center - (Vector2)agent.transform.position;
        float t = centerOffset.magnitude / radius;
        if (t < 0.9f)
        {
            return Vector2.zero;
        }

        return centerOffset * t * t;
    }
}
