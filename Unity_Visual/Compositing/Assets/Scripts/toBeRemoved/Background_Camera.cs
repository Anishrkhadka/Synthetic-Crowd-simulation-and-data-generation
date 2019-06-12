using UnityEngine;
using System.Collections;
using UnityEditor;

public class Background_Camera : MonoBehaviour
{
    public Sprite background;
    public Vector3 current_scale;
    public float scale_amount = 0.1f;


    public int screen_height;
    public int screen_width;
    public SpriteRenderer sr;

    // Use this for initialization
    private void Start()
    {
        sr = GetComponent<SpriteRenderer>();

        background = (Sprite) Resources.Load("Background", typeof(Sprite));
        sr.sprite = background;
        screen_height = background.texture.height;
        screen_width = background.texture.width;

        Screen.SetResolution(background.texture.width, background.texture.height, false);
    }

    public void ScaleUp()
    {
        current_scale = transform.localScale;
        transform.localScale = current_scale + new Vector3(scale_amount, scale_amount, 0);
    }

    public void ScaleDown()
    {
        current_scale = transform.localScale;
        transform.localScale = current_scale - new Vector3(scale_amount, scale_amount, 0);
    }

    public void SetScale(Vector3 scale)
    {
        transform.localScale = scale;
        current_scale = scale;
    }
}