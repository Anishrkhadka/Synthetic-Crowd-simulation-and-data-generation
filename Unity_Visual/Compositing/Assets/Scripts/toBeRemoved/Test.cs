using UnityEngine;

public class Test : MonoBehaviour
{
    public GameObject body;

    public Camera_Control cameraControl;

    // Use this for initialization
    private void Start()
    {
        cameraControl = GameObject.FindGameObjectWithTag("CameraManager").GetComponent<Camera_Control>();
    }

    // Update is called once per frame
    private void Update()
    {
        CheckVisible();
        CheckHeight();
    }

    private void CheckVisible()
    {
        body.layer = 0;
        var off_pos = new Vector3(transform.position.x, transform.position.y + 1, transform.position.z);
        var direction = cameraControl.transform.position - off_pos;

        //Debug.Log(off_pos);
        var ray = new Ray(off_pos, direction);
        Debug.DrawLine(off_pos, direction * 100);
        //Ray ray = new Ray(cameraControl.transform.position, off_pos);
        //Debug.DrawLine(off_pos, cameraControl.transform.position);
        var hit = new RaycastHit();
        if (Physics.Raycast(ray, out hit))
            if (hit.transform.tag == "Obstacle")
                body.layer = 1;
    }

    private void CheckHeight()
    {
        var ray = new Ray(transform.position, transform.position + Vector3.down * 30);
        Debug.DrawLine(transform.position, transform.position + Vector3.down * 30);
        //Debug.DrawLine(off_pos, cameraControl.transform.position);
        var hit = new RaycastHit();
        if (Physics.Raycast(ray, out hit))
        {
            //Debug.Log("HIT");
            Debug.DrawLine(transform.position, hit.point, Color.blue);
            transform.position = new Vector3(transform.position.x, hit.point.y, transform.position.z);
        }
    }
}