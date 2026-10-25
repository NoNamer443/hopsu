## Hopsu: An esolang

![Python 3.13](https://img.shields.io/badge/Python-3.13-blue)
![Auther: NoNamer443](https://img.shields.io/badge/Author-NoNamer443-orange)

~~写英文太累了，换成中文了。~~

### 名字来源

```python
"".join(sorted(set("pushpop")))
```

### 语法

整个语言在一个栈上

- `N`（数字）：压栈
- `^`：弹栈
- `?`：当栈顶为0时弹栈
- `+`：弹栈并将现在的栈顶加上原栈顶值
- `-`：弹栈并将现在的栈顶减去原栈顶值
- `,`：输入
- `.`：输出
- `~ H ( )`：当栈高不为`H`时循环（`H`为1个非负整数）
- `#`到行尾：注释
- 由于作者的懒惰，每两个token之间必须有空白字符，以便split

### 使用

正常使用：

```python
import hopsu
inter = hopsu.Hopsu()
inter.run("10 65 ~ 0 ( . )")
```

链式写法（避免字符串操作，但是要自己写循环）：

```py
import hopsu
inter = hopsu.Hopsu()
inter.push(10).push(65)
while len(inter) != 0:
    inter.output()
```

`inter.py`和`shell.py`是实现出来的简易工具，可以直接使用。
