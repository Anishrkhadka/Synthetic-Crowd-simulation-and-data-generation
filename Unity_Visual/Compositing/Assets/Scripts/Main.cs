using UnityEditor;
using UnityEngine;
using UnityEngine.Serialization;

public class Main : MonoBehaviour
{
    private readonly string pathToAvatarIDAndRadius = "Assets/Data/SimulationResult/AgentIDAndRadius.txt";
    private readonly string pathToAvatarPosition = "Assets/Data/SimulationResult/AgentPosition.txt";
    private readonly string pathToAvatarRotation = "Assets/Data/SimulationResult/AgentRotation.txt";
    private readonly string pathToSimulationSettingFile = "Assets/Data/SimulationResult/SimulationSetting.txt";
    private string pathToUnityEnvSaveSettings;

    private string pathToGroundTruthFolder;
    private string pathToOriginalFolder;
    private string pathToDepthMapFolder;
    private string pathToJsonMapFolder;
    
    private getSettingManager settingManager;
    private getAvatarManager avatarsManager;
    private getFloorManager floorManager;
    private getCameraManager cameraManager;
    private getGUIManager guiManager;
    private getCameraDepth cameraDepth;
    private Camera2D camera2D;
    private Camera3D camera3D;
    private getBackgroundManager backgroundManager;
    private getLightManager lightManager;
    private getMaterialManager materialManager;
    private getGameLoopManager gameLoopManager;


    private const int timeDelayBy = 60;
    private const bool timeDelayForScreenCapture = false;
    private int count;
    private int frameCounter;

    public bool IsScreenShot;
    public bool IsSaveJoint;
    public bool IsDepthCamera;
    


    private int totalNoOfSimulatedFrameForAvatar;
    
    private void Awake()
    {
      
        init();
        load();
 
    }

    private void init()
    {
        // -- Get the Load getSettingManager script from Setting Manager Game Object -- // 
        settingManager = GameObject.FindGameObjectWithTag("settingManager").GetComponent<getSettingManager>();
        avatarsManager = GameObject.FindGameObjectWithTag("agentManager").GetComponentInChildren<getAvatarManager>();

        floorManager = GameObject.FindGameObjectWithTag("floorManager").GetComponent<getFloorManager>();
        
        backgroundManager = GameObject.FindGameObjectWithTag("backgroundManager").GetComponent<getBackgroundManager>();
        
        lightManager = GameObject.FindGameObjectWithTag("lightManager").GetComponentInChildren<getLightManager>();
        
        cameraManager = GameObject.FindGameObjectWithTag("cameraManager").GetComponent<getCameraManager>();
        camera2D = GameObject.FindGameObjectWithTag("cameraManager").GetComponentInChildren<Camera2D>();
        camera3D = GameObject.FindGameObjectWithTag("cameraManager").GetComponentInChildren<Camera3D>();
        cameraDepth = camera3D.GetComponent<getCameraDepth>();
        cameraDepth.enabled = false;

        guiManager = GameObject.FindGameObjectWithTag("guiManager").GetComponentInChildren<getGUIManager>();
        guiManager.enabled = false;

        materialManager = GameObject.FindGameObjectWithTag("materialManager").GetComponent<getMaterialManager>();

        // -- Game Loop is attache the Manager --// 		
        gameLoopManager = GetComponent<getGameLoopManager>();

       
    }
    
    private void load()
    {
        
        // -- [Note] -- ordering of the function matter -- // 
        loadBackgroundImage();
       
        
        loadSettings();
        loadFloor();
        loadAvatars();
  
        loadCamera();
        loadShaders();
        loadGameLoop();
      
        loadGUI();
        loadSettingsDependency();
        loadLight();
       
        pathToOriginalFolder = "Result/" + settingManager.getSimulationFolderName() + "/Ori";
        pathToGroundTruthFolder= "Result/" + settingManager.getSimulationFolderName() + "/GT";
        pathToDepthMapFolder= "Result/" + settingManager.getSimulationFolderName() + "/depth";
        pathToJsonMapFolder= "Result/" + settingManager.getSimulationFolderName() + "/joint";
        
        
        getUtilityManager.createDirectory( pathToOriginalFolder);
        getUtilityManager.createDirectory( pathToGroundTruthFolder);
        getUtilityManager.createDirectory(pathToDepthMapFolder);
        getUtilityManager.createDirectory(pathToJsonMapFolder);

        checkTimeForScreenCapture();
        
        
    }

    private void loadBackgroundImage()
    {
        backgroundManager.init();
    }
    
    private void loadLight()
    {
        lightManager.init();
    }
    
    private void loadSettings()
    {
        settingManager.loadSimulationSettingsFromFile(pathToSimulationSettingFile);
        pathToUnityEnvSaveSettings = "Assets/Data/SimulationResult/Save_"+settingManager.getSimulationName()+".txt";
        settingManager.setPathToUnityEnvSaveSettings(pathToUnityEnvSaveSettings);
        settingManager.loadUnityEnvSettingsFromFile();
    }

    private void loadFloor()
    {
        floorManager.init();
        floorManager.create();
    }

    private void loadAvatars()
    {
        avatarsManager.init();

        avatarsManager.getAvatarPositionAndRotationFromFiles(pathToAvatarPosition, pathToAvatarRotation);
        avatarsManager.getAvatarIdAndRadiusFromFile(pathToAvatarIDAndRadius);

        avatarsManager.getTheAvatarsForScaling();
        avatarsManager.createClone();
        avatarsManager.initAvatarMovement();
    }

    private void loadShaders()
    {
        // -- First store the default material from avatars -- // 
        avatarsManager.getOriginalAvatarShader();
        avatarsManager.getFlatAvatarShader();
    }

    private void loadCamera()
    {
       
        cameraManager.loadSettings();
        camera2D.init();
        camera3D.init();
    }

   
    // -- Auto load by Unity -- // 
    private void loadGUI()
    {
        guiManager.enabled = true;
        guiManager.init();
    }

    private void loadGameLoop()
    {
        gameLoopManager.init();
    }

    private void pauseGame(bool InIsGamePause, int InFrameCounter)
    {
        if (InIsGamePause)
        {
            Time.timeScale = 0f;
            gameLoopManager.startLoop(false, InFrameCounter);
        }
        else
        {
            Time.timeScale = 1f;
            gameLoopManager.startLoop(true, InFrameCounter);
        }
    }

    private bool setGroundTruthMaterialToAvatar()
    {
        // -- Change the material to flat --//
        avatarsManager.setFlatAvatarShader();
        // -- Also set the material manager option  --// 
        materialManager.setIsGroundTruth(true);

        setCameraBackgroundForGroundTruth(true);

        setDefaultCamera();
     
        if (IsScreenShot)
            return getUtilityManager.TakeScreenshot(pathToGroundTruthFolder, gameLoopManager.getCurrentFrameNumber());

        return false;
    }

    private bool setDefaultMaterialToAvatar()
    {
        // -- First get the default material from avatars -- // 
        // -- Change the material to flat --//
        avatarsManager.setOriginalAvatarShader();
        // -- Also set the material manager option  --// 
        materialManager.setIsGroundTruth(false);
        // -- Change the 2D image background --//
        setCameraBackgroundForGroundTruth(false);
        
        lightManager.setLightForBackground();
        // -- Take a screenshot [returns false if failed to createClone file ] -- // 
        if (IsScreenShot)
            return getUtilityManager.TakeScreenshot(pathToOriginalFolder, gameLoopManager.getCurrentFrameNumber());


        return false;
    }

    private void setCameraBackgroundForGroundTruth(bool InIsGroundTruthBackground)
    {
        if (InIsGroundTruthBackground)
        {
            cameraManager.setBackgroundImageToGroundTruth();
            // -- reset the new background --// 
            camera2D.setBackground(true);
        }
        else
        {
            floorManager.setDisplayFloor(true);
            cameraManager.setBackgroundImageToDefault();
            // -- reset the new background --// 
            camera2D.setBackground();
        }
    }

    private bool getCameraDepth()
    {
        //-- Enable depth script -- //
        cameraDepth.enabled = true;
        // -- Hide floor --//
        floorManager.setDisplayFloor(false);
        // -- Take screen shot --// 
        if (IsDepthCamera)
            return getUtilityManager.TakeScreenshot(pathToDepthMapFolder, gameLoopManager.getCurrentFrameNumber());

        return false;
    }

    private bool setDefaultCamera()
    {
        if (cameraDepth.enabled)
        {
            cameraDepth.enabled = false;
            return true;
        }

        return false;
    }

    private void checkTimeForScreenCapture()
    {
        // --  Assigned in Editor -- // 
        if (timeDelayForScreenCapture) Time.captureFramerate = timeDelayBy;
    }

    private void loadSettingsDependency()
    {
        settingManager.loadDependency();
        totalNoOfSimulatedFrameForAvatar = settingManager.getTotalNoOfSimulatedFrameForAvatar();
        
    }

    private bool getJoint()
    {    
        if(IsSaveJoint)
            return avatarsManager.saveJointInfoToFile(pathToJsonMapFolder, gameLoopManager.getCurrentFrameNumber());
        
        return false;
    }

    
    // -- Unity Game Engine Loop -- / 
    private void Update()
    {
        if (frameCounter < totalNoOfSimulatedFrameForAvatar)
        {
            // -- Run function in game change Pause the Game = true  -- // 
            if (!gameLoopManager.getIsGamePause()) return;
            pauseGame(true, frameCounter);

            // -- Only increment the frame once the Screen shot is complete -- // 
//            if (!setGroundTruthMaterialToAvatar()|| !getJoint() || !setDefaultMaterialToAvatar() ||
//                !getCameraDepth()) return;
//            
            if (!setGroundTruthMaterialToAvatar()|| !getJoint() || !setDefaultMaterialToAvatar() ) return;
            
            // For GAN --//
//            if (!setGroundTruthMaterialToAvatar()|| !getJoint()) return;
            
            // resume from the same frameCounter -- // 
            pauseGame(false, frameCounter);
            frameCounter++;
        }
        else
        {
            gameLoopManager.showAvatars(false, true);
            gameLoopManager.setIsGamePause(true);
            unityEditorHelper.Quit();
    
        }
    }
}