using UnityEngine;

public class Move_Agent : MonoBehaviour
{
    public GameObject body;

    public Vector3 camera_pos;
    public Camera_Control cameraControl;

    public bool check_height;
    private int frame_number = -1;
    public bool hide_enabled = true;

    public int ID;

    //CONTROL ANIMATIONS
    private Animator m_Animator;

    public Vector3[] positions;
    public float radius;
    public float ratio_x = 1;
    public float[] rotations;


    public bool running;
    public bool updated = true;

    // Use this for initialization
    private void Start()
    {
        m_Animator = GetComponent<Animator>();
        cameraControl = GameObject.FindGameObjectWithTag("CameraManager").GetComponent<Camera_Control>();

        camera_pos = cameraControl.gameObject.transform.position;
    }

    // Update is called once per frame
    private void Update()
    {
        if (frame_number != cameraControl.frame_number)
        {
            frame_number = cameraControl.frame_number;

            running = cameraControl.running;

            if (running)
            {
//                updated = false;
                if (check_height)
                    transform.position =
                        new Vector3(positions[frame_number].x, CheckHeight(), positions[frame_number].z);
                else
                    transform.position = new Vector3(positions[frame_number].x, 0, positions[frame_number].z);

                transform.eulerAngles = new Vector3(0, rotations[frame_number], 0);
                if (frame_number < positions.Length - 1)
                    transform.LookAt(new Vector3(positions[frame_number + 1].x, transform.position.y,
                        positions[frame_number + 1].z));
                if (hide_enabled)
                    CheckVisible();

                UpdateAnimator(frame_number);

                updated = true;
            }
        }
        else
        {
            transform.position = positions[0];
            running = false;
        }
    }

    public void UpdateAgent()
    {
        if (frame_number != cameraControl.frame_number)
        {
            frame_number = cameraControl.frame_number;
            if (check_height)
                transform.position = new Vector3(positions[frame_number].x, CheckHeight(), positions[frame_number].z);
            else
                transform.position = new Vector3(positions[frame_number].x, 0, positions[frame_number].z);

            transform.eulerAngles = new Vector3(0, rotations[frame_number], 0);
            CheckVisible();
            UpdateAnimator(frame_number);
        }
        else
        {
            transform.position = positions[0];
        }
    }

    private void CheckVisible()
    {
        body.layer = 0;

        var off_pos = new Vector3(transform.position.x, transform.position.y + 1, transform.position.z);
        var direction = camera_pos - off_pos;
        //Debug.Log(off_pos);
        var ray = new Ray(off_pos, direction);
        Debug.DrawRay(off_pos, direction);
        var hit = new RaycastHit();

        if (Physics.Raycast(ray, out hit))
        {
            var distance = (hit.point - off_pos).magnitude;
            //Debug.Log("HIT SOMETHING");
            if (hit.transform.tag == "Obstacle") // && distance < 3)
                body.layer = 1;
        }
    }

    private float CheckHeight()
    {
        var offset = transform.position;
        var ray = new Ray(offset, transform.position + Vector3.down * 300);
        var ray2 = new Ray(offset, transform.position + Vector3.up * 300);
        //Debug.DrawLine(offset, (transform.position + (Vector3.down * 300)));
        var hit = new RaycastHit();
        if (Physics.Raycast(ray, out hit))
        {
            if (hit.collider.tag != "Agent")
            {
                //Debug.Log("HIT");
                Debug.DrawLine(offset, hit.point, Color.blue);
                //this.transform.position = new Vector3(transform.position.x, hit.point.y, transform.position.z);
                return hit.point.y + 0.05f;
            }

            return transform.position.y;
        }

        if (Physics.Raycast(ray2, out hit))
        {
            if (hit.collider.tag != "Agent")
            {
                //Debug.Log("HIT");
                Debug.DrawLine(offset, hit.point, Color.blue);
                //this.transform.position = new Vector3(transform.position.x, hit.point.y, transform.position.z);
                return hit.point.y + 0.05f;
            }

            return transform.position.y;
        }

        return transform.position.y;
    }

    private void UpdateAnimator(int frame_number)
    {
        var velocity = 0.5f;
        if (frame_number > 1)
            velocity = Vector3.Magnitude(positions[frame_number] - positions[frame_number - 1]) *
                       cameraControl.animation_speed;
        // update the animator parameters
        m_Animator.SetFloat("Forward", velocity, 0.1f, Time.deltaTime);
    }

    public void SetScale(Vector3 scale)
    {
        transform.localScale = scale;
    }
}