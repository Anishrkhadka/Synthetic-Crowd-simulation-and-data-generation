using System.IO;
using UnityEngine;

public class Screenshots : MonoBehaviour
{
    private bool IsScreenShots;

    private Camera mycamera;
    private string screenShotName;

    private void Awake()
    {
        mycamera = gameObject.GetComponent<Camera>();
    }


    private void OnPostRender()
    {
        if (IsScreenShots)
        {
            IsScreenShots = false;

            var renderTextureForMyCamera = mycamera.targetTexture;

            var renderToThisTexture = new Texture2D(renderTextureForMyCamera.width, renderTextureForMyCamera.height,
                TextureFormat.ARGB32, false);
            var rect = new Rect(0, 0, renderTextureForMyCamera.width, renderTextureForMyCamera.height);
            renderToThisTexture.ReadPixels(rect, 0, 0);

            var saveToPngFile = renderToThisTexture.EncodeToPNG();
            File.WriteAllBytes(screenShotName, saveToPngFile);

            RenderTexture.ReleaseTemporary(renderTextureForMyCamera);
            mycamera.targetTexture = null;
        }
    }


    public void TakeScreenShot(int InWidth, int InHeight, string InScreenshortPrefix, int InFrameNumber)
    {
        mycamera.targetTexture = RenderTexture.GetTemporary(InWidth, InHeight, 16);
        IsScreenShots = true;

        screenShotName = InScreenshortPrefix + "/" + InScreenshortPrefix + "_" + InFrameNumber.ToString("0000") +
                         ".png";
    }
}