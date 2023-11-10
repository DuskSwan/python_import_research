# python import导入机制研究

这个项目是为了搞明白python的模块引用机制而创建的。

python中，每个.py文件被称之为模块(module)，每个具有\_\_init\_\_.py文件的目录被称为包(package)，包通常是包含了很多模块。只要模块或者包所在的目录在sys.path中，就可以使用import 模块或import包来使用。

不过，实际情况要复杂得多，因为我们有相对引用和绝对引用两种引用方式；同时，还有从脚本调用模块、从模块调用模块等多种层级关系，所以需要分类讨论，测试如何在各种情况下合理引用。

我将给出一个极其简单的计算器案例，在这一案例中涵盖所有可能的引用情况。

```
└── simple_calculator
	├── main.py
    ├── package_show
    │   ├── module_showInfo.py
    │   └── module_showRules.py
    └── package_calc
    	├── __init__.py
    	├── module_calc.py
    	└── subpackage_exp
    		└── module_expAnalysis.py
```

更加详细的结果，请阅读`how to import self-defined module.md`。