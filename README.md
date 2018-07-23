# luogu-problem-difficulty

统计（通过）的洛谷题目的难度。

# 安装

使用了一些第三方库，你需要先安装他们。

你可以下`config.yml`文件中修改配置，具体方法其中有中文注释。

进入命令行（如果你已经正确安装了`Python3`且配置了路径的话），输入

```bash
pip install pyyaml
pip install requests
python main.py
```

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