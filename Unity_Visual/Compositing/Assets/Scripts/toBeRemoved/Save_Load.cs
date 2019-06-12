using System.IO;
using UnityEngine;

public class Save_Load : MonoBehaviour
{
    private Background_Camera backgroundCamera;

    private Camera_Control cameraControl;


    private StreamReader fileRead;
    private StreamWriter fileWrite;
    private string path;
    private Agents_Scale scaleAgent;

    // Use this for initialization
    private void Start()
    {
        //GET OBJECTS CONTAINING THE SAVE AND LOAD VARIABLES
        path = "Save.txt";
        cameraControl = GameObject.FindGameObjectWithTag("CameraManager").GetComponent<Camera_Control>();
        backgroundCamera = GameObject.FindGameObjectWithTag("Background_Camera").GetComponent<Background_Camera>();
        scaleAgent = GameObject.FindGameObjectWithTag("Scale_Agents").GetComponent<Agents_Scale>();


        Load();
    }

    // Update is called once per frame
    public void Save()
    {
        fileWrite = new StreamWriter(path, false);
        //CAMERA POSITION
        var line = cameraControl.transform.position.x.ToString();
        fileWrite.WriteLine(line);
        line = cameraControl.transform.position.y.ToString();
        fileWrite.WriteLine(line);
        line = cameraControl.transform.position.z.ToString();
        fileWrite.WriteLine(line);

        //CAMERA ROTATION
        line = cameraControl.transform.eulerAngles.x.ToString();
        fileWrite.WriteLine(line);
        line = cameraControl.transform.eulerAngles.y.ToString();
        fileWrite.WriteLine(line);
        line = cameraControl.transform.eulerAngles.z.ToString();
        fileWrite.WriteLine(line);

        //FIELD OF VIEW VALUE
        line = cameraControl.current_fov.ToString();
        fileWrite.WriteLine(line);

        //BACKGROUND IMAGE SCALE
        line = backgroundCamera.current_scale.x.ToString();
        fileWrite.WriteLine(line);

        //CHARACTER MODEL SCALE
        line = scaleAgent.scale.x.ToString();
        fileWrite.WriteLine(line);

        //CHARACTER MODEL POSITION
        line = scaleAgent.transform.position.x.ToString();
        fileWrite.WriteLine(line);
        line = scaleAgent.transform.position.y.ToString();
        fileWrite.WriteLine(line);
        line = scaleAgent.transform.position.z.ToString();
        fileWrite.WriteLine(line);

        //CHARACTER MODEL ANIMATION SPEED
        line = cameraControl.animation_speed.ToString();
        fileWrite.WriteLine(line);

        //SCREENSHOT PREFIX
        line = cameraControl.screenshot_prefix;
        fileWrite.WriteLine(line);
        fileWrite.Close();
    }

    public void Load()
    {
        fileRead = new StreamReader(File.OpenRead(path));
        //CAMERA POSITION
        var vec = Vector3.zero;
        float.TryParse(fileRead.ReadLine(), out vec.x);
        float.TryParse(fileRead.ReadLine(), out vec.y);
        float.TryParse(fileRead.ReadLine(), out vec.z);
        cameraControl.transform.position = vec;
        //CAMERA ROTATION
        float.TryParse(fileRead.ReadLine(), out vec.x);
        float.TryParse(fileRead.ReadLine(), out vec.y);
        float.TryParse(fileRead.ReadLine(), out vec.z);
        cameraControl.transform.eulerAngles = vec;
        //FIELD OF VIEW VALUE
        float temp = 0;
        float.TryParse(fileRead.ReadLine(), out temp);
        cameraControl.SetFOV(temp);
        //BACKGROUND IMAGE SCALE
        temp = 0;
        float.TryParse(fileRead.ReadLine(), out temp);
        backgroundCamera.SetScale(new Vector3(temp, temp, 0));
        //CHARACTER MODEL SCALE
        temp = 0;
        float.TryParse(fileRead.ReadLine(), out temp);
        scaleAgent.SetScale(new Vector3(temp, temp, temp));
        //CHARACTER MODEL POSITION
        float.TryParse(fileRead.ReadLine(), out vec.x);
        float.TryParse(fileRead.ReadLine(), out vec.y);
        float.TryParse(fileRead.ReadLine(), out vec.z);
        scaleAgent.transform.position = vec;
        //CHARACTER MODEL ANIMATION SPEED
        float.TryParse(fileRead.ReadLine(), out cameraControl.animation_speed);
        //SCREENSHOT PREFIX
        cameraControl.screenshot_prefix = fileRead.ReadLine();

        fileRead.Close();
    }
}