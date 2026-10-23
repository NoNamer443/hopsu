## Hopsu: An esolang

![Python 3.13](https://img.shields.io/badge/Python-3.13-blue)
![Auther: NoNamer443](https://img.shields.io/badge/Author-NoNamer443-orange)

~~写英文太累了，换成中文了。~~

### 名字来源

```py
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
- `~ N ( )`：当栈高不为N时循环（N为1个正整数）
- `#`到行尾：注释
- 由于作者的懒惰，每两个token之间必须有空白字符，以便split
