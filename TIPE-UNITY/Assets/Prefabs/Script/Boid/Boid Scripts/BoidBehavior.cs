using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class BoidBehavior : ScriptableObject
{
    public abstract Vector2 CalculateMove(BoidAgent agent, List<Transform> context, GameManagerBoid gameManager);
}
