using UnityEngine;

public class getMaterialManager : MonoBehaviour
{
    public Material flatMatrial;
    public Material transparentFloorWithShadow;
    
    private bool IsFlatShader;


    public void setIsGroundTruth(bool InIsGroundTruth)
    {
        IsFlatShader = InIsGroundTruth;
    }

    public bool getIsGroundTruth()
    {
        return IsFlatShader;
    }

    public Material getFlatMaterial()
    {
        return flatMatrial;
    }

    public Material getTransparentShaderWithShadowMaterial()
    {
        return transparentFloorWithShadow;
    }

    
    public Color[] getListOfColor(int InTotalNoOfColor, int InScaleBy)
    {
        // -- Create the list of total colour --// 
        var totalColor = new Color[InTotalNoOfColor * InScaleBy];

        var min = 10;
        var max = InTotalNoOfColor * InScaleBy - 10;

        var counter = 0;
        for (var i = min; i < max; i++)
        {
            totalColor[counter] = new Color((float) i / max, (float) i / max, (float) i / max, 1);
            totalColor[counter] += Random.ColorHSV(0f, 1f, 0.5f, 1f, 1f, 0f);
            
            // For GAN --//
//            totalColor[counter] = new Color(255,0,0);
     

            counter++;
        }


        return totalColor;
    }
}