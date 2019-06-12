using UnityEngine;
using System.Collections;
using System.IO;

public class Camera_Control : MonoBehaviour
{
    public GameObject[] agents;

    public float animation_speed = 10;
    public GameObject canvas;
    public float current_fov;

    public float fov_amount = 1;
    public int frame_number;
    public int max_frames;

    public float move_amount = 1;
    public float rot_amount = 1;
    public bool running;

    Agents_Scale scale_agents;
    public bool screenshot = false;
    public string screenshot_prefix = "RECORDING_NAME";

    Read_Data settings;

    void Start()
    {
        settings = GameObject.FindGameObjectWithTag("Read_Data").GetComponent<Read_Data>();
        canvas = GameObject.FindGameObjectWithTag("Canvas");
        scale_agents = GameObject.FindGameObjectWithTag("Scale_Agents").GetComponent<Agents_Scale>();

        current_fov = this.gameObject.GetComponent<Camera>().fieldOfView;


//        max_frames = settings.num_frames - 1;
    }

    void Update()
    {
        if (running)
        {
            if (frame_number < settings.num_frames - 1)
            {
                TakeScreenshot();

                if (CanContinue())
                {
                    frame_number++;
                }
            }
            else
            {
                running = false;
                canvas.SetActive(true);

                foreach (Transform child in settings.floor_parent.transform)
                {
                    child.gameObject.layer = 0;
                    if (child.gameObject.tag == "Floor_Tile")
                        child.gameObject.SetActive(true);
                }

                scale_agents.gameObject.SetActive(true);
            }
        }
        else
        {
        }

        // -- Stop the sim when space is pressed --//
        if (Input.GetKeyDown(KeyCode.Space))
            StopSim();
    }

    public void Run()
    {
        for (int i = 0; i < settings.num_frames; i++)
        {
            TakeScreenshot();
            frame_number++;
            foreach (GameObject agent in agents)
            {
                agent.GetComponent<Move_Agent>().UpdateAgent();
            }
        }

        running = false;
        canvas.SetActive(true);
        foreach (Transform child in settings.floor_parent.transform)
        {
            child.gameObject.layer = 0;
        }

        scale_agents.gameObject.SetActive(true);
    }

    public void RunSim()
    {
        SetAgentScale(scale_agents.scale);

        if (screenshot)
        {
            Directory.CreateDirectory(screenshot_prefix);
        }

        // -- Start the Main loop --//
        running = true;
        frame_number = 0;

        // -- Hide the floorManager, canvas, scale_agents --//
        foreach (Transform child in settings.floor_parent.transform)
        {
            child.gameObject.layer = 1;
            if (child.gameObject.tag == "Floor_Tile")
                child.gameObject.SetActive(false);
        }

        canvas.SetActive(false);
        scale_agents.gameObject.SetActive(false);
    }

    public void StopSim()
    {
        running = false;
        frame_number = 0;
        foreach (Transform child in settings.floor_parent.transform)
        {
            child.gameObject.layer = 0;
            if (child.gameObject.tag == "Floor_Tile")
                child.gameObject.SetActive(true);
        }

        canvas.SetActive(true);

        scale_agents.gameObject.SetActive(true);
    }

    public void TakeScreenshot()
    {
        if (screenshot)
            ScreenCapture.CaptureScreenshot(screenshot_prefix + "/" + screenshot_prefix + "_" +
                                            frame_number.ToString("0000") + ".png");
    }

    bool CanContinue()
    {
        for (int i = 0; i < agents.Length; i++)
        {
            if (agents[i].GetComponent<Move_Agent>().updated == false)
                return false;
        }

        return true;
    }


    public void XUp()
    {
        Vector3 current_pos = this.transform.position;
        this.transform.position = current_pos + new Vector3(move_amount, 0, 0);
    }

    public void YUp()
    {
        Vector3 current_pos = this.transform.position;
        this.transform.position = current_pos + new Vector3(0, move_amount, 0);
    }

    public void ZUp()
    {
        Vector3 current_pos = this.transform.position;
        this.transform.position = current_pos + new Vector3(0, 0, move_amount);
    }

    public void XDown()
    {
        Vector3 current_pos = this.transform.position;
        this.transform.position = current_pos + new Vector3(-move_amount, 0, 0);
    }

    public void YDown()
    {
        Vector3 current_pos = this.transform.position;
        this.transform.position = current_pos + new Vector3(0, -move_amount, 0);
    }

    public void ZDown()
    {
        Vector3 current_pos = this.transform.position;
        this.transform.position = current_pos + new Vector3(0, 0, -move_amount);
    }

    public void XRotUp()
    {
        Vector3 current_rot = this.transform.eulerAngles;
        this.transform.eulerAngles = current_rot + new Vector3(rot_amount, 0, 0);
    }

    public void YRotUp()
    {
        Vector3 current_rot = this.transform.eulerAngles;
        this.transform.eulerAngles = current_rot + new Vector3(0, rot_amount, 0);
    }

    public void ZRotUp()
    {
        Vector3 current_rot = this.transform.eulerAngles;
        this.transform.eulerAngles = current_rot + new Vector3(0, 0, rot_amount);
    }

    public void XRotDown()
    {
        Vector3 current_rot = this.transform.eulerAngles;
        this.transform.eulerAngles = current_rot + new Vector3(-rot_amount, 0, 0);
    }

    public void YRotDown()
    {
        Vector3 current_rot = this.transform.eulerAngles;
        this.transform.eulerAngles = current_rot + new Vector3(0, -rot_amount, 0);
    }

    public void ZRotDown()
    {
        Vector3 current_rot = this.transform.eulerAngles;
        this.transform.eulerAngles = current_rot + new Vector3(0, 0, -rot_amount);
    }

    public void FOVUp()
    {
        current_fov = this.gameObject.GetComponent<Camera>().fieldOfView;
        this.gameObject.GetComponent<Camera>().fieldOfView = current_fov + fov_amount;
    }

    public void FOVDown()
    {
        current_fov = this.gameObject.GetComponent<Camera>().fieldOfView;
        this.gameObject.GetComponent<Camera>().fieldOfView = current_fov - fov_amount;
    }

    public void SetFOV(float fov)
    {
        this.gameObject.GetComponent<Camera>().fieldOfView = fov;
        this.current_fov = fov;
    }

    public void AnimationSpeedUp()
    {
        animation_speed += 0.1f;
    }

    public void AnimationSpeedDown()
    {
        animation_speed -= 0.1f;
    }

    public void SetAgentScale(Vector3 scale)
    {
        for (int i = 0; i < agents.Length; i++)
        {
            agents[i].transform.localScale = new Vector3(scale.x + (agents[i].GetComponent<Move_Agent>().radius * 0.1f),
                scale.y + (agents[i].GetComponent<Move_Agent>().radius * 0.1f),
                scale.z + (agents[i].GetComponent<Move_Agent>().radius * 0.1f));
        }
    }
}