# python_import_research

这个项目是为了搞明白python的模块引用机制而创建的。

python中，每个.py文件被称之为模块(module)，每个具有__init__.py文件的目录被称为包(package)，包通常包含很多模块的目录。只要模块或者包所在的目录在sys.path中，就可以使用import 模块或import 包来使用。

不过，实际情况要复杂得多，因为我们有相对引用和绝对引用两种引用方式；同时，还有从脚本调用模块、从模块调用模块等多种层级关系，所以需要分类讨论，测试如何在各种情况下合理引用。

> 我分别使用过spyder与vscode作为编辑器，在运行时他们的表现似乎有不同（？），有必要声明，在运行该项目时使用的是vscode。如果之后我用spyder运行该项目发现表现相同，会删除这段话。

## 基本引用方法

首先说引用方式。绝对引用有如下几种常见的引用方式

```python
# 引入模块
import module [as name] 
import package.module [as name] 
from package import module [as name] 
import package.subpackage.module [as name]
from package.subpackage import module [as name]

# 引入功能
from module import func [as name]
from package.module import func [as name]
from package.subpackage.module import func [as name]

# 错误用法
# import package.module.func [as name] # 多级的.中，最末的会被认为是模块
```

可见，包>模块>功能（函数、变量）之间有层级关系，from的对象只能是包或模块，import的对象可以是包、模块或者功能。事实上包是一个包含其他模块的模块，包本身也是一个模块，它的功能（函数、变量）在package目录下的\_\_init\_\_.py文件中。包里面当然也能包含包。

相对引用顾名思义是以相对路径来引用包，通常用于使用自定义包的场景。怎么引用会在后面的具体例子里说明，这里先不说了。

## 案例

一般在描述引用关系时，用package_A、package_B、module_a.py、module_b.py举例就够了，但为了便于理解，我希望这些模块更有意义，而不是单纯的以编号命名。

考虑下面这个极其简单的计算器案例，它只能处理正整数的加法和乘法运算：

```
└── simple_add_calculater
	├── main.py
    ├── package_show
    │   ├── module_showInfo.py
    │   └── module_showRules.py
    └── package_calc
    	├── __init__.py
    	├── module_str.py
    	└── subpackage_exp
    		└── module_expAnalysis.py
```

每个部分的实际意义如下：

- main.py：主函数，运行后，在控制台输入表达式，输出值，直到输入exit.
- package_show：用于显示信息的“包”，但不含\_\_init\_\_.py，可以与含有\_\_init\_\_.py的模块形成比较。
  - module_showInfo.py：用于显示计算器的信息。
  - module_showRules.py：用于显示计算器的输入规则。
- package_calc：用于计算的包。
  - \_\_init\_\_.py：含有add和mult两个函数，用于计算两个数的和与积。
  - module_str.py：含有str2int函数，用于将字符转换成整数。
  - subpackage_exp：用于处理表达式字符串的包。
    - module_expAnalysis.py：分析表达式字符串是否合法。