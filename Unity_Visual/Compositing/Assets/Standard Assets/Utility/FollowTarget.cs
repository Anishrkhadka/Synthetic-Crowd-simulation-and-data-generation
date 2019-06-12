using System;
using UnityEngine;


namespace UnityStandardAssets.Utility
{
    public class FollowTarget : MonoBehaviour
    {
        public Vector3 offset = new Vector3(0f, 7.5f, 0f);
        public Transform target;


        private void LateUpdate()
        {
            transform.position = target.position + offset;
        }
    }
}