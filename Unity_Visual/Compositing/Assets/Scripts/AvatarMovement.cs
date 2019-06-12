using System.Runtime.Serialization;
using UnityEngine;
using UnityEngine.Serialization;

// -- Agent Movement Class is attached to indivisual Avatar prefab --// 
public class AvatarMovement : MonoBehaviour
{
    private float AnimationSpeed;
    private Animator animatorThirdPerson;

    public GameObject[] avatarBody;
    public getAvatarManager avatarManager;

    // -- values are set when object are clone by Agents createClone function --//     
    public Vector3[] avatarPositions;
    public float[] avatarRotations;
    private Camera3D camera3D;

//    private Vector3 cameraPosition;
//    public int currentframeNumber = -1;

    public int ID;

    private bool IsCheckAvatarHeight;
    private bool IsHideAvatar;
    public float radius;

//    private getSettingManager settingManager;
    private bool updated;
 
        

    public void init()
    {
        avatarManager = GameObject.FindGameObjectWithTag("agentManager").GetComponentInChildren<getAvatarManager>();
        camera3D = GameObject.FindGameObjectWithTag("cameraManager").GetComponentInChildren<Camera3D>();

        animatorThirdPerson = GetComponent<Animator>();
        AnimationSpeed = avatarManager.getAnimationSpeed();

        IsCheckAvatarHeight = true;
        IsHideAvatar = true;
        updated = false;
    }
    
    
    
    public void loop(int InCurrentFrame)
    {

        if (InCurrentFrame > 1)
        {
            transform.position = avatarPositions[InCurrentFrame];
            var targetPosition = avatarPositions[InCurrentFrame + 1];
            var targetRotation = Quaternion.LookRotation(targetPosition - transform.position);
            
            transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, 100 * Time.deltaTime);


//            transform.position = new Vector3(avatarPositions[InCurrentFrame].x, 0,
////                                             getYPositionForAvatars(), 
//                                             avatarPositions[InCurrentFrame].z);
//            var currentPosition = transform.position;
//            transform.eulerAngles = new Vector3(0, avatarRotations[InCurrentFrame], 0);
//            transform.LookAt(new Vector3(avatarPositions[InCurrentFrame + 1].x, 0,
//                avatarPositions[InCurrentFrame + 1].z));

//            var targetPosition = new Vector3(avatarPositions[InCurrentFrame + 1].x, 0,
//                avatarPositions[InCurrentFrame + 1].z);


//            checkIfAvatarsVisible();

            // --- Move the avatarDummy -- // 
            moveAvatar(InCurrentFrame);
        }

        else
        {
            transform.position = new Vector3(-1000, 0, -1000);
        }
    }

    private float getYPositionForAvatars()
    {
        var offset = transform.position;
        var ray = new Ray(offset, transform.position + Vector3.down * 300);
        var ray2 = new Ray(offset, transform.position + Vector3.up * 300);

        var hit = new RaycastHit();

        if (Physics.Raycast(ray, out hit))
        {
            if (hit.collider.tag != "Agent") return hit.point.y + 0.05f;

            return transform.position.y;
        }

        if (!Physics.Raycast(ray2, out hit)) return transform.position.y;
        if (hit.collider.tag != "Agent")
            return hit.point.y + 0.05f;
        return transform.position.y;

    }

    private void checkIfAvatarsVisible()
    {
        // -- Make sure the Avatars are in default layer = 0 -- // 
        foreach (var body in avatarBody) body.layer = 0;

        var offPos = new Vector3(transform.position.x, 1, transform.position.z);
        var direction = camera3D.getPosition() - offPos;


        var ray = new Ray(offPos, direction);
        var hit = new RaycastHit();


        if (!Physics.Raycast(ray, out hit)) return;
        {
            if (!hit.transform.CompareTag("Obstacle")) return;
            foreach (var body in avatarBody)
                body.layer = 1;
        }
    }


    private void moveAvatar(int currentFrameNumber)
    {
        var velocity = 0.5f;

        if (currentFrameNumber > 0)
            velocity = Vector3.Magnitude(avatarPositions[currentFrameNumber] -
                                                avatarPositions[currentFrameNumber - 1]) * AnimationSpeed;
        
    
        // -- Move avatarDummy - Animation controller -- // 
        animatorThirdPerson.SetFloat("Forward", velocity, 0.1f, Time.deltaTime);
    }


    public void setAvatarPosition( Vector3[] InPosition)
    {
        avatarPositions = InPosition;
    }

    public void setAvatarRotation(float[] InRotation)
    {
        avatarRotations = InRotation;

    }
    // -- Called from Avatars scale function --// 
    public float getAvatarRadius()
    {
        return radius;
    }

    public bool getUpdate()
    {
        return updated;
    }
}