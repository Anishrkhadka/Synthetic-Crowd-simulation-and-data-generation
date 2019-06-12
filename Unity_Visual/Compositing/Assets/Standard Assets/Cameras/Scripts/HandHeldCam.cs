using System;
using UnityEngine;

namespace UnityStandardAssets.Cameras
{
    public class HandHeldCam : LookatTarget
    {
        [SerializeField] private float m_BaseSwayAmount = .5f;
        [SerializeField] private float m_SwaySpeed = .5f;
        [Range(-1, 1)] [SerializeField] private float m_TrackingBias;
        [SerializeField] private float m_TrackingSwayAmount = .5f;


        protected override void FollowTarget(float deltaTime)
        {
            base.FollowTarget(deltaTime);

            var bx = Mathf.PerlinNoise(0, Time.time * m_SwaySpeed) - 0.5f;
            var by = Mathf.PerlinNoise(0, Time.time * m_SwaySpeed + 100) - 0.5f;

            bx *= m_BaseSwayAmount;
            by *= m_BaseSwayAmount;

            var tx = Mathf.PerlinNoise(0, Time.time * m_SwaySpeed) - 0.5f + m_TrackingBias;
            var ty = Mathf.PerlinNoise(0, Time.time * m_SwaySpeed + 100) - 0.5f + m_TrackingBias;

            tx *= -m_TrackingSwayAmount * m_FollowVelocity.x;
            ty *= m_TrackingSwayAmount * m_FollowVelocity.y;

            transform.Rotate(bx + tx, by + ty, 0);
        }
    }
}