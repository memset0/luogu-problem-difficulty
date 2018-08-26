# luogu-problem-difficulty

统计（通过）的洛谷题目的难度。

**如果出现不能使用的情况， 请更新到最新版本。**

**请在合理范围内爬取数据，出现的一切后果概不负责。**

# 安装

首先您需要点击右上方的 Download 按钮下载源码并解压。

打开解压出的文件夹，进入`main.py`所在的文件夹。

在命令行中输入以下命令安装第三方库并运行爬虫（以 cmd 为例）。

```plain
pip install pyyaml
pip install requests
copy config.sample.yml config.yml
python main.py
```

你可以在`config.yml`文件中修改配置，具体方法其中有中文注释。

从第二次使用开始您可以直接双击运行 `main.py` 即可。

# 结果

产生的结果保存在以下文件中:
```
result/U*****.txt
```

（默认关闭未完成的HTML的结果生成）

# 注意

所有被隐藏的题目或尚未评定难度的题目均不会被计算在内

# TODO

1. 完善HTML的结果生成
2. 添加批量分析的功能，同时避免重复

# License

MIT License