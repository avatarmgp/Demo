Shader "test"{
    Properties{
        //属性
    }

    //显卡A
    SubShader{
        Pass{
            //渲染状态和标签

            //开始CG代码段
            CGPROGRAM
            
            //定义顶点着色器函数
            #pragma vertex vert
            //定义片段着色器函数
            #pragma fragment frag

            ENDCG
        }
    }
    //显卡B
    SubShader{

    }

    //以上所有显卡都不能使用
    Fallback "VertexLit"
}