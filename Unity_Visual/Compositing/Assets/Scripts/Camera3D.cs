using UnityEngine;

public class Camera3D : MonoBehaviour
{
    private const float cameraFOVAmount = 0.5f;
    private const float cameraMovementAmount = 0.5f;
    private const float cameraRotationAmount = 0.5f;

    private getCameraManager cameraManager;


    public void init()
    {
        // -- Get the Load getSettingManager script from Setting Manager Game Object -- // 
        cameraManager = GetComponentInParent<getCameraManager>();

        transform.position = cameraManager.getCamera3DPosition();
        transform.eulerAngles = cameraManager.getCamera3DRotation();

        setCameraFOV(cameraManager.getCameraFOVFromSettingsFile());

    }


    private void setCameraFOV(float InCurrentFOV)
    {
        gameObject.GetComponent<Camera>().fieldOfView = InCurrentFOV;
    }


    public Vector3 getPosition()
    {
        return transform.position;
    }

    public Vector3 getEulerAngles()
    {
        return transform.rotation.eulerAngles;
    }

    public float getCameraFov()
    {
        return gameObject.GetComponent<Camera>().fieldOfView ;
    }

       
//    public bool IsObjectVisibleToCamera(GameObject Object) {
//        Plane[] planes = GeometryUtility.CalculateFrustumPlanes(gameObject.GetComponent<Camera>());
//        
//        return GeometryUtility.TestPlanesAABB(planes , Object.GetComponent<Collider>().bounds);
//    }

    
    // ---------------- Camera Movement ----------------- //
    
    
    public void XUp()
    {
//        var current_pos = transform.position;
        transform.position += new Vector3(cameraMovementAmount, 0, 0);
    }

    public void YUp()
    {
//        var current_pos = transform.position;
        transform.position +=  new Vector3(0, cameraMovementAmount, 0);
    }

    public void ZUp()
    {
        transform.position += new Vector3(0, 0, cameraMovementAmount);
    }

    public void XDown()
    {

        transform.position += new Vector3(-cameraMovementAmount, 0, 0);
    }

    public void YDown()
    {
        transform.position += new Vector3(0, -cameraMovementAmount, 0);
    }

    public void ZDown()
    {

        transform.position += new Vector3(0, 0, -cameraMovementAmount);
    }

    public void XRotUp()
    {

        transform.eulerAngles += new Vector3(cameraRotationAmount, 0, 0);
    }

    public void YRotUp()
    {
        transform.eulerAngles += new Vector3(0, cameraRotationAmount, 0);
    }

    public void ZRotUp()
    {
        transform.eulerAngles += new Vector3(0, 0, cameraRotationAmount);
    }

    public void XRotDown()
    {
        transform.eulerAngles+= new Vector3(-cameraRotationAmount, 0, 0);
    }

    public void YRotDown()
    {

        transform.eulerAngles += new Vector3(0, -cameraRotationAmount, 0);
    }

    public void ZRotDown()
    {

        transform.eulerAngles += new Vector3(0, 0, -cameraRotationAmount);
    }

    public void FOVUp()
    {
        gameObject.GetComponent<Camera>().fieldOfView += cameraFOVAmount;
    }

    public void FOVDown()
    {
        gameObject.GetComponent<Camera>().fieldOfView -= cameraFOVAmount;
    }

    public void SetFOV(float fov)
    {
        gameObject.GetComponent<Camera>().fieldOfView = fov;
    }
}