using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

public class getBackgroundManager : MonoBehaviour
{

	public GameObject backgroundImageSpriteTemplate;
	
	public GameObject[] backgroundImageSpriteList;
	public Texture2D[] backgroundImage;
	
	private int circulatingCounter = -1;
	private bool IsFixBackground;
	
	public void init()
	{
		var length = backgroundImage.Count(t => t != null);

		backgroundImageSpriteList = new GameObject[length];
		
		for (var i = 0; i < backgroundImageSpriteList.Length; i++)
		{
			var instantiate = Instantiate(backgroundImageSpriteTemplate, new Vector3(0, 0, 0), Quaternion.identity);
			instantiate.transform.parent = transform;
			instantiate.GetComponent<SpriteRenderer>().sprite = Sprite.Create( backgroundImage[i], 
								new Rect( 0, 0, backgroundImage[i].width, backgroundImage[i].height ), 
								new Vector2( 0.5f, 0.5f ) );
			
			backgroundImageSpriteList[i] = instantiate;
		}
				
	}

	
	public Sprite getDefaultBackgroundImage()
	{
		if (IsFixBackground) return backgroundImageSpriteList[circulatingCounter].GetComponent<SpriteRenderer>().sprite;
		if (circulatingCounter < backgroundImageSpriteList.Length - 1)
		{
			circulatingCounter += 1;
		}
		else
		{
			circulatingCounter = 0;
			backgroundImageSpriteList[0].GetComponent<SpriteRenderer>().color = Color.white;
		}

//		print("Current Background Index"+circulatingCounter);
		return backgroundImageSpriteList[circulatingCounter].GetComponent<SpriteRenderer>().sprite ;
		

	}

	public int getCurrentBackgroundIndex()
	{
		return circulatingCounter;
	}

	// Return a black sprite --//
	public Sprite getBackgroundImageForGT()
	{
//		var instantiate = backgroundImageSpriteList[0];
		backgroundImageSpriteList[0].GetComponent<SpriteRenderer>().color = Color.black;

		return backgroundImageSpriteList[0].GetComponent<SpriteRenderer>().sprite;
	}

	public void setISFixBackground(bool InValue)
	{
		IsFixBackground = InValue;
	}

	public bool getIsFixBackground()
	{
		return IsFixBackground;
	}
	
}
