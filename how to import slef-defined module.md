# python_import_research

这个项目是为了搞明白python的模块引用机制而创建的。

python中，每个.py文件被称之为模块(module)，每个具有__init__.py文件的目录被称为包(package)，包通常包含很多模块的目录。只要模块或者包所在的目录在sys.path中，就可以使用import 模块或import 包来使用。

不过，实际情况要复杂得多，因为我们有相对引用和绝对引用两种引用方式；同时，还有从脚本调用模块、从模块调用模块等多种层级关系，所以需要分类讨论，测试如何在各种情况下合理引用。

> 我分别使用过spyder与vscode作为编辑器，在运行时他们的表现似乎有不同（？），有必要声明，在运行该项目时使用的是vscode。如果之后我用spyder运行该项目发现表现相同，会删除这段话。

## 基本概念

### 包(package)与模块(module)

一个模块是一个包含了Python代码的文件（以`.py`为扩展名）。模块可以包含函数、类、变量和其他Python代码。可以将模块看作是一个独立的代码单元，它包含类、函数、变量可以被其他程序或模块导入和使用。

包是一种组织模块的方式。它是一个包含了一组相关模块的目录，该目录中还包含一个特殊的名为 `__init__.py` 的文件（可以为空文件）。这个 `__init__.py` 文件指示该目录是一个包，并允许你在其他地方导入包与包中的模块。事实上包可以看作一个包含其他模块的模块，它的功能（类、函数、变量）在package目录下的\_\_init\_\_.py文件中。包里面当然也能包含新的包。

### from...import...语法

有以下几种常见的引用方式

```python
# 引入模块
import module [as name] 
import package.module [as name] 
import package.subpackage.module [as name]
from package import module [as name] 
from package.subpackage import module [as name]

# 引入功能
from module import func [as name]
from package.module import func [as name]
from package.subpackage.module import func [as name]

# 错误用法
# import package.module.func [as name] # 多级的.中，最末的会被认为是模块
```

总的来说只有三种情况：①import模块②from模块import功能③from包import模块。

值得注意的是：①后面的测试中会发现，from的对象也可以是一个目录（欠缺\_\_init\_\_.py的包）②from A import B会先被考虑成从模块引入功能，不满足时再考虑从包引入模块，如果一个包A中有同名的模块B与功能B，from A import B导入的实际上是功能B而非模块。

### 环境变量sys.path

在执行import语句时，到底进行了什么操作？按照python的文档，它执行了如下操作：

> 第1步，创建一个新的，空的module对象（它可能包含多个module）；
> 第2步，把这个module对象插入sys.module中
> 第3步，装载module的代码（每个模块都会被编译成一个对应的.pyc文件）
> 第4步，执行新的module中对应的代码。

关键就在于第3步要找到module程序所在的位置，其原理为：如果需要导入的module的名字是m1，则解释器必须找到m1.py。解释器先在**当前目录**中搜索名为 m1.py 的文件。如果没有找到的话，接着会到 **sys.path** 变量中给出的目录列表中查找。 sys.path 变量的初始值来自如下：

+ 输入脚本的目录。

+ 环境变量 PYTHONPATH 表示的目录列表中的目录。

+ Python 默认安装路径中搜索。 

sys.path变量中依次包含上述路径，因此搜索顺序也是当前路径、然后是PYTHONPATH、然后是python的安装设置相关的默认路径。正因为存在这样的顺序，如果当前路径或PYTHONPATH中存在与标准module同样的module，则会覆盖标准module。比如，如果当前目录下存在xml.py，那么执行import xml时，导入的是当前目录下的module，而不是系统标准的xml。

### 相对路径引用

上述引用方式都是以绝对路径引用，所引的包或模块存在于当前运行脚本的同目录下。然而，在自定义包时，有时需要一个模块引用同包下的另一个模块，这时需要用相对引用的方法。相对引用顾名思义是以相对路径来引用包，通常用于使用自定义包的场景。一个常见的情况是在同一个包内有`a.py`和`b.py`，如果要在`a.py`中使用`b.py`中的函数func，就需要

```python
# a.py
from .b import func
```

此时的`.`表示后面的内容处于当前目录下，如果换成`..`就是上一级目录下，以此类推。

值得注意的是，①用`.`表示目录的用法只能出现在from的对象里，`import .a`则不行；②当某个`.py`文件使用相对导入时，对于目录关系的判断是基于当前模块的`__name__`属性的（而不是实际的目录结构），而运行脚本的`__name__`为`__main__`，必然无法用相对路径导入。更详细的信息请看[`__name__`属性](https://docs.python.org/3/library/__main__.html)。

## 案例

一般在描述引用关系时，用package_A、package_B、module_a.py、module_b.py举例就够了，但为了便于理解，我希望这些模块更有意义，而不是单纯的以编号命名。

考虑下面这个极其简单的计算器案例，它只能处理正整数的加法和乘法运算：

```
└── simple_add_calculater (工作目录)
	├── config.py
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
  - \_\_init\_\_.py：含有功能函数calc，用于根据表达式计算结果。
  - module_str.py：含有str2int函数，用于将字符转换成整数。
  - subpackage_exp：用于处理表达式字符串的包。
    - module_expAnalysis.py：分析表达式字符串是否合法。

这一结构将涵盖所有可能的引用情况。下来让我们逐一分析。



## 各种引用情况

注意，工作目录要设为`simple_add_calculater`（而不是本项目的仓库）



### 1、脚本中引用同目录的包或模块

同目录下的包或模块，指的是包或模块和运行脚本处于同一目录下。

在main.py中，分别使用了同目录（simple_calculator）下的模块、包（实际上是对应的\_\_init.py\_\_）以及目录中的两个模块。以如下方式引用，可以正常执行：

```python
import config
from package_calc import calc
from package_show.module_showInfo import show_info
from package_show.module_showRules import show_rules
```

进一步分类讨论各个情况

- 使用同目录下的模块中的方法

  直接import模块，或者从模块中import具体的功能（类、函数、变量）。因为脚本所在的目录已经加入了sys.path.

- 使用同目录下的包中的方法

  直接import包，或者从包中import具体的功能（类、函数、变量）。因为脚本所在的目录已经加入了sys.path.

- 使用同目录下的目录中的模块中的函数

  注意，这时并不需要要求是“包中的函数”，只需要是“模块中函数”就行，这个要求实际上比包更低。不需要\_\_init.py\_\_也行。

  - 直接from 目录.模块 import 功能，可行
  - from 目录 import 模块，再调用模块.功能，可行
  - import 目录，再调用目录.模块.功能，不可行。此时会把“目录.模块.功能”解读成目录的\__init__.py中的内容，所以报错AttributeError: module 目录 has no attribute 模块。

  ```python
  from package_show.module_showRules import show_rules 
      # yes
  
  from package_show import module_showRules 
  show_rules = module_showRules.show_rules
      # yes
  
  # import package_show
  # show_rules = package_show.module_showRules.show_rules
      # no
  ```



我们注意到，`from A import B`后使用`B`与`import A`后使用`A.B `有一样的效果。所以只考虑`from A import B`形式的调用。

另外，当模块与包处于同一目录中时，使用模块中的方法（`from module import func`）和使用包中的方法（`from package import func`）并无本质区别；使用包中的模块（`from package import module`）和使用包中的方法（`from package import func`）在导入时也遵循相同的逻辑。因此，只要能成功实现`from module import xxx`，与module处于同目录下的package就同样可以通过`from package import xxx`引入。

至于下级目录、下下级目录、……中的包，只要用`from package.subpackage.subsubpackage.... import xxx`就好了，与同级目录一个原理。

综上所述，之后只需要观察如何实现`from module import xxx`，也即如何引入模块即可，无需再讨论如何引入包。



### 2、脚本中引用父目录的模块

上一级目录下的包或模块，指的是包或模块与运行脚本所在的目录处于同一父目录下。

在本案例中，如果希望运行package_show/module_showInfo.py并输出config.py的信息，就属于这种情况。以如下方式引用，可以正常执行：

```python
# method 1
current_path = os.path.abspath(__file__)
current_cont = os.path.dirname(current_path)
parent_cont = os.path.dirname(current_cont)
sys.path.append(parent_cont)
from config import cfg

# method 2
sys.path.append('.')
from config import cfg
```

这本质上是手动添加了模块所在的目录进入sys.path。只不过法1添加的是绝对路径，法2添加的是相对路径。



### 3、脚本中引用隔壁目录的模块

隔壁目录下的包或模块，指的是包或模块所在的目录，和运行脚本所在的目录处于同一父目录下。

在本案例中，如果希望在package_show/module_showInfo.py中使用package_calc/module_calc.py的函数add，就属于这种情况。以如下方式引用，可以正常执行：

```python
# method 1
current_path = os.path.abspath(__file__)
current_cont = os.path.dirname(current_path)
parent_cont = os.path.dirname(current_cont)
sys.path.append(parent_cont)
from package_calc.module_calc import add

# method 2
sys.path.append('.')
from package_calc.module_calc import add
```

事实上这与“引用上一级目录的包或模块”一样，都是将模块所在的目录加入sys.path。



### 4、模块中引用同目录的模块

模块中引用同目录的模块，指的是一个包中有模块a和b，运行脚本要引用a，而a又要引用b。此时a是以模块的身份来引用b的。

在本案例中，mian.py要使用package_calc中的函数calc（本质上是`package_calc\__init__.py`中的函数calc），而calc又用了`package_calc\module_calc.py`中的函数add,mult,str2int，以及`package_calc\subpackage_exp\module_expAnalysis.py`中的函数legal_exp,parse_expression，换言之`__init__.py`在以模块身份引用`module_calc.py`. 在`__init__.py`中应该用下面的引用方式：

（以下代码是写在`__init__.py`中的，运行的则是`main.py`）

```python
# method 1
from .subpackage_exp.module_expAnalysis import legal_exp,parse_expression
from .module_calc import add,mult,str2int

# method 2 
from . import module_calc
add,mult,str2int = module_calc.add,module_calc.mult,module_calc.str2int
```

其中`.xxx`就表示同一个包下的模块xxx，可以看作该模块所处的包以空名字`(null)`或者`.`存在。

而且，此时只能以相对路径引用，如果试图使用绝对路径就会出错：

```python
# from module_calc import add,mult,str2int
# ModuleNotFoundError: No module named 'module_calc'
```



### 5、模块中引用父目录的模块 & 6、模块中引用隔壁目录或的模块

相信根据之前的描述，这一节标题所描述的两种情况是容易理解的。然而，我认为，在实际使用中，应该不会出现这样繁琐而且反人类的引用关系。

所以，这里直接给出如何实现，而不再多加分析。我相信经过之前的例子，这是容易理解的。



**模块中引用父目录的模块**

运行`main.py`，引用`package_calc\subpackage_exp\module_expAnalysis.py`，在其中又引用`package_calc\module_calc.py`

```python
# module_expAnalysis.py
def test_condition5():
    from ..module_calc import add
    print(add(1,2))
# main.py
def test_condition5():
    from package_calc.subpackage_exp import module_expAnalysis
    module_expAnalysis.test_condition5()
```

这时可以成功运行。



**模块中引用隔壁目录的模块**

运行`main.py`，引用`package_calc\module_calc.py`，在其中又引用`package_show\module_showInfo.py`

```python
# module_calc.py
def test_condition6():
    from ..package_show.module_showInfo import show_info
    show_info()
# main.py
def test_condition6():
    from package_calc import module_calc
    module_calc.test_condition6()
# ImportError: attempted relative import beyond top-level package
```

这时会报错ImportError: attempted relative import beyond top-level package。这个错误表示从顶级包之外进行相对导入时。在Python中，相对导入是基于当前模块的`__name__`属性的，而不是它在包中的实际位置。

在本案例中如果输出`module_calc.py`的`__name__`，会发现是`package_calc.module_calc`，这是运行脚本读取module_calc的结构。module_calc中的`.`即表示package_calc这一级，`..`应该是package_calc所属于的包，但并不存在这样的包。

如果要成功实现模块中引用隔壁目录的模块，应该在package_calc中创建`subpackage_xxx/module_xxx`，然后通过`subpackage_exp/modul_expAnalysisy`，以`from ..subpackage_xxx import module_XXX`来引用module_xxx。为了保持本项目的简洁，我就不实现这一情况了，读者可以自行尝试。