using UnityEngine;
using UnityEngine.Rendering;

public class getFloorManager : MonoBehaviour
{
    public GameObject entrance_tile;
    public GameObject floor_tile;

    public Texture2D floorImageMap;
    public GameObject floorParent;
    private Transform floorParentTransform;
    public GameObject obstacle_tile;

    private float ratioXForResizingFloor;

    private getSettingManager settingManager;
    private getMaterialManager materialManager;
    
    
    // Temp Variable -- //
    private Transform[] allChildren;
    private MeshRenderer skinnedMeshRenderer;
    private Material tempFlatMaterial;
    
    // --- createFloor is ran from Main --//
    public void init()
    {
        // -- Get the Load getSettingManager script from Setting Manager Game Object -- // 
        settingManager = GameObject.FindGameObjectWithTag("settingManager").GetComponent<getSettingManager>();
        materialManager = GameObject.FindGameObjectWithTag("materialManager").GetComponent<getMaterialManager>();

        // -- set the Ratio X for Resizing the floorManager -- //
        ratioXForResizingFloor = settingManager.getRatioXForResizingFloor();

        // -- Get the transform of Floor parent game object --// 
        floorParentTransform = floorParent.transform;

        //-- Read the map image and createClone the floorManager --// 
        loadFloorImageMapFromFile();
    }

    // -- Load image file "map" to createClone floorManager --//  
    private void loadFloorImageMapFromFile()
    {
        floorImageMap = (Texture2D) Resources.Load("map");
    }


    // -- Reads the map image and place the floorManager accordingly  -- // 
    public void create()
    {
        // Might need to fix this if the map is not square --- // floor won't be created properly if map is not sure
        for (float i = 0; i < floorImageMap.height; i++)
        {
            for (float j = 0; j < floorImageMap.width; j++)
            {
                var temp = floorImageMap.GetPixel((int) i, (int) j);
                if (temp.r >= 1)
                {
                    var instantiate = Instantiate(entrance_tile, new Vector3(i, 1, j), Quaternion.identity);
                    instantiate.transform.parent = floorParent.transform;
                    instantiate.transform.position = new Vector3(0.5f + i, 0, floorImageMap.height - (float) 0.5 - j);
                }
                else if (temp.r <= 0)
                {
//                    var instantiate = Instantiate(obstacle_tile, new Vector3(i, 1, j), Quaternion.identity);
//                    instantiate.transform.parent = floorParent.transform;
//                    instantiate.transform.position = new Vector3(0.5f + i, 0, floorImageMap.height - (float) 0.5 - j);
//                    instantiate.transform.localScale = new Vector3(1, 2, 1);
                }
                else
                {
                    var instantiate = Instantiate(floor_tile, new Vector3(i, 1, j), Quaternion.identity);
                    instantiate.transform.parent = floorParent.transform;
                    instantiate.transform.position = new Vector3(0.5f + i, 0, floorImageMap.height - (float) 0.5 - j);
                }
            }
        }
        floorParent.transform.localScale = new Vector3(1, 1, 1);
        
//        floorParent.transform.localScale = new Vector3(ratioXForResizingFloor, 1, 1);
        // temp fix for positioning avatar on right path --// 
        floorParent.transform.position = new Vector3(-0.32f, 0, -0.5f);
    }

    // -- Display or hide the floorManager -- // 
    public void setDisplayFloor(bool InIsDisplayFloor)
    {
        floorParent.gameObject.SetActive(InIsDisplayFloor);
        setFloorToShadowOnlyShader();    
    }


    private void setFloorToShadowOnlyShader()
    {
        var floorChild = floorParent.GetComponentsInChildren<Transform>();

        foreach (var floor in floorChild)
            if (floor != null)
            {
                // -- Get Transform list for all the child component for each avatarDummy --// 
                allChildren = floor.GetComponentsInChildren<Transform>();

                // --- For each child, createClone a single color and get all the mesh within each child --// 
                foreach (var childMesh in allChildren)
                {
                    // -- Get the list of part of Avatar --// 
                    skinnedMeshRenderer = childMesh.GetComponent<MeshRenderer>();

                    if (skinnedMeshRenderer == null) continue;
                        tempFlatMaterial = Instantiate(materialManager.getTransparentShaderWithShadowMaterial());

                    skinnedMeshRenderer.material = tempFlatMaterial;
                    skinnedMeshRenderer.material.shader = Shader.Find("AnishRKhadka/TransparentShadowCollector");

                }
            }
    }
}