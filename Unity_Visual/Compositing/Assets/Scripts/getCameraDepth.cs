using UnityEngine;
 
//[ExecuteInEditMode]
public class getCameraDepth : MonoBehaviour
{
//    [Range(0f, 3f)]
    private float depthLevel = 0.5f;
     
    private Shader _shader;
    private Shader shader
    {
        get { return _shader != null ? _shader : (_shader = Shader.Find("AnishRKhadka/depthShader")); }
    }
 
    private Material _material;
    private Material material
    {
        get
        {
            if (_material == null)
            {
                _material = new Material(shader);
                _material.hideFlags = HideFlags.HideAndDontSave;
            }
            return _material;
        }
    }
 
    private void Start ()
    {

        // turn on depth rendering for the camera so that the shader can access it via _CameraDepthTexture
        GetComponent<Camera>().depthTextureMode = DepthTextureMode.Depth;
    }
     
    private void OnDisable()
    {
        if (_material != null)
            DestroyImmediate(_material);
    }
     
    private void OnRenderImage(RenderTexture src, RenderTexture dest)
    {
        if (shader != null)
        {
            material.SetFloat("_DepthLevel", depthLevel);
            Graphics.Blit(src, dest, material);
        }
        else
        {
            Graphics.Blit(src, dest);
        }
    }
}