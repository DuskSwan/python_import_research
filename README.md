# python_import_research

这个项目是为了搞明白python的模块引用机制而创建的。

python中，每个.py文件被称之为模块(module)，每个具有__init__.py文件的目录被称为包(package)，包通常包含很多模块的目录。只要模块或者包所在的目录在sys.path中，就可以使用import 模块或import 包来使用。

不过，实际情况要复杂得多，因为我们有相对引用和绝对引用两种引用方式；同时，还有从脚本调用模块、从模块调用模块等多种层级关系，所以需要分类讨论，测试如何在各种情况下合理引用。

> 我分别使用过spyder与vscode作为编辑器，在运行时他们的表现似乎有不同（？），有必要声明，在运行该项目时使用的是vscode。如果之后我用spyder运行该项目发现表现相同，会删除这段话。

## 基本概念

### 包(package)与模块(module)

一个模块是一个包含了Python代码的文件（以`.py`为扩展名）。模块可以包含函数、类、变量和其他Python代码。可以将模块看作是一个独立的代码单元，它包含类、函数、变量可以被其他程序或模块导入和使用。

包是一种组织模块的方式。它是一个包含了一组相关模块的目录，该目录中还包含一个特殊的名为 `__init__.py` 的文件（可以为空文件）。这个 `__init__.py` 文件指示该目录是一个包，并允许你在其他地方导入包与包中的模块。事实上包可以看作一个包含其他模块的模块，它的功能（类、函数、变量）在package目录下的\_\_init\_\_.py文件中。包里面当然也能包含新的包。

### 引用方式

有以下几种常见的引用方式

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

简单来说就是from包或模块，从中import包、模块或者功能（类、函数、变量）。

在执行import语句时，到底进行了什么操作？按照python的文档，它执行了如下操作：

> 第1步，创建一个新的，空的module对象（它可能包含多个module）；
> 第2步，把这个module对象插入sys.module中
> 第3步，装载module的代码（如果需要，首先必须编译成.pyc文件）
> 第4步，执行新的module中对应的代码。

关键就在于第3步要找到module程序所在的位置，其原理为：如果需要导入的module的名字是m1，则解释器必须找到m1.py。解释器先在**当前目录**中搜索名为 m1.py 的文件。如果没有找到的话，接着会到 **sys.path** 变量中给出的目录列表中查找。 sys.path 变量的初始值来自如下：

+ 输入脚本的目录（当前路径）。

+ 环境变量 PYTHONPATH 表示的目录列表中的目录。

+ Python 默认安装路径中搜索。 

sys.path变量中依次包含上述路径，因此搜索顺序也是当前路径、然后是PYTHONPATH、然后是python的安装设置相关的默认路径。正因为存在这样的顺序，如果当前路径或PYTHONPATH中存在与标准module同样的module，则会覆盖标准module。比如，如果当前目录下存在xml.py，那么执行import xml时，导入的是当前目录下的module，而不是系统标准的xml。

上述引用方式都是以绝对路径引用，所引的包或模块存在于当前运行脚本的同目录下。然而，在自定义包时，有时需要一个模块引用同包下的另一个模块，这时需要用相对引用的方法。相对引用顾名思义是以相对路径来引用包，通常用于使用自定义包的场景。一个常见的情况是在同一个包内有`a.py`和`b.py`，如果要在`a.py`中使用`b.py`中的函数func，就需要

```python
# a.py
from .b import func
```



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
    	├── module_calc.py
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