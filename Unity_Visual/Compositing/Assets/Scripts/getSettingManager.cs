using System.IO;
using UnityEngine;

public class getSettingManager : MonoBehaviour
{
    private getAvatarManager avatars;
    private getCameraManager cameraManager;
    private Camera3D camera3D;
    private getLightManager lightManager;


    private float camera2DBackgroundScale;

    //-- Variables to load save.txt --- // 
    private Vector3 camera3DPosition = Vector3.zero;
    private Vector3 camera3DRotation = Vector3.zero;
    private float cameraFOV;


    private float animationSpeed;
    private Vector3 avatarPosition = Vector3.zero;
    private float avatarScaleSize;
    private int totalNoOfAgents;
    private string filePathToUnityEnvSettings;
    private float mapUnitSize;
    private string simulationName;
    private string simulationFolderName;
    private readonly bool resizeFloor = true;
    private float ratioXForResizingFloor;


    private int totalNoOfSimulatedFrameForAgents;
    private Vector3[] lightTransformList;

    public void loadDependency()
    {
        avatars = GameObject.FindGameObjectWithTag("agentManager").GetComponentInChildren<getAvatarManager>();
        cameraManager = GameObject.FindGameObjectWithTag("cameraManager").GetComponent<getCameraManager>();
        camera3D = GameObject.FindGameObjectWithTag("cameraManager").GetComponentInChildren<Camera3D>();
        lightManager = GameObject.FindGameObjectWithTag("lightManager").GetComponentInChildren<getLightManager>();
    }

    public void setPathToUnityEnvSaveSettings(string InPath)
    {
        filePathToUnityEnvSettings = InPath;
    }

    // -- readSettingsFromFiles is ran from Main --// 
    public bool loadSimulationSettingsFromFile(string InPathToSimulationSettingsFile)
    {
        if (getUtilityManager.checkIfFileExist(InPathToSimulationSettingsFile))
        {
            // -- Path to Trial sets -- // 
            var settingsFiles = new StreamReader(File.OpenRead(InPathToSimulationSettingsFile));

            // -- Read each line at a time and set the value -- //
            int.TryParse(settingsFiles.ReadLine(), out totalNoOfSimulatedFrameForAgents);
            int.TryParse(settingsFiles.ReadLine(), out totalNoOfAgents);
            float.TryParse(settingsFiles.ReadLine(), out ratioXForResizingFloor);
            float.TryParse(settingsFiles.ReadLine(), out mapUnitSize);

            // -- read the cameraManager settings from the files and set in -- //
            simulationFolderName = settingsFiles.ReadLine();
            simulationName = settingsFiles.ReadLine();
            // -- Close the files -- // 
            settingsFiles.Dispose();
            settingsFiles.Close();

            return true;
        }

        print("Can't Find " + InPathToSimulationSettingsFile);
        return false;
    }

    public bool loadUnityEnvSettingsFromFile()
    {
        if (getUtilityManager.checkIfFileExist(filePathToUnityEnvSettings))
        {
            var fileRead = new StreamReader(File.OpenRead(filePathToUnityEnvSettings));

            float.TryParse(fileRead.ReadLine(), out camera3DPosition.x);
            float.TryParse(fileRead.ReadLine(), out camera3DPosition.y);
            float.TryParse(fileRead.ReadLine(), out camera3DPosition.z);

            float.TryParse(fileRead.ReadLine(), out camera3DRotation.x);
            float.TryParse(fileRead.ReadLine(), out camera3DRotation.y);
            float.TryParse(fileRead.ReadLine(), out camera3DRotation.z);
            float.TryParse(fileRead.ReadLine(), out cameraFOV);

            float.TryParse(fileRead.ReadLine(), out camera2DBackgroundScale);

            float.TryParse(fileRead.ReadLine(), out avatarScaleSize);

            float.TryParse(fileRead.ReadLine(), out avatarPosition.x);
            float.TryParse(fileRead.ReadLine(), out avatarPosition.y);
            float.TryParse(fileRead.ReadLine(), out avatarPosition.z);

            float.TryParse(fileRead.ReadLine(), out animationSpeed);

            // -- read the cameraManager settings from the files and set in -- //
//            simulationFolderName = fileRead.ReadLine();
//            simulationName = fileRead.ReadLine();

            try
            {
                lightTransformList = new Vector3[5];
                for (var i = 0; i < 5; i++)
                {
                    var line = fileRead.ReadLine();
                    var value = line.Split('\t');

                    lightTransformList[i] = new Vector3(float.Parse(value[0]),float.Parse(value[1]),float.Parse(value[2]));
                }
            }
            catch
            {
                // ignored
            }


            // -- Close the files -- // 
            fileRead.Dispose();
            fileRead.Close();

            return true;
        }

        print("Can't Find " + filePathToUnityEnvSettings);
        return false;
    }

    // -- Save the file to the given file [i.e save.txt]-- // 
    public bool saveUnityEnvSettingToFile()
    {
        var writeInFile = new StreamWriter(filePathToUnityEnvSettings, false);

        // -- Get the Camera 3D current Position -- // 
        var cameraPosition = camera3D.getPosition();
        var line = cameraPosition.x.ToString();
        writeInFile.WriteLine(line);
        line = cameraPosition.y.ToString();
        writeInFile.WriteLine(line);
        line = cameraPosition.z.ToString();
        writeInFile.WriteLine(line);

        // -- Get the Camera 3D euler angles -- // 
        var camera3DEulerAngles = camera3D.getEulerAngles();
        line = camera3DEulerAngles.x.ToString();
        writeInFile.WriteLine(line);
        line = camera3DEulerAngles.y.ToString();
        writeInFile.WriteLine(line);
        line = camera3DEulerAngles.z.ToString();
        writeInFile.WriteLine(line);

        // -- Get the Camera 3D field of View -- // 
        line = camera3D.getCameraFov().ToString();
        writeInFile.WriteLine(line);

        // -- Get Camera 2D background scale value (true) will return current local scale --// 
        var currentCameraScaleAmount = cameraManager.getCamera2DBackgroundScale(true);
        line = currentCameraScaleAmount.x.ToString();
        writeInFile.WriteLine(line);

        // -- get Scale of Avatar used for initial scale purpose --// 
        var avatarsScaleAmount = avatars.getAvatarScaleAmount();

        line = avatarsScaleAmount.x.ToString();
        writeInFile.WriteLine(line);

        // -- Get the current Avatar Manager position -- // 
        var avatarsForScalePosition = avatars.getPositionOfScaleAvatars();

        line = avatarsForScalePosition.x.ToString();
        writeInFile.WriteLine(line);
        line = avatarsForScalePosition.y.ToString();
        writeInFile.WriteLine(line);
        line = avatarsForScalePosition.z.ToString();
        writeInFile.WriteLine(line);

        // -- Get the Character Animation Speed -- // 
        line = avatars.getAnimationSpeed().ToString();
        writeInFile.WriteLine(line);

        // -- Get the Screenshot prefix -- // 
//        line = getSimulationFolderName();
//        writeInFile.WriteLine(line);
//        line = getSimulationName();
//        writeInFile.WriteLine(line);

        // -- Get the current Avatar Manager position -- // 
        var lightTransformList = lightManager.getLightTransformList();
        for (var i = 0; i < 5; i++)
        {
            line = lightTransformList[i].x + "\t" +
                   lightTransformList[i].y + "\t" +
                   lightTransformList[i].z;

            writeInFile.WriteLine(line);
        }


        writeInFile.Close();


        if (getUtilityManager.checkIfFileExist(filePathToUnityEnvSettings))
        {
            print("Saved");
            return true;
        }

        print("Can't Save " + filePathToUnityEnvSettings);
        return false;
    }


    public Vector3[] getLightRotation()
    {
        return lightTransformList;
    }

    public Vector3 getCamera3DPosition()
    {
        return camera3DPosition;
    }

    public Vector3 getCamera3DRotation()
    {
        return camera3DRotation;
    }


    public float getCameraFOV()
    {
        return cameraFOV;
    }

    public float getCamera2DBackgroundScale()
    {
        return camera2DBackgroundScale;
    }

    public Vector3 getAvatarPosition()
    {
        return avatarPosition;
    }

    public float getAvatarScaleSize()
    {
        return avatarScaleSize;
    }

    public float getAnimationSpeed()
    {
        return animationSpeed;
    }


    public string getSimulationName()
    {
        return simulationName;
    }

    public string getSimulationFolderName()
    {
        return simulationFolderName;
    }


    public int getTotalNoOfSimulatedFrameForAvatar()
    {
        return totalNoOfSimulatedFrameForAgents;
    }


    public float getRatioXForResizingFloor()
    {
//        if (!resizeFloor) return ratioXForResizingFloor;
        return ratioXForResizingFloor;
    }


    public int getTotalNoOfAvatar()
    {
        return totalNoOfAgents;
    }

    public float getMapUnitSize()
    {
        return mapUnitSize;
    }
}