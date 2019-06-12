using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

public class getGUIManager : MonoBehaviour
{
    private readonly int buttonSize = 20;
    private readonly int buttonWidth = 80;
    private readonly int buttonHeight = 40;
    private getAvatarManager avatar;

    private Camera2D camera2D;
    private Camera3D camera3D;
    private getCameraManager cameraManager;
    private getGameLoopManager gameLoop;
    private getLightManager lightManager;
    private int screenHeight;

    private string simulationName = "RECORDING_NAME";
    private int screenWidth;

    private getSettingManager settingManager;
    private getBackgroundManager backgroundManager;

    private State state;


    public void init()
    {
        state = State.Main;

        settingManager = GameObject.FindGameObjectWithTag("settingManager").GetComponent<getSettingManager>();
        cameraManager = GameObject.FindGameObjectWithTag("cameraManager").GetComponent<getCameraManager>();
        camera3D = GameObject.FindGameObjectWithTag("cameraManager").GetComponentInChildren<Camera3D>();
        camera2D = GameObject.FindGameObjectWithTag("cameraManager").GetComponentInChildren<Camera2D>();
        gameLoop = GameObject.FindGameObjectWithTag("manager").GetComponentInChildren<getGameLoopManager>();
        avatar = GameObject.FindGameObjectWithTag("agentManager").GetComponentInChildren<getAvatarManager>();
        lightManager = GameObject.FindGameObjectWithTag("lightManager").GetComponentInChildren<getLightManager>();
        backgroundManager = GameObject.FindGameObjectWithTag("backgroundManager").GetComponent<getBackgroundManager>();
        
        screenWidth = Screen.width;
        screenHeight = Screen.height;
    }


    private void OnGUI()
    {
        screenWidth = Screen.width;
        screenHeight = Screen.height;

        if (gameLoop.getIsLoopRunning()) return;
        switch (state)
        {
            case State.Main:
                if (button(getScreenPosX(buttonSize), getScreenPosY(screenHeight / 2 - (buttonHeight * 3 + buttonSize * 3)), "BGRD")) state = State.MoveBackground;
                if (button(getScreenPosX(buttonSize),getScreenPosY(screenHeight / 2 - (buttonHeight * 2 + buttonSize * 2)), "CAM")) state = State.MoveCamera;
                if (button(getScreenPosX(buttonSize), getScreenPosY(screenHeight / 2 - (buttonHeight + buttonSize)), "CHAR")) state = State.ResizeAvatars;
                   
                simulationName=  GUI.TextField( new Rect(getScreenPosX(screenWidth/2), getScreenPosY(buttonSize), 150, 20), settingManager.getSimulationName() , 50);

                break;

            case State.MoveBackground:
                if (button (getScreenPosX(buttonWidth + buttonSize), getScreenPosY(screenHeight / 2 - (buttonHeight * 3 + buttonSize * 3)), "ZOOM +")) camera2D.ScaleUp();
                if (button (getScreenPosX(buttonWidth * 2 + buttonSize * 2), getScreenPosY(screenHeight / 2 - (buttonHeight * 3 + buttonSize * 3)), "ZOOM -")) camera2D.ScaleDown();
                if (button(getScreenPosX(buttonSize), getScreenPosY(screenHeight - 60), "BACK")) state = State.Main;
                
                if (button (getScreenPosX(buttonWidth * 2 + buttonSize * 2), getScreenPosY(screenHeight / 2 - (buttonHeight * 5 + buttonSize * 3)), "Fix Background"))
                    // -- cycle the value true or false -- // 
                    backgroundManager.setISFixBackground(!backgroundManager.getIsFixBackground());

                break;

            case State.MoveCamera:
                if (button (getScreenPosX(buttonWidth * 2 + buttonSize), getScreenPosY(buttonHeight + buttonSize) , "FRD"))  camera3D.ZUp();
                if (button(getScreenPosX(buttonWidth * 2 + buttonSize),  getScreenPosY(buttonHeight * 4 + buttonSize * 4) ,"BCK")) camera3D.ZDown();
                if (button (getScreenPosX(buttonWidth + buttonSize), getScreenPosY(buttonHeight * 2 + buttonSize * 2), "LFR")) camera3D.XDown();
                if (button (getScreenPosX(buttonWidth * 3 + buttonSize), getScreenPosY(buttonHeight * 2 + buttonSize * 2) ,"RGT")) camera3D.XUp();

                if (button (getScreenPosX(buttonWidth + buttonSize), getScreenPosY(buttonHeight * 3 + buttonSize * 3),"UP")) camera3D.YDown();
                if (button (getScreenPosX(buttonWidth * 3 + buttonSize),getScreenPosY(buttonHeight * 3 + buttonSize * 3) ,"DWN")) camera3D.YUp();

                if (button(getScreenPosX(buttonWidth + buttonSize),getScreenPosY(buttonHeight * 8 + buttonSize),"FOV +")) camera3D.FOVUp();
                if (button(getScreenPosX(buttonWidth * 3 + buttonSize),getScreenPosY(buttonHeight * 8 + buttonSize),"FOV -")) camera3D.FOVDown();

                if (button(getScreenPosX(buttonWidth * 7 + buttonSize),getScreenPosY(buttonHeight + buttonSize), "PCH +")) camera3D.XRotDown();
                if (button(getScreenPosX(buttonWidth * 7 + buttonSize),getScreenPosY(buttonHeight * 4 + buttonSize * 4),"PCH -")) camera3D.XRotUp();
                if (button(getScreenPosX(buttonWidth * 6 + buttonSize), getScreenPosY(buttonHeight * 2 + buttonSize * 2),"YAW -")) camera3D.YRotDown();
                if (button (getScreenPosX(buttonWidth * 8 + buttonSize),getScreenPosY(buttonHeight * 2 + buttonSize * 2),"YAW +")) camera3D.YRotUp();
                if (button(getScreenPosX(buttonWidth * 6 + buttonSize),getScreenPosY(buttonHeight * 3 + buttonSize * 3), "ROLL -")) camera3D.ZRotDown();
                if (button (getScreenPosX(buttonWidth * 8 + buttonSize), getScreenPosY(buttonHeight * 3 + buttonSize * 3),"ROLL +")) camera3D.ZRotUp();

                if (button(getScreenPosX(buttonSize), getScreenPosY(screenHeight - 60), "BACK")) state = State.Main;
                break;

            case State.ResizeAvatars:
                if (button(getScreenPosX(buttonWidth * 2 + buttonSize),getScreenPosY(buttonHeight + buttonSize) , "FRD")) avatar.ZUp();
                if (button(getScreenPosX(buttonWidth * 2 + buttonSize),getScreenPosY(buttonHeight * 3 + buttonSize * 3),"BCK")) avatar.ZDown();
                if (button(getScreenPosX(buttonWidth + buttonSize), getScreenPosY(buttonHeight * 2 + buttonSize * 2),"LFR")) avatar.XDown();
                if (button(getScreenPosX(buttonWidth * 3 + buttonSize),getScreenPosY(buttonHeight * 2 + buttonSize * 2),"RGT")) avatar.XUp();
                if (button(getScreenPosX(buttonWidth + buttonSize),getScreenPosY(buttonHeight * 10 + buttonSize),"ANI +")) avatar.AnimationSpeedUp();
                if (button(getScreenPosX(buttonWidth * 3 + buttonSize),getScreenPosY(buttonHeight * 10 + buttonSize),"ANI -")) avatar.AnimationSpeedDown();
                // GUI.TextArea( (camera2D.getScreenWidth() - 110, 5, 50, 50), camera3D.animation_speed.ToString());

                if (button (getScreenPosX(buttonWidth + buttonSize), getScreenPosY(buttonHeight * 8 + buttonSize),"SCL +")) avatar.ScaleUp();
                if (button(getScreenPosX(buttonWidth * 3 + buttonSize), getScreenPosY(buttonHeight * 8 + buttonSize),"SCL -")) avatar.ScaleDown();

                if (button(getScreenPosX(buttonSize), getScreenPosY(screenHeight - 60), "BACK")) state = State.Main;
                break;
        }


        if (button( getScreenPosX(screenWidth - (buttonWidth * 2 + buttonSize * 1)),
                    getScreenPosY(screenHeight - buttonSize * 3), "RUN"))
        {
            gameLoop.showAvatars(true, false);
            gameLoop.setIsGamePause(true);
        }

        if (button(getScreenPosX(screenWidth - (buttonWidth * 3 + buttonSize * 2)),
            getScreenPosY(screenHeight - buttonSize * 3),"SAVE"))
        {
            if (settingManager.saveUnityEnvSettingToFile())
            {
                print("Saved");
            }
        }
                
        if (button(getScreenPosX(screenWidth - (buttonWidth * 4 + buttonSize * 3)),  
            getScreenPosY(screenHeight - buttonSize * 3), "LOAD"))
        {
            if (settingManager.loadUnityEnvSettingsFromFile())
                print("Loaded");
        }
        
        if (button( getScreenPosX(screenWidth - (buttonWidth * 8 + buttonSize * 1)),
            getScreenPosY(screenHeight - buttonSize * 3), "Change Background"))
        {
            cameraManager.setBackgroundImageToDefault();
            camera2D.setBackground();
            lightManager.setLightForBackground();
        }
        
        if (button( getScreenPosX(screenWidth - (buttonWidth * 10 + buttonSize * 1)),
            getScreenPosY(screenHeight - buttonSize * 3), "Save Light Position"))
        {
            lightManager.saveLightRotationToList();
        }
    }



    private bool button (int InXPosition, int InYPosition, string InLabel)
    {
        return GUI.Button( new Rect(InXPosition, InYPosition, buttonWidth, buttonHeight), InLabel);

    }
    
    
    

    private int getScreenPosX(int InPosition)
    {
        return screenWidth - (screenWidth - InPosition);
    }

    private int getScreenPosY(int InPosition)
    {
        return screenHeight - (screenHeight - InPosition);
    }

    private enum State
    {
        Main,
        MoveCamera,
        MoveBackground,
        ResizeAvatars
    }

//    private int getButtonWidthInX(int InSizeX)
//    {                
//        return screenWidth - ( screenWidth - (screenWidth - InSizeX)); 
//    }
//    
//    private int getButtonWidthInY(int InSizeY)
//    {
//        return screenHeight- (screenHeight - (screenHeight - InSizeY)); 
//    }
}