// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "AnishRKhadka/FlatShader" {
	Properties {
		_Color ("Color", Color) = (1,1,1,1)
	}
	SubShader {

		pass{
			CGPROGRAM

			#pragma vertex vertexShader
			#pragma fragment pixelShader


			// -- User define colour: external interface for unity gui -- // 
			uniform float4 _Color;


			struct a2v
			{
				float4 position : POSITION;
			};


			struct v2f
			{

				float4 position : SV_POSITION;
			};


			v2f vertexShader(a2v In){
				v2f Out;

				Out.position = UnityObjectToClipPos(In.position);

				return Out;
			}



			float4 pixelShader(v2f In) : COLOR
			{

				return _Color;

			}

			ENDCG

			}
	}
	FallBack "Diffuse"
}
