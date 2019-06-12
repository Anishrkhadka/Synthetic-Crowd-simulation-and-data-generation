//using System.Collections;
//using System.Collections.Generic;

using UnityEngine;

//using UnityEngine.Serialization;

public class Camera2D : MonoBehaviour
{
    public Transform backgroundImage;
    private float backgroundImageScaleAmount;
//    private Vector3 camera2DCurrentScale;
    private getCameraManager cameraManager;

    public SpriteRenderer spriteRenderer;


    public void init()
    {
        // -- Get the _cameraManager settings from Main Camera -- //	
        cameraManager = GetComponentInParent<getCameraManager>();
        // -- Get the transform component of background image ---// 
        backgroundImage = gameObject.transform.GetChild(0); // Get the first child // 	
        backgroundImageScaleAmount = cameraManager.getCamera2DBackgroundScaleAmount();
        spriteRenderer = GetComponentInChildren<SpriteRenderer>();

        Screen.SetResolution(cameraManager.getBackgroundWidth(), cameraManager.getBackgroundHeight(), false);
        setBackgroundImageScale(cameraManager.getCamera2DBackgroundScale());

        setBackground();
    }

    private void setBackgroundImageScale(Vector3 InBackgroundImageScale)
    {
        backgroundImage.localScale = InBackgroundImageScale;
    }
    
    public Vector3 getBackgroundImageScale()
    {
        return backgroundImage.localScale ;
    }
    // -- Ran from Main --//
    public void setBackground(bool IsBackgroundGroundTruth = false)
    {
        // -- Get the sprite Render and set the background image as background for 2D _cameraManager -- //
        spriteRenderer.sprite = cameraManager.getBackgroundImageFor2DCamera();
        spriteRenderer.color = IsBackgroundGroundTruth ? Color.black : Color.white;
  
        
        
    }

    public int getScreenWidth()
    {
        return cameraManager.getBackgroundWidth();
    }

    public int getScreenHeight()
    {
        return cameraManager.getBackgroundHeight();
    }


    // -- -------------------------  Camera2D -----------------------------------------// 
    public void ScaleUp()
    {
//        camera2DCurrentScale = backgroundImage.localScale;
        backgroundImage.localScale +=new Vector3(backgroundImageScaleAmount, backgroundImageScaleAmount, 0);

        // -- For visual purpose --//
//        setCamera2DCurrentScaleInCameraSettings();
    }

    public void ScaleDown()
    {
//        camera2DCurrentScale = backgroundImage.localScale;
        backgroundImage.localScale -= new Vector3(backgroundImageScaleAmount, backgroundImageScaleAmount, 0);
    }

    public void SetScale(Vector3 scale)
    {
        backgroundImage.localScale = scale;
        // -- For visual purpose --//
//        setCamera2DCurrentScaleInCameraSettings();
    }

//    public void setCamera2DCurrentScaleInCameraSettings()
//    {
//        cameraManager.setCamera2DCurrentScale(backgroundImage.localScale);
//    }
}