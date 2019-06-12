using UnityEditor;
using UnityEngine;

public class getGameLoopManager : MonoBehaviour
{
    private getAvatarManager avatarManager;
    private getFloorManager floorManager;

    public int frameNumber;

    public bool IsGamePause;

    public bool IsLoopRunning;
    private getSettingManager settingManager;
    
    
    public void init()
    {
        settingManager = GameObject.FindGameObjectWithTag("settingManager").GetComponent<getSettingManager>();
        floorManager   = GameObject.FindGameObjectWithTag("floorManager").GetComponent<getFloorManager>();
        avatarManager  = GameObject.FindGameObjectWithTag("agentManager").GetComponentInChildren<getAvatarManager>();
    }


    public void startLoop(bool InIsLoopRunning, int InFrameNumber)
    {
        if (frameNumber != InFrameNumber)
        {
            frameNumber = InFrameNumber;
            
            if (frameNumber < settingManager.getTotalNoOfSimulatedFrameForAvatar() - 1)
            {
                avatarManager.startAvatarMovement(frameNumber);
            }
            else
            {
                // --- Show Floor and avatar List used for scale ---// 
                floorManager.setDisplayFloor(false);

                // -- Display scale avatarDummy by default --// 
                avatarManager.setIsDisplayScaleAvatar(true);
            }
        }
    }


    // -- Called from GUI -- // 
    public void showAvatars(bool InIsLoopRunning, bool IsDisplay)
    {
        // -- Start the Main loop --//
        IsLoopRunning = InIsLoopRunning;

        frameNumber = 0;

        // -- Set the size of Avatars --// 
        avatarManager.scaleAllAvatars();
        // -- Hide the model used for scaling purpose -- // 
        avatarManager.setIsDisplayScaleAvatar(IsDisplay);
  
        // -- Hide the floorManager --//
        // -- Need to set it to false by Default -- // 
        floorManager.setDisplayFloor(true);
    }

    public bool getIsGamePause()
    {
        return IsGamePause;
    }
    
    public void setIsGamePause(bool InIsGamePause)
    {
        IsGamePause = InIsGamePause;
    }


//	public void StopSim()
//    {
//        IsLoopRunning = false;
//        frameNumber = 0;
//
//	    // -- Display avatarDummy for scaling purpose --// 
//	    avatarManager.setIsDisplayScaleAvatar(true);
//
//	    // -- Hide the floorManager --//
//	    floorManager.setDisplayFloor(true);
//
//	    Time.timeScale = 0f;
//    }


    // -- Is required by GUI-Control ---// 
    public bool getIsLoopRunning()
    {
        return IsLoopRunning;
    }


    // -- Required in Agent Movement -- // 
    public int getCurrentFrameNumber()
    {
        return frameNumber;
    }
}