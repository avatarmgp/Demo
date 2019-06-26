using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class main : MonoBehaviour
{
    string srv_app_version;     //服务器app版本
    string srv_res_version;     //服务器res版本

    string loc_app_version = "1.0";
    string loc_res_version = "2019.6.26";

    public Dictionary<string, string> srv_files = new Dictionary<string, string>();
    public Dictionary<string, string> loc_files = new Dictionary<string, string>();

    IEnumerator GetVersionCoroutine(string url,Action<WWW> getVersionCallback)
    {
        WWW www = new WWW(url);
        yield return www;
        if(string.IsNullOrEmpty(www.error) && www.isDone)
        {
            if(getVersionCallback != null)
            {
                getVersionCallback(www);
            }
        }
        else
        {
            Debug.Log("Download failed "+www.error);
            getVersionCallback(null);
        }
        www.Dispose();
    }

    void GetVersionCallBack(WWW www)
    {
        if (www != null)
        { 
            string jsonText = www.text;
            RootObject rb = JsonConvert.DeserializeObject<RootObject>(jsonText);
            srv_app_version = rb.appversion;
            srv_res_version = rb.resversion;
        }
    }

    void DownLoadFinish(WWW www)
    {
        if (www != null)
        { 
                
        }
    }

    //检测版本
    void CheckVersion()
    {
        if (srv_app_version != loc_app_version)
        { 
            //提示重新下载app包
        }else if (srv_res_version != loc_app_version)
        { 
            //提示热更新
        }else
        {
            //直接进入游戏
        }
    }

    //热更新
    void HotUpdate()
    { 
        //下载服务器版本文件
        //加载本地版本文件
        //对比版本文件生成更新列表
        //更新文件
    }

    void Start()
    {
        //获取当前大版本号和小版本号，一个json请求
        string url = "localhost:9090";
        StartCoroutine(GetVersionCoroutine(url,GetVersionCallBack));

        //对比当前软件的app版本号是否一样
        //如果大版本不一样直接下载文件
        //载入资源文件，查看是否资源版本一样
        //如果资源版本不一样，对比本地资源文件和服务器文件
    }

    void Update()
    {
        
    }
}
