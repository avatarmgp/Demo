using UnityEngine;
using System.Collections;
using UnityEditor;
using System;
using System.IO;
using System.Text;
using System.Collections.Generic;

//版本生成文件
namespace AssetBundleFramework
{
    public class VersionFile {
        //name-md5
        public Dictionary<string, string> files = new Dictionary<string, string>();
        //version
        public string resVersion;
    }

    public class VersionBuilder : Editor 
	{
		public static string AssetsPath = Application.streamingAssetsPath;
		private static string _versionFilesPath = Application.dataPath + "/VersionFiles/";
        private static VersionFile _versionFile = new VersionFile();

        public static string GetMd5Val(string path)
		{
			FileStream file = new FileStream(path, FileMode.Open);
			System.Security.Cryptography.MD5 md5 = new System.Security.Cryptography.MD5CryptoServiceProvider();
			byte[] retVal = md5.ComputeHash(file);
			file.Close();
			StringBuilder sb = new StringBuilder();
			for (int j = 0; j < retVal.Length; j++)
			{
				sb.Append(retVal[j].ToString("x2"));
			}
			return sb.ToString();
		}

        [MenuItem("Version/CleanBuildApp(we need a new app)")]
		static void BuildGameApp()
		{
            //清空原先的streamasset目录
            if(Directory.Exists(AssetsPath))
			{
				Directory.Delete(AssetsPath,true);
			}
            //清空版本文件
            if(Directory.Exists(_versionFilesPath))
			{
				Directory.Delete(_versionFilesPath,true);
			}
            //打包assetbundle
            AssetBundleBuilder.BuildAssetBundle();
            //生成版本文件
            GenerateVersionFiles();
		}

		//生成更新文件列表
		static void GenerateVersionFiles()
		{
            _versionFile.resVersion = "2019.6.26";
            _versionFile.files.Clear();
			if(!Directory.Exists(AssetsPath))
			{
				Debug.LogError(string.Format("AssetsPath path {0} not exist",AssetsPath));
				return;
			}
			DirectoryInfo dir = new DirectoryInfo(AssetsPath);
			var files = dir.GetFiles("*", SearchOption.AllDirectories);
			for (var i = 0; i < files.Length; ++i)
			{
				try
				{
					if(files[i].Name.EndsWith(".meta") || files[i].Name.EndsWith(".manifest") )
						continue;
					string md5 = GetMd5Val(files[i].FullName);
					string fileRelativePath = files[i].FullName.Substring(AssetsPath.Length+1);
					_versionFile.files[fileRelativePath] = md5;
				}
				catch (Exception ex)
				{
					throw new Exception("GetMD5HashFromFile fail,error:" + ex.Message);
					return;
				}
			}

			if(!Directory.Exists(_versionFilesPath))
			{
				Directory.CreateDirectory(_versionFilesPath);
			}
			StringBuilder sb = new StringBuilder();		
			foreach(KeyValuePair<string,string> kvp in _versionFile.files)
			{
				string content = string.Format("{0},{1}\n",kvp.Key,kvp.Value);
				sb.Append(content);
			}
			sb.Append(_versionFile.resVersion);
			File.WriteAllText(_versionFilesPath + "VersionFile.txt",sb.ToString());	
		}
	}
}