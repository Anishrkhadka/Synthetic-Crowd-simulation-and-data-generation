using System.IO;
using UnityEngine;

//using System;
public class getUtilityManager : MonoBehaviour
{
    public static void createDirectory(string InDirectoryName)
    {
        Directory.CreateDirectory(InDirectoryName);
    }

    public static bool TakeScreenshot(string InScreenshortPrefix, int InFrameNumber)
    {
        var name = InScreenshortPrefix + "/" + "_" + InFrameNumber.ToString("0000") + ".png";

        ScreenCapture.CaptureScreenshot(name, 1);

        return File.Exists(name);
    }


    public static bool IsFileExist(string name)
    {
        return File.Exists(name);
    }

    public static bool checkIfFileExist(string InFilePath)
    {
        return File.Exists(InFilePath);
    }


    public static bool writeFileToJson(string InDirFilePath, string InJsonFileName, string InContent)
    {
        var fullPath = InDirFilePath + InJsonFileName;
        File.WriteAllText(fullPath, InContent);

        return checkIfFileExist(fullPath);

    }
    
    public static bool writeFileToTxt(string InDirFilePath, string InJsonFileName, string InContent)
    {

        var fullPath = InDirFilePath + InJsonFileName;
        File.WriteAllText(fullPath, InContent);

        return checkIfFileExist(fullPath);

    }
    
    
    public static bool IsChildWithName(Transform InObject, string InString)
    {
        return InObject.name == InString;
    }

    public static Vector3 getRoundVector3(Vector3 InVector)
    { 
        return new Vector3(Mathf.Round(InVector.x),Mathf.Round(InVector.y),Mathf.Round(InVector.z));
        
    }

  
}