using UnityEngine;

namespace UnityStandardAssets.Utility
{
    public class SimpleActivatorMenu : MonoBehaviour
    {
        // An incredibly simple menu which, when given references
        // to gameobjects in the scene
        public GUIText camSwitchButton;


        private int m_CurrentActiveObject;
        public GameObject[] objects;


        private void OnEnable()
        {
            // active object starts from first in array
            m_CurrentActiveObject = 0;
            camSwitchButton.text = objects[m_CurrentActiveObject].name;
        }


        public void NextCamera()
        {
            var nextactiveobject = m_CurrentActiveObject + 1 >= objects.Length ? 0 : m_CurrentActiveObject + 1;

            for (var i = 0; i < objects.Length; i++) objects[i].SetActive(i == nextactiveobject);

            m_CurrentActiveObject = nextactiveobject;
            camSwitchButton.text = objects[m_CurrentActiveObject].name;
        }
    }
}