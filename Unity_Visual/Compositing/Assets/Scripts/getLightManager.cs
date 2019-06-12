using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class getLightManager : MonoBehaviour
{
    private getBackgroundManager backgroundManager;
    private getSettingManager settingManager;
    
    public GameObject sunLight;
    private Vector3 [] lightTransformList = new Vector3 [5];

    
    public void init()
    {
              
        backgroundManager = GameObject.FindGameObjectWithTag("backgroundManager").GetComponent<getBackgroundManager>();
        settingManager = GameObject.FindGameObjectWithTag("settingManager").GetComponent<getSettingManager>();
        
        // -- First Try to load sun rotation from the file if not found the set the current rotation for value --//
        try
        {
            setLightTransformList(settingManager.getLightRotation());
            setLightForBackground();
        }
        catch{
            for (var i =0; i<5; i++)
            {
                lightTransformList[i] = sunLight.GetComponent<Transform>().eulerAngles;
            }
        }
        
    }

    public void saveLightRotationToList()
    {
        
        lightTransformList[backgroundManager.getCurrentBackgroundIndex()] = sunLight.transform.eulerAngles;
        
//        print(lightTransformList[backgroundManager.getCurrentBackgroundIndex()]);
//        print("Light Saved: "+backgroundManager.getCurrentBackgroundIndex());
    }


    public Vector3 [] getLightTransformList()
    {
        return lightTransformList;
    }


    private void setLightTransformList(Vector3[] InLightTransformList)
    {
        lightTransformList = InLightTransformList;
    }
   
    // -- Called from GUI --// 
    public void setLightForBackground()
    {
        var index = backgroundManager.getCurrentBackgroundIndex();
        sunLight.transform.eulerAngles = lightTransformList[index];
    }
    
}
