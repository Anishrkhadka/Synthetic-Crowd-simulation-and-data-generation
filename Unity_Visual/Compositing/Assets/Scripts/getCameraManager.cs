using UnityEngine;

public class getCameraManager : MonoBehaviour
{
//	public Materials materialManager;
    // public Camera_Control cameraControl;

//    private readonly Sprite[] backgroungImageListFor2DCamera = new Sprite [2];

    private readonly float camera2DBackgroundScaleAmount = 0.1f;
    private Sprite backgroundImageFor2DCamera;
//    public Vector3 camera2DCurrentScale;
    public float camera3DFieldOfView = 1;

    public float camera3DMovementAmount = 1;
    public float camera3DRotationAmount = 1;

    public int maxNumberOfCameraFrames;

    private int screenHeight;
    private int screenWidth;

    private getSettingManager settingManager;
    private getBackgroundManager backgroundManager;

    public void loadSettings()
    {
        // -- Get the Load getSettingManager script from Setting Manager Game Object -- // 
        settingManager = GameObject.FindGameObjectWithTag("settingManager").GetComponent<getSettingManager>();
        backgroundManager = GameObject.FindGameObjectWithTag("backgroundManager").GetComponent<getBackgroundManager>();

//        getBackgroundImageForCamera2D();
        setBackgroundImageToDefault();

        screenHeight = getBackgroundHeight();
        screenWidth = getBackgroundWidth();

        maxNumberOfCameraFrames = settingManager.getTotalNoOfSimulatedFrameForAvatar();
    }

//    private void getBackgroundImageForCamera2D()
//    {
//        backgroungImageListFor2DCamera[0] = backgroundManager.getDefaultBackgroundImage();
//        backgroungImageListFor2DCamera[1] = backgroundManager.getBackgroundImageForGT();
//
//    }


    public void setBackgroundImageToDefault()
    {
        backgroundImageFor2DCamera = backgroundManager.getDefaultBackgroundImage();
    }


//	 -- Call from Main -- // 
    public void setBackgroundImageToGroundTruth()
    {
        backgroundImageFor2DCamera =  backgroundManager.getBackgroundImageForGT() ;
    }


    public Vector3 getCamera3DPosition()
    {
        return settingManager.getCamera3DPosition();
    }

    public Vector3 getCamera3DRotation()
    {
        return settingManager.getCamera3DRotation();
    }

    public float getCameraFOVFromSettingsFile()
    {
        return settingManager.getCameraFOV();
    }

    public Vector3 getCamera2DBackgroundScale(bool IsGetCurrentScale=false)
    {
        if (IsGetCurrentScale)
        {
            return GameObject.FindGameObjectWithTag("camera2DBackground").GetComponent<Transform>().localScale;
        }
        var scale = settingManager.getCamera2DBackgroundScale();
        return new Vector3(scale, scale, 0);

    }



    public Sprite getBackgroundImageFor2DCamera()
    {
        return backgroundImageFor2DCamera;
    }


    public int getBackgroundWidth()
    {
        return backgroundImageFor2DCamera.texture.width;
    }

    public int getBackgroundHeight()
    {
        return backgroundImageFor2DCamera.texture.height;
    }

    public float getCamera2DBackgroundScaleAmount()
    {
        return camera2DBackgroundScaleAmount;
    }


    public float getcamera3DMovementAmount()
    {
        return camera3DMovementAmount;
    }

    public float getcamera3DRotationAmount()
    {
        return camera3DRotationAmount;
    }

    public float getcamera3DFieldOfView()
    {
        return camera3DFieldOfView;
    }


//    public void setCamera2DCurrentScale(Vector3 InCurrentScale)
//    {
//        camera2DCurrentScale = InCurrentScale;
//    }


    public int getMaxCameraFrame()
    {
        return maxNumberOfCameraFrames;
    }
}