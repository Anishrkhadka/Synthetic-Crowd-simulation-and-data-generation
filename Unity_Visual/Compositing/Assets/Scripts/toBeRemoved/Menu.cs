using UnityEngine;

public class Menu : MonoBehaviour
{
    private Background_Camera backgroundControl;
    private Camera_Control cameraControl;
    private int height;
    private Save_Load saveOrLoad;
    private Agents_Scale scaleAgents;

    private State state;
    private int width;

    // Use this for initialization
    private void Start()
    {
        state = State.Main;

        cameraControl = GameObject.FindGameObjectWithTag("CameraManager").GetComponent<Camera_Control>();
        backgroundControl = GameObject.FindGameObjectWithTag("Background_Camera").GetComponent<Background_Camera>();
        saveOrLoad = GameObject.FindGameObjectWithTag("CameraManager").GetComponent<Save_Load>();
        scaleAgents = GameObject.FindGameObjectWithTag("Scale_Agents").GetComponent<Agents_Scale>();
    }

    // // Update is called once per frame
    // void Update () {

    // }

    private void OnGUI()
    {
        if (!cameraControl.running)
        {
            switch (state)
            {
                case State.Main:
                    if (GUI.Button(new Rect(5, 5, 50, 50), "BGRD")) state = State.Move_Background;
                    if (GUI.Button(new Rect(5, 60, 50, 50), "CAM")) state = State.Move_Camera;
                    if (GUI.Button(new Rect(5, 115, 50, 50), "CHAR")) state = State.Resize_characters;
                    cameraControl.screenshot_prefix = GUI.TextField(
                        new Rect(5, backgroundControl.screen_height - 25, 150, 20), cameraControl.screenshot_prefix,
                        50);

                    break;
                case State.Move_Background:
                    if (GUI.Button(new Rect(5, 5, 50, 50), "ZOOM +")) backgroundControl.ScaleUp();
                    if (GUI.Button(new Rect(60, 5, 50, 50), "ZOOM -")) backgroundControl.ScaleDown();
                    if (GUI.Button(new Rect(5, backgroundControl.screen_height - 55, 50, 50), "BACK"))
                        state = State.Main;
                    break;

                case State.Move_Camera:
                    if (GUI.Button(new Rect(60, 5, 50, 50), "FRD")) cameraControl.ZUp();
                    if (GUI.Button(new Rect(60, 115, 50, 50), "BCK")) cameraControl.ZDown();
                    if (GUI.Button(new Rect(5, 60, 50, 50), "LFR")) cameraControl.XDown();
                    if (GUI.Button(new Rect(115, 60, 50, 50), "RGT")) cameraControl.XUp();
                    if (GUI.Button(new Rect(5, 115, 50, 50), "UP")) cameraControl.YDown();
                    if (GUI.Button(new Rect(115, 115, 50, 50), "DWN")) cameraControl.YUp();

                    if (GUI.Button(
                        new Rect(backgroundControl.screen_width / 2 + 2.5f, backgroundControl.screen_height - 55, 50,
                            50), "FOV +")) cameraControl.FOVUp();
                    if (GUI.Button(
                        new Rect(backgroundControl.screen_width / 2 - 52.5f, backgroundControl.screen_height - 55, 50,
                            50), "FOV -")) cameraControl.FOVDown();

                    if (GUI.Button(new Rect(backgroundControl.screen_width - 110, 5, 50, 50), "PCH +"))
                        cameraControl.XRotDown();
                    if (GUI.Button(new Rect(backgroundControl.screen_width - 110, 115, 50, 50), "PCH -"))
                        cameraControl.XRotUp();
                    if (GUI.Button(new Rect(backgroundControl.screen_width - 165, 60, 50, 50), "YAW -"))
                        cameraControl.YRotDown();
                    if (GUI.Button(new Rect(backgroundControl.screen_width - 55, 60, 50, 50), "YAW +"))
                        cameraControl.YRotUp();
                    if (GUI.Button(new Rect(backgroundControl.screen_width - 165, 115, 50, 50), "ROLL -"))
                        cameraControl.ZRotDown();
                    if (GUI.Button(new Rect(backgroundControl.screen_width - 55, 115, 50, 50), "ROLL +"))
                        cameraControl.ZRotUp();

                    if (GUI.Button(new Rect(5, backgroundControl.screen_height - 55, 50, 50), "BACK"))
                        state = State.Main;
                    break;
                case State.Resize_characters:
                    if (GUI.Button(new Rect(60, 5, 50, 50), "FRD")) scaleAgents.ZUp();
                    if (GUI.Button(new Rect(60, 115, 50, 50), "BCK")) scaleAgents.ZDown();
                    if (GUI.Button(new Rect(5, 60, 50, 50), "LFR")) scaleAgents.XDown();
                    if (GUI.Button(new Rect(115, 60, 50, 50), "RGT")) scaleAgents.XUp();
                    if (GUI.Button(new Rect(backgroundControl.screen_width - 55, 5, 50, 50), "ANI +"))
                        cameraControl.AnimationSpeedUp();
                    if (GUI.Button(new Rect(backgroundControl.screen_width - 165, 5, 50, 50), "ANI -"))
                        cameraControl.AnimationSpeedDown();
                    GUI.TextArea(new Rect(backgroundControl.screen_width - 110, 5, 50, 50),
                        cameraControl.animation_speed.ToString());

                    if (GUI.Button(
                        new Rect(backgroundControl.screen_width / 2 + 2.5f, backgroundControl.screen_height - 55, 50,
                            50), "SCL +")) scaleAgents.ScaleUp();
                    if (GUI.Button(
                        new Rect(backgroundControl.screen_width / 2 - 52.5f, backgroundControl.screen_height - 55, 50,
                            50), "SCL -")) scaleAgents.ScaleDown();

                    if (GUI.Button(new Rect(5, backgroundControl.screen_height - 55, 50, 50), "BACK"))
                        state = State.Main;
                    break;
            }

            if (GUI.Button(new Rect(backgroundControl.screen_width - 55, backgroundControl.screen_height - 60, 50, 50),
                "RUN")) cameraControl.RunSim();
            if (GUI.Button(new Rect(backgroundControl.screen_width - 110, backgroundControl.screen_height - 60, 50, 50),
                "SAVE")) saveOrLoad.Save();
            if (GUI.Button(new Rect(backgroundControl.screen_width - 165, backgroundControl.screen_height - 60, 50, 50),
                "LOAD")) saveOrLoad.Load();
        }
    }

    private enum State
    {
        Main,
        Move_Camera,
        Move_Background,
        Resize_characters
    }
}