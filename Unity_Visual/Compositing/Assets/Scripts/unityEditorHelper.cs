using System.Collections;
using System.Collections.Generic;
using UnityEngine;

 public static class unityEditorHelper
 {
     public static void Quit()
     {
         #if UNITY_EDITOR
         UnityEditor.EditorApplication.isPlaying = false;
         #else
         Application.Quit();
         #endif
     }
 }
