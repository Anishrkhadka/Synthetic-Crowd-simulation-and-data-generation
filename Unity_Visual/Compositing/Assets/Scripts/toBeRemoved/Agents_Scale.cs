using UnityEngine;

public class Agents_Scale : MonoBehaviour
{
    public GameObject[] agents;

    public float move_amount = 0.5f;
    public Vector3 scale;
    public float scale_amount = 0.05f;

    // Use this for initialization
    private void Start()
    {
        agents = new GameObject[3];

        var i = 0;
        foreach (Transform child in transform)
        {
            agents[i] = child.gameObject;
            i++;
        }

        scale = transform.localScale;
    }

    public void XUp()
    {
        var current_pos = transform.position;
        transform.position = current_pos + new Vector3(move_amount, 0, 0);
    }

    public void YUp()
    {
        var current_pos = transform.position;
        transform.position = current_pos + new Vector3(0, move_amount, 0);
    }

    public void ZUp()
    {
        var current_pos = transform.position;
        transform.position = current_pos + new Vector3(0, 0, move_amount);
    }

    public void XDown()
    {
        var current_pos = transform.position;
        transform.position = current_pos + new Vector3(-move_amount, 0, 0);
    }

    public void YDown()
    {
        var current_pos = transform.position;
        transform.position = current_pos + new Vector3(0, -move_amount, 0);
    }

    public void ZDown()
    {
        var current_pos = transform.position;
        transform.position = current_pos + new Vector3(0, 0, -move_amount);
    }

    public void ScaleUp()
    {
        for (var i = 0; i < agents.Length; i++)
            agents[i].transform.localScale = scale + new Vector3(scale_amount, scale_amount, scale_amount);
        scale = agents[1].transform.localScale;
    }

    public void ScaleDown()
    {
        for (var i = 0; i < agents.Length; i++)
            agents[i].transform.localScale = scale - new Vector3(scale_amount, scale_amount, scale_amount);
        scale = agents[1].transform.localScale;
    }

    public void SetScale(Vector3 new_scale)
    {
        for (var i = 0; i < agents.Length; i++) agents[i].transform.localScale = new_scale;
        scale = agents[1].transform.localScale;
    }

    public void SetLayer(int layer_num)
    {
        for (var i = 0; i < agents.Length; i++) agents[i].layer = layer_num;
    }
}