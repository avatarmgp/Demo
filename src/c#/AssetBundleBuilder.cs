using UnityEngine;
using System.Collections.Generic;
using UnityEditor;
using System.IO;

public class AssetBundleBuilder : Editor
{
    public static List<string> abResourcePath = new List<string>()
    {
        "Prefabs",
    };

    public class AssetNode
    {
        public List<AssetNode> parents = new List<AssetNode>();
        public string path;
        public int depth = 0;
    }

    private static List<AssetNode> _leafNodes = new List<AssetNode>();
    private static Dictionary<string,AssetNode> _allAssetNodes = new Dictionary<string, AssetNode>();
    private static List<string> _buildMap = new List<string>();

    //打包assetbundle
    [MenuItem("AssetBundle/BuildAssetbundle")]
    public static void BuildAssetBundle()
    {
        Init();
		CollectDependcy();
		BuildResourceBuildMap();
		BuildAssetBundleWithBuildMap();
		AssetDatabase.SaveAssets();
		AssetDatabase.Refresh();	
    }

    static void Init()
	{
		_buildMap.Clear();
		_leafNodes.Clear();
		_allAssetNodes.Clear();
	}

    static void CollectDependcy()
    {
        for (int i = 0; i < abResourcePath.Count; i++)
        {
            string path = Application.dataPath + "/" + abResourcePath[i];
            if (!Directory.Exists(path))
            {
                Debug.LogError(string.Format("abResourcePath {0} not exist",abResourcePath[i]));
            }
            else 
            {
                DirectoryInfo dir = new DirectoryInfo(path);
                FileInfo[] files = dir.GetFiles("*", SearchOption.AllDirectories);
                for (int j = 0; j < files.Length; j++)
                {
                    string fileName = files[j].FullName;
                    if(fileName.EndsWith(".meta") || fileName.EndsWith(".DS_Store") || fileName.EndsWith(".cs"))
                        continue;

                    string fileRelativePath = GetRelativeToAssets(fileName);
                    AssetNode root = null;
                    if (!_allAssetNodes.ContainsKey(fileRelativePath))
                    {
                        root = new AssetNode();
                        root.path = fileRelativePath;
                        _allAssetNodes[root.path] = root;
                        GetDependcyRecursive(fileRelativePath, root);
                    }
                }
            }
        }
    }

    static void GetDependcyRecursive(string path,AssetNode parentNode)
    {
        string[] dependcy = AssetDatabase.GetDependencies(path, false);
        for (int i = 0; i < dependcy.Length; i++)
        {
            if (_allAssetNodes.ContainsKey(dependcy[i]))
            {
                var node = _allAssetNodes[dependcy[i]];
                if(!node.parents.Contains(parentNode))
                {
                    node.parents.Add(parentNode);
                }
                if (node.depth < parentNode.depth + 1)
                {
                    node.depth = parentNode.depth + 1;
                    GetDependcyRecursive(dependcy[i], node);
                }
            }
            else
            {
                AssetNode node = new AssetNode();
				node.path = dependcy[i];
				node.depth = parentNode.depth + 1;
				node.parents.Add(parentNode);
				_allAssetNodes[node.path] = node;
				GetDependcyRecursive(dependcy[i],node);
            }
        }

        //叶子节点
        if (dependcy.Length == 0)
        { 
            if(!_leafNodes.Contains(parentNode))
			{
				_leafNodes.Add(parentNode);
			}
        }
    }

    static int GetMaxDepthOfLeafNodes()
	{
		if(_leafNodes.Count == 0)
			return 0;
		_leafNodes.Sort((x,y)=> 
			{
				return y.depth - x.depth;
			});
		return _leafNodes[0].depth;
	}

    //首先获取到最底层叶子节点
    //然后一层层往上遍历
    static void BuildResourceBuildMap()
	{
		int maxDepth = GetMaxDepthOfLeafNodes();
		while(_leafNodes.Count > 0)
		{
			List<AssetNode> _curDepthNodesList = new List<AssetNode>();
			for(int i = 0; i < _leafNodes.Count;i++)
			{
				if(_leafNodes[i].depth == maxDepth)
				{
					//如果叶子节点有多个父节点或者没有父节点,打包该叶子节点
                    //0或者>1
					if(_leafNodes[i].parents.Count != 1)
					{
						if(!_leafNodes[i].path.EndsWith(".cs"))
						{
							_buildMap.Add(_leafNodes[i].path);
						}
					}
					_curDepthNodesList.Add(_leafNodes[i]);
				}
			}
			//删除已经遍历过的叶子节点，并把这些叶子节点的父节点添加到新一轮的叶子节点中
			for(int i = 0; i < _curDepthNodesList.Count;i++)
			{
				_leafNodes.Remove(_curDepthNodesList[i]);
				foreach(AssetNode node in _curDepthNodesList[i].parents)
				{
					if(!_leafNodes.Contains(node))
					{
						_leafNodes.Add(node);
					}
				}
			}
			maxDepth -= 1;
		}
	}

    public static string AssetBundle_Path = Application.streamingAssetsPath;
    //通过buildmap创建assetbundle
    static void BuildAssetBundleWithBuildMap()
	{
		string prefix = "Assets";
		AssetBundleBuild[] buildMapArray = new AssetBundleBuild[_buildMap.Count];
		for(int i = 0;i < _buildMap.Count;i++)
		{
			buildMapArray[i].assetBundleName = _buildMap[i].Substring(prefix.Length+1);
			buildMapArray[i].assetNames = new string[]{_buildMap[i]};
			Debug.Log(_buildMap[i]);
		}
		if(!Directory.Exists(AssetBundle_Path))
			Directory.CreateDirectory(AssetBundle_Path);
		BuildPipeline.BuildAssetBundles(AssetBundle_Path, buildMapArray, BuildAssetBundleOptions.ChunkBasedCompression|BuildAssetBundleOptions.DeterministicAssetBundle, EditorUserBuildSettings.activeBuildTarget);	
	}

    static string GetRelativeToAssets(string fullName)
    {
        string fileRelativePath = fullName.Substring(Application.dataPath.Length - 6);
        fileRelativePath = fileRelativePath.Replace("\\", "/");
        return fileRelativePath;
    }
}
