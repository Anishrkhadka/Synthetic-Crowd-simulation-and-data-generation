using System.IO;
using UnityEngine;

public class Read_Data : MonoBehaviour
{
    public GameObject agent;
    public Agent[] agentIDAndRadiusStruct;
    public Camera_Control cameraControl;
    public GameObject entrance_tile;
    public GameObject floor_parent;
    public GameObject floor_tile;

    public Texture2D floorMapImage;
    public float map_unit_size;
    public Material mat1;
    public Material mat2;
    public Material mat3;
    public Material mat4;
    public int num_agents;
    public int num_frames;
    public GameObject obstacle_tile;

    //VARIABLES
    //GET DATA FROM FILE
    public Vector3[][] positions;
    public float ratio_x;
    public bool resize_floor = true;
    public float[][] rotations;
    private StreamReader settingsFiles;
    private StreamReader sr_agents;
    private StreamReader sr_pos;
    private StreamReader sr_rot;

    private void Start()
    {
        cameraControl = GameObject.FindGameObjectWithTag("CameraManager").GetComponent<Camera_Control>();

        getSettingsFromFile();

        getPositionAndRotationForAgentFromFiles();

        createFloor();

        getAgentInfoFromFile();

        CreateAgents();

        // cameraControl.max_frames = num_frames - 1;
    }

    public void getSettingsFromFile()
    {
        var path = "TRIAL_Sets.txt";
        settingsFiles = new StreamReader(File.OpenRead(path));

        int.TryParse(settingsFiles.ReadLine(), out num_frames);
        int.TryParse(settingsFiles.ReadLine(), out num_agents);
        float.TryParse(settingsFiles.ReadLine(), out ratio_x);
        float.TryParse(settingsFiles.ReadLine(), out map_unit_size);

        cameraControl.screenshot_prefix = settingsFiles.ReadLine();

        settingsFiles.Dispose();
        settingsFiles.Close();

        if (!resize_floor) ratio_x = 1;
    }

    public void createFloor()
    {
        //MORE THE FLOOR TO THE CORRECT POSITION
        floorMapImage = (Texture2D) Resources.Load("map");


        //ADD THE TILES TO THE 
        for (float i = 0; i < floorMapImage.height; i++)
        for (float j = 0; j < floorMapImage.width; j++)
        {
            var temp = floorMapImage.GetPixel((int) i, (int) j);
//                Debug.Log(temp);
            if (temp.r <= 0)
            {
                var go = Instantiate(obstacle_tile, new Vector3(i, 1, j), Quaternion.identity);
                go.transform.parent = floor_parent.transform;

                go.transform.position = new Vector3(0.5f + i, 0, floorMapImage.height - (float) 0.5 - j);
            }
            else if (temp.r >= 1)
            {
                var go = Instantiate(entrance_tile, new Vector3(i, 1, j), Quaternion.identity);
                go.transform.parent = floor_parent.transform;
                go.transform.position = new Vector3(0.5f + i, 0, floorMapImage.height - (float) 0.5 - j);
            }
//                else if (temp.r > 0.3)
            else
            {
                var go = Instantiate(floor_tile, new Vector3(i, 1, j), Quaternion.identity);
                go.transform.parent = floor_parent.transform;
                go.transform.position = new Vector3(0.5f + i, 0, floorMapImage.height - (float) 0.5 - j);
            }
        }


        // -- Modifiying the y to 1 to 0 banish the flooor --- // 
        floor_parent.transform.localScale = new Vector3(ratio_x, 1, 1);
    }


    public void getPositionAndRotationForAgentFromFiles()
    {
        //POSITION AND ROTATION DATA FOR THE SCENE
        positions = new Vector3[num_agents][];
        rotations = new float[num_agents][];
        for (var i = 0; i < num_agents; i++)
        {
            //Debug.Log(num_frames);
            positions[i] = new Vector3[num_frames];
            rotations[i] = new float[num_frames];
        }

//        Debug.Log(positions.Length);        
//        Debug.Log(positions[1].Length);
        //STREAMREADERS
        var path = "TRIAL_Pos.txt";
        var path2 = "TRIAL_Rot.txt";
        sr_pos = new StreamReader(File.OpenRead(path));
        sr_rot = new StreamReader(File.OpenRead(path2));
        float x, z, r;
        for (var i = 0; i < num_frames; i++)
        {
            var pos = sr_pos.ReadLine().Split('\t');
            var rot = sr_rot.ReadLine().Split('\t');
            //Debug.Log(pos);
            //Debug.Log(rot);

            for (var j = 0; j < num_agents; j++)
            {
                float.TryParse(pos[2 * j], out x);
                float.TryParse(pos[2 * j + 1], out z);
                positions[j][i] = new Vector3(z * ratio_x / map_unit_size, 0, x / map_unit_size);
                //Debug.Log(positions[j, i]);
                float.TryParse(rot[j], out r);
                rotations[j][i] = r;
                //Debug.Log(rotations[i, i]);
            }
        }

        sr_pos.Dispose();
        sr_rot.Dispose();
        sr_pos.Close();
        sr_rot.Close();
    }

    public void getAgentInfoFromFile()
    {
        //POSITION AND ROTATION DATA FOR THE SCENE
        agentIDAndRadiusStruct = new Agent[num_agents];

        //STREAMREADERS
        var path = "Agents.txt";
        sr_agents = new StreamReader(File.OpenRead(path));

        var agent = sr_agents.ReadLine().Split('\t');

        int id;
        float radius;
        for (var i = 0; i < num_agents; i++)
        {
            //Debug.Log(i);
            agent = sr_agents.ReadLine().Split('\t');

            int.TryParse(agent[0], out id);
            float.TryParse(agent[1], out radius);

            agentIDAndRadiusStruct[i].ID = id;
            agentIDAndRadiusStruct[i].radius = radius;

            //Debug.Log(agentIDAndRadiusStruct[i].ID);
            //Debug.Log(agentIDAndRadiusStruct[i].radius);
        }

        sr_agents.Dispose();
        sr_agents.Close();
    }

    public void CreateAgents()
    {
        // int matcount = 1;

        cameraControl.agents = new GameObject[agentIDAndRadiusStruct.Length];

        for (var i = 0; i < agentIDAndRadiusStruct.Length; i++)
        {
            //Debug.Log(positions[i].Length);
            var temp_object = Instantiate(agent);
//            SkinnedMeshRenderer mr = temp_object.GetComponentInChildren<SkinnedMeshRenderer>();
//            //ASIGN DIFFERENT MATERIALS
//            switch(matcount)
//            {
//                case 1:
//                    mr.material = mat1;
//                    matcount += 1;
//                    break;
//                case 2:
//                    mr.material = mat2;
//                    matcount += 1;
//                    break;
//                case 3:
//                    mr.material = mat3;
//                    matcount += 1;
//                    break;
//                default:
//                    mr.material = mat4;
//                    matcount = 1;
//                    break;
//            }

            temp_object.transform.position = positions[i][1];

            //-- Get the MoveAgent Component and the set the attribute for each instance --//
            var temp = agent.GetComponent<Move_Agent>();

            temp.ID = agentIDAndRadiusStruct[i].ID;
            temp.radius = agentIDAndRadiusStruct[i].radius;

            temp.positions = positions[i];
            temp.rotations = rotations[i];
            temp.ratio_x = ratio_x;

            cameraControl.agents[i] = temp_object;
        }
    }


    // Update is called once per frame
    private void Update()
    {
    }

    public struct Agent
    {
        public int ID;
        public float radius;
    }
}