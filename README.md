# Python分析指定微博用户粉丝僵尸粉

## 项目概要
起因是我一位认识的画师遭遇恶意塞粉。微博一天内被塞了2w个僵尸粉。观察后，我发现僵尸粉的微博数、关注数、粉丝数呈现一种比较线性相近的结果。我决定借此机会学习一下python获取粉丝数据并且分析僵尸粉的特征。

## 我的修改&代码使用方法

1. 请检查代码用的库，请自行使用`pip install`的方式安装
2. `weibo-lessget.py` 这个文件：
   - 请获取你当前的微博Cookie，填写在line 22，复制粘贴的时候请小心。cookie有时间和访问限制，请记得更换。
   - line 103处填写保存文件名
   -  line 118处填写粉丝uid列表的文件名
   -  line  142 143不影响程序运行，可以自己改成保存文件的位置
3. `userid.py` 
   -  line 49 ，填写被调查用户的oid （请使用浏览器开发者工具取得，注意不是uid）
   -   line 38，填写保存结果的文件位置。

## 设计思路

### 第一次搜集并分析样本

- [x] 使用 python_weiboSpider（https://github.com/rainpenber/python_weiboSpider） 抓取某人的粉丝列表，得到所有粉丝的uid。
- [x] 通过程序其中的Weibopr.py（已经修改代码）来得到所有uid对应的粉丝数、微博数、关注数，输出为一个txt列表。
- [x] 使用Python或者matlab分析抓取的数据，通过图形化，
- [ ] 分析出样本最密集的分布区域，确定僵尸粉的特征范围。确定阈值。
- [ ] 通过阈值重新筛选数据，得出僵尸粉列表。
- [ ] 使用weibo-dog-killer （https://github.com/overtrue/weibo-dogs-killer）批量拉黑。

### 处于僵尸粉正在新增状态（确定抓取的前n页全都是僵尸粉）

1. 使用 python_weiboSpider（https://github.com/rainpenber/python_weiboSpider） 抓取某人的粉丝列表，得到所有粉丝的uid。
2. 使用weibo-dog-killer （https://github.com/overtrue/weibo-dogs-killer）批量拉黑。


## 学习踩坑笔记

### python 语法细节踩坑
这里是我自己从网上出于自我学习的目的搜集的资料。我并不是以下部分文字的原创者。

#### python读写文件

##### 使用with open() as的方法

  实现代码如下

```python
with open('result/result.txt','a+') as infofile:
    infofile.write(head_text + '\n')
    infofile.close()
```

由于源程序只写入一次，所以他使用的是`wb` 即写入一次二进制文件。导致文件被重复擦写，数据丢失。

另外要带上`file.close()`，文件使用完毕后必须关闭，因为文件对象会占用操作系统的资源，并且操作系统同一时间能打开的文件数量也是有限的。

最为常见的三种模式，见下表，其中模式就是指获取文件对象时传入的参数，最常用的是前三个。  
| 模式 |                    描述                    |
| :--: | :----------------------------------------: |
|  r   |         仅读，待打开的文件必须存在         |
|  w   |     仅写，若文件已存在，内容将先被清空     |
|  a   |      仅写，若文件已存在，内容不会清空      |
|  r+  |         读写，待打开的文件必须存在         |
|  w+  |     读写，若文件已存在，内容将先被清空     |
|  a+  |      读写，若文件已存在，内容不会清空      |
|  rb  |     仅读，二进制，待打开的文件必须存在     |
|  wb  | 仅写，二进制，若文件已存在，内容将先被清空 |
|  ab  |  仅写，二进制，若文件已存在，内容不会清空  |
| r+b  |     读写，二进制，待打开的文件必须存在     |
| w+b  | 读写，二进制，若文件已存在，内容将先被清空 |
| a+b  |  读写，二进制，若文件已存在，内容不会清空  |

##### 使用codec.open的方法

由于python中默认的编码是ascii，如果直接使用open方法得到文件对象然后进行文件的读写，都将无法使用包含中文字符（以及其他非ascii码字符），因此建议使用utf-8编码。

- 读 :下面的代码读取了文件，将每一行的内容组成了一个列表。 

```python
import codecs
file = codecs.open('test.txt','r','utf-8')
lines = [line.strip() for line in file] 
file.close()
```

- 写：下面的代码写入了一行英文和一行中文到文件中。 

```python
import codecs
file = codecs.open('test.txt','w','utf-8')
file.write('Hello World!\n')
file.write('哈哈哈\n')
file.close()
```

#### python的循环

假设要对一个来源的文件遍历取值，python等更新的语言提供了一种循环方法：for each.

这里，原数据以每个一行的形式分布。那么自然是让文件按行依次读取。

```python
for current_id in read_f.readlines():
	if current_id == '':
    	break
```

#### \r和\n的区别

`\r`就是"回到行首"，`\n`就是"到下一行"

>在计算机还没有出现之前，有一种叫做电传打字机（Teletype Model 33）的玩意，每秒钟可以打10个字符。但是它有一个问题，就是打完一行换行的时候，要用去0.2秒，正好可以打两个字符。要是在这0.2秒里面，又有新的字符传过来，那么这个字符将丢失。
>
>于是，研制人员想了个办法解决这个问题，就是在每行后面加两个表示结束的字符。一个叫做**“回车”**，告诉打字机把打印头定位在左边界；另一个叫做**“换行”**，告诉打字机把纸向下移一行。
>
>这就是“换行”和“回车”的来历，从它们的英语名字上也可以看出一二。
>
>后来，计算机发明了，这两个概念也就被般到了计算机上。那时，存储器很贵，一些科学家认为在每行结尾加两个字符太浪费了，加一个就可以。于是，就出现了分歧。

- Unix系统里，每行结尾只有“**<换行>**”，即“`\n`”；
- Windows系统里面，每行结尾是“**<换行><回车>**”，即“`\n\r`”；
- Mac系统里，每行结尾是“**<回车>**”。

然而在本程序中，对`write`操作，如果使用\r\n，会导致写入两行。如果使用`codec.open()`，则是写入一行。不一样。

#### 读取行

python文件对象提供了三个“读”方法： read()、readline() 和 readlines()。每种方法可以接受一个变量以限制每次读取的数据量。

- read() 每次读取整个文件，它通常用于将文件内容放到一个字符串变量中。如果文件大于可用内存，为了保险起见，可以反复调用`read(size)`方法，每次最多读取size个字节的内容。
- readlines() 之间的差异是后者一次读取整个文件，象 .read() 一样。.readlines() 自动将文件内容分析成一个行的列表，该列表可以由 Python 的 for ... in ... 结构进行处理。
- readline() 每次只读取一行，通常比readlines() 慢得多。仅当没有足够内存可以一次读取整个文件时，才应该使用 readline()。

> **注意**：这三种方法是把每行末尾的'\n'也读进来了，它并不会默认的把'\n'去掉，需要我们手动去掉。

```python
with open('test1.txt', 'r') as f1:
    list1 = f1.readlines()
for i in range(0, len(list1)):
    list1[i] = list1[i].rstrip('\n')
```

如果直接使用`int()`转换方法的话，是会把`\n`消去的。本例比较特殊，输入的str就是数字，今后要注意。

#### 连接多行较长的语句 or 长句自动换行

python中较长的语句如果一行写不完可以用“\”来连接多行语句

在(),{},[] 中无需用“\”连接

```python
print('hello world,\
I am \
KangKang')
 
s = [1,2,3,
	4,5,6,
	7,8,9]
print(s)
```

结果：

```python
hello world，I am KangKang
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

- pycharm中设置自动换行的办法：
  - 只对当前文件有效的操作：菜单栏   ->   View   ->   Active Editor   ->   Use Soft Wraps；
  - 如果想对所有文件都有效，就要在setting里面进行操作：File   ->   Setting   ->   Editor   ->   General    ->   Use soft wraps in editor；

#### 几乎在任何文本编辑器里跳转到指定行的办法（多用于debug）

ctrl+g 就ok了

#### Python3中的最大整数和最大浮点数

考虑到这个问题，是因为考虑过用`int`是不是有一个值上限，如果说用`int()`方法转换str以后，变量放不下就尴尬了。所以调查了一下

###### Python中的最大整数

Python中可以通过sys模块来得到int的最大值. python2中使用的方法是

```python
import sys
max = sys.maxint
print (max)
```

python3中使用的方法是：

```python
import sys
max = sys.maxsize
print (max)
```

###### Python中获得最大浮点数

- 方法一：使用sys模块

```python
>>> import sys
>>> sys.float_info
sys.floatinfo(max=1.7976931348623157e+308, max_exp=1024, max_10_exp=308, min=2.2
250738585072014e-308, min_exp=-1021, min_10_exp=-307, dig=15, mant_dig=53, epsil
on=2.2204460492503131e-16, radix=2, rounds=1)
>>> sys.float_info.max
1.7976931348623157e+308
```

- 方法二：使用float函数

```py
>>> infinity = float("inf")
>>> infinity
inf
>>> infinity / 10000
inf
```

