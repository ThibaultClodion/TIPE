using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HumanBehaviour : MonoBehaviour
{

    private Rigidbody2D humanRb;

    // Start is called before the first frame update
    void Start()
    {
        humanRb = GetComponent<Rigidbody2D>();
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            humanRb.velocity = new Vector2(7f, 0f);
        }        
        else if (Input.GetKeyDown(KeyCode.LeftArrow))
        {
            humanRb.velocity = new Vector2(-7f, 0f);
        }        
        else if (Input.GetKeyDown(KeyCode.UpArrow))
        {
            humanRb.velocity = new Vector2(0f, 7f);
        }        
        else if (Input.GetKeyDown(KeyCode.DownArrow))
        {
            humanRb.velocity = new Vector2(0f, -7f);
        }
    }
}
