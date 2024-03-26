# Bash
This is a reading note for [Bash 脚本教程](https://wangdoc.com/bash/) 
## Bash 提供很多快捷键，可以大大方便操作。
* Ctrl + L：清除屏幕并将当前行移到页面顶部。
* Ctrl + C：中止当前正在执行的命令。
* Shift + PageUp：向上滚动。
* Shift + PageDown：向下滚动。
* Ctrl + U：从光标位置删除到行首。
* Ctrl + K：从光标位置删除到行尾。
* Ctrl + W：删除光标位置前一个单词。
* Ctrl + D：关闭 Shell 会话。
* ↑，↓：浏览已执行命令的历史记录。

## 八种扩展
* 波浪线扩展，`~` 代表用户主目录
* ?字符扩展, ?字符代表文件路径里面的任意单个字符，不包括空字符。
* *字符扩展, *字符代表文件路径里面的任意数量的任意字符，包括零个字符。如果要匹配隐藏文件，需要写成.*。
* 方括号扩展，[ab]可以匹配a或b，前提是确实存在相应的文件。[^...]和[!...]。它们表示匹配不在方括号里面的字符，这两种写法是等价的。[0-9]匹配[0123456789]。
    * [a-z]：所有小写字母。
    * [a-zA-Z]：所有小写字母与大写字母。
    * [a-zA-Z0-9]：所有小写字母、大写字母与数字。
    * [abc]*：所有以a、b、c字符之一开头的文件名。
    * program.[co]：文件program.c与文件program.o。
    * BACKUP.[0-9][0-9][0-9]：所有以BACKUP.开头，后面是三个数字的文件名。
* 大括号扩展，echo d{a,e,i,u,o}g = dag deg dig dug dog。大括号内部的逗号前后不能有空格，否则，大括号扩展会失效。
    * a.log{,.bak}等同于a.log 和a.log.bak。
    * {j{p,pe}g,png} = jpg jpeg png
    * 嵌套 a{A{1,2},B{3,4}}b = aA1b aA2b aB3b aB4b
    * echo /bin/{cat,b*} = echo /bin/cat;echo /bin/b* 会先进行大括号扩展，然后进行*扩展，等同于执行两条echo命令。
    * 由于大括号扩展{...}不是文件名扩展，所以它总是会扩展的。这与方括号扩展[...]完全不同，如果匹配的文件不存在，方括号就不会扩展。
    * echo d{a..d}g = dag dbg dcg ddg
    * echo .{mp{3..4},m4{a,b,p,v}} = .mp3 .mp4 .m4a .m4b .m4p .m4v
    * mkdir {2007..2009}-{01..12}  命令会新建36个子目录，每个子目录的名字都是”年份-月份“。
    * echo {001..5} = 001 002 003 004 005
    * echo {0..8..2} = 0 2 4 6 8 增加步长参数在末尾。
    * echo {a..c}{1..3} = a1 a2 a3 b1 b2 b3 c1 c2 c3
* 变量扩展，
    * echo $SHELL = echo ${SHELL}
    * ${!string*}或${!string@}返回所有匹配给定字符串string的变量名。
* 子命令扩展，$(...)可以扩展成另一个命令的运行结果，该命令的所有输出都会作为返回值。
    * echo $(date) = Wed Mar 20 22:15:26 CST 2024 = echo `date`
    * $(ls $(pwd)) 可以嵌套
    * echo $(ls `pwd`)
* 算术扩展，echo $((2 + 2)) = 4

## 字符类
    * [[:alnum:]]：匹配任意英文字母与数字
    * [[:alpha:]]：匹配任意英文字母
    * [[:blank:]]：空格和 Tab 键。
    * [[:cntrl:]]：ASCII 码 0-31 的不可打印字符。
    * [[:digit:]]：匹配任意数字 0-9。
    * [[:graph:]]：A-Z、a-z、0-9 和标点符号。
    * [[:lower:]]：匹配任意小写字母 a-z。
    * [[:print:]]：ASCII 码 32-127 的可打印字符。
    * [[:punct:]]：标点符号（除了 A-Z、a-z、0-9 的可打印字符）。
    * [[:space:]]：空格、Tab、LF（10）、VT（11）、FF（12）、CR（13）。
    * [[:upper:]]：匹配任意大写字母 A-Z。
    * [[:xdigit:]]：16进制字符（A-F、a-f、0-9）。
## 量词语法
量词语法用来控制模式匹配的次数。它只有在 Bash 的extglob参数打开的情况下才能使用
````
* Franks-Mac:mygithub frank$ shopt extglob
* extglob        	off
* Franks-Mac:mygithub frank$ ls abc?(.)txt
* -bash: syntax error near unexpected token `('
* Franks-Mac:mygithub frank$ shopt -s extglob
* Franks-Mac:mygithub frank$ shopt extglob
* extglob        	on
* Franks-Mac:mygithub frank$ ls abc?(.)txt
* ls: abc?(.)txt: No such file or directory
````
- ?(pattern-list)：模式匹配零次或一次。
- *(pattern-list)：模式匹配零次或多次。
- +(pattern-list)：模式匹配一次或多次。
- @(pattern-list)：只匹配一次模式。
- !(pattern-list)：匹配给定模式以外的任何内容。

## shopt
```commandline
# 打开某个参数
$ shopt -s [optionname]

# 关闭某个参数
$ shopt -u [optionname]

# 查询某个参数关闭还是打开
$ shopt [optionname]
```
## 引号和转义
Bash 只有一种数据类型，就是字符串。
### 转义
反斜杠除了用于转义，还可以表示一些不可打印的字符。
````
\a：响铃
\b：退格
\n：换行
\r：回车
\t：制表符
````
如果想要在命令行使用这些不可打印的字符，可以把它们放在引号里面，然后使用echo命令的-e参数。
```commandline
$ echo a\tb
atb

$ echo -e "a\tb"
a        b

```
### 单引号
Bash 允许字符串放在单引号或双引号之中，加以引用。
```commandline
# 不正确
$ echo it's

# 不正确
$ echo 'it\'s'

# 正确
$ echo $'it\'s'

$ echo "it's"
it's

Franks-Mac:bash frank$ echo 'it\'s'
> 
```

### 双引号
双引号比单引号宽松，大部分特殊字符在双引号里面，都会失去特殊含义，变成普通字符。
但是，三个特殊字符除外：美元符号（$）、反引号（`）和反斜杠（\）。这三个字符在双引号之中，依然有特殊含义，会被 Bash 自动扩展。

```commandline
Franks-Mac:bash frank$ echo "$SHELL"
/bin/bash
Franks-Mac:bash frank$ echo "`date`"
Thu Mar 21 06:47:57 CST 2024

```
换行符在双引号之中，会失去特殊含义，Bash 不再将其解释为命令的结束，只是作为普通的换行符。所以可以利用双引号，在命令行输入多行文本。

文件名包含空格。这时就必须使用双引号（或单引号），将文件名放在里面。
`$ ls "two words.txt"`

双引号还有一个作用，就是保存原始命令的输出格式。
```commandline
Franks-Mac:reading frank$ echo $(ls )
total 8 drwxr-xr-x 3 frank staff 96 Apr 17 2022 2022年4月14日夜記 drwxr-3 frank staff 96 Mar 11 21:11 A-Philosophy-of-Software-Design -rw-r--r-- 1 frank staff 354 Mar 10 16:20 README.md drwxr-xr-x 3 frank staff 96 Mar 21 06:52 bash drwxr-xr-x 3 frank staff 96 Jul 26 2021 万万没想到 drwxr 3 frank staff 96 May 15 2020 小窗幽记-長者之言 drwxr-xr-x 3 frank staff14 2019 断舍离
Franks-Mac:reading frank$ echo "$(ls )"
total 8
drwxr-xr-x  3 frank  staff   96 Apr 17  2022 2022年4月14日夜記
drwxr-xr-x  3 frank  staff   96 Mar 11 21:11 A-Philosophy-of-Software-Design
-rw-r--r--  1 frank  staff  354 Mar 10 16:20 README.md
drwxr-xr-x  3 frank  staff   96 Mar 21 06:52 bash
drwxr-xr-x  3 frank  staff   96 Jul 26  2021 万万没想到
drwxr-xr-x  3 frank  staff   96 May 15  2020 小窗幽记-長者之言
drwxr-xr-x  3 frank  staff   96 Aug 14  2019 断舍离

Franks-Mac:reading frank$ echo $(cal)
March 2024 Su Mo Tu We Th Fr Sa 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
Franks-Mac:reading frank$ echo "$(cal)"
     March 2024       
Su Mo Tu We Th Fr Sa  
                1  2  
 3  4  5  6  7  8  9  
10 11 12 13 14 15 16  
17 18 19 20 21 22 23  
24 25 26 27 28 29 30  
31                    
Franks-Mac:reading frank$ echo '$(cal)'
$(cal)
Franks-Mac:reading frank$ echo $'(cal)'
(cal)
Franks-Mac:reading frank$ echo $"(cal)"
(cal)

```
### Here document
Here 文档的本质是重定向，它将字符串重定向输出给某个命令，相当于包含了echo命令。
````
$ command << token
string
token

# 等同于
$ echo string | command
````

Here 字符串只适合那些可以接受标准输入作为参数的命令，对于其他命令无效

```commandline
Franks-Mac:reading frank$ md5sum <<< 'helloworld'
d73b04b0e696b0945283defa3eee4538  -

```
md5sum命令只能接受标准输入作为参数，不能直接将字符串放在命令后面，会被当作文件名，即md5sum ddd里面的ddd会被解释成文件名。
这时就可以用 Here 字符串，将字符串传给md5sum命令。

## 变量
变量声明的语法如下。等号两边不能有空格。
`variable=value`

如果同一行定义多个变量，必须使用分号（;）分隔。
`$ foo=1;bar=2`

### 读取变量
读取变量的时候，直接在变量名前加上$就可以了。

每当 Shell 看到以$开头的单词时，就会尝试读取这个变量名对应的值。
如果变量不存在，Bash 不会报错，而会输出空字符。

读取变量的时候，变量名也可以使用花括号{}包围，比如$a也可以写成${a}。这种写法可以用于变量名与其他字符连用的情况。
```commandline
$ a=foo
$ echo $a_file

$ echo ${a}_file
foo_file
```

如果变量的值本身也是变量，可以使用${!varname}的语法，读取最终的值。
```commandline
Franks-Mac:reading frank$ home=HOME
Franks-Mac:reading frank$ echo home
home
Franks-Mac:reading frank$ echo $home
HOME
Franks-Mac:reading frank$ echo ${!home}
/Users/frank
```

如果变量值包含连续空格（或制表符和换行符），最好放在双引号里面读取。
```commandline
Franks-Mac:reading frank$ a="1  2  3"
Franks-Mac:reading frank$ echo $a
1 2 3
Franks-Mac:reading frank$ echo "$a"
1  2  3
```
变量a的值包含两个连续空格。如果直接读取，Shell 会将连续空格合并成一个。只有放在双引号里面读取，才能保持原来的格式。

### 删除变量
unset命令用来删除一个变量。 `unset NAME`
```commandline
Franks-Mac:reading frank$ echo $b

Franks-Mac:reading frank$ unset b
Franks-Mac:reading frank$ echo $a
1 2 3
Franks-Mac:reading frank$ unset a
Franks-Mac:reading frank$ echo $a
```
不存在的 Bash 变量一律等于空字符串

### export 变量
用户创建的变量仅可用于当前 Shell，子 Shell 默认读取不到父 Shell 定义的变量。为了把变量传递给子 Shell，需要使用export命令。
这样输出的变量，对于子 Shell 来说就是环境变量。
```commandline
NAME=foo
export NAME

export NAME=value
```

### 特殊变量
- $?为上一个命令的退出码，用来判断上一个命令是否执行成功。返回值是0，表示上一个命令执行成功；如果不是零，表示上一个命令执行失败。
```commandline
Franks-Mac:reading frank$ echo $a
love
Franks-Mac:reading frank$ echo $?
0
Franks-Mac:reading frank$ a
bash: a: command not found
Franks-Mac:reading frank$ echo $?
127
Franks-Mac:reading frank$ ls hh
ls: hh: No such file or directory
Franks-Mac:reading frank$ echo $?
1
```

- $$为当前 Shell 的进程 ID。
这个特殊变量可以用来命名临时文件。
`LOGFILE=/tmp/output_log.$$`

- $!为最近一个后台执行的异步命令的进程 ID。

- $0为当前 Shell 的名称（在命令行直接执行时）或者脚本名（在脚本中执行时）。
````
Franks-Mac:reading frank$ echo $0
/bin/bash
````

### Bash 提供四个特殊语法，跟变量的默认值有关，目的是保证变量不为空。
- `${varname:-word}` 如果变量varname存在且不为空，则返回它的值，否则返回word。它的目的是返回一个默认值，
  比如${count:-0}表示变量count不存在时返回0。
- `${varname:=word}` 如果变量varname存在且不为空，则返回它的值，否则将它设为word，并且返回word。它的目的是设置变量的默认值，
  比如${count:=0}表示变量count不存在时返回0，且将count设为0。
- `${varname:+word}` 如果变量名存在且不为空，则返回word，否则返回空值。它的目的是测试变量是否存在，
  比如${count:+1}表示变量count存在时返回1（表示true），否则返回空值。
- `${varname:?message}` 如果变量varname存在且不为空，则返回它的值，否则打印出varname: message，并中断脚本的执行。
  如果省略了message，则输出默认的信息“parameter null or not set.”。它的目的是防止变量未定义，
  比如${count:?"undefined!"}表示变量count未定义时就中断执行，抛出错误，返回给定的报错信息undefined!。

上面四种语法如果用在脚本中，变量名的部分可以用数字1到9，表示脚本的参数。

`filename=${1:?"filename missing."}`
1表示脚本的第一个参数。如果该参数不存在，就退出脚本并报错。

## 字符串的操作
获取字符串长度的语法如下。

`${#varname}`

```commandline
Franks-Mac:reading frank$ echo ${home}
HOME
Franks-Mac:reading frank$ echo ${!home}
/Users/frank
Franks-Mac:reading frank$ echo ${#home}
4
Franks-Mac:reading frank$ echo ${#HOME}
12
```
### 子字符串
字符串提取子串的语法如下。

`${varname:offset:length}`

```commandline
$ count=frogfootman
$ echo ${count:4:4}
foot
```
这种语法不能直接操作字符串，只能通过变量来读取字符串，并且不会改变原始字符串。

如果省略length，则从位置offset开始，一直返回到字符串的结尾。

如果offset为负值，表示从字符串的末尾开始算起。注意，负数前面必须有一个空格， 以防止与${variable:-word}的变量的设置默认值语法混淆。
这时还可以指定length，length可以是正值，也可以是负值（负值不能超过offset的长度）。
```commandline
$ foo="This string is long."
$ echo ${foo: -5}
long.
$ echo ${foo: -5:2}
lo
$ echo ${foo: -5:-2}
lon
Franks-Mac:reading frank$ echo ${foo:-5}
this string is long.
```

### 搜索匹配和替换
#### 字符串头部的模式匹配。
```commandline
# 如果 pattern 匹配变量 variable 的开头，
# 删除最短匹配（非贪婪匹配）的部分，返回剩余部分
${variable#pattern}

# 如果 pattern 匹配变量 variable 的开头，
# 删除最长匹配（贪婪匹配）的部分，返回剩余部分
${variable##pattern}
```
例子，注意返回的是被删除匹配字符串之后剩余的部分。
```commandline
Franks-Mac:reading frank$ mypath=$PWD
Franks-Mac:reading frank$ echo $mypath
/Users/frank/play/mygithub/reading
Franks-Mac:reading frank$ echo ${mypath#/*/}
frank/play/mygithub/reading
Franks-Mac:reading frank$ echo ${mypath##/*/}
reading
Franks-Mac:reading frank$ echo ${mypath#/*}
Users/frank/play/mygithub/reading
Franks-Mac:reading frank$ echo ${mypath##/*}

```
上面例子中，匹配的模式是/*/，其中*可以匹配任意数量的字符，所以最短匹配是/home/，最长匹配是/home/cam/book/

#### 字符串尾部的模式匹配
```commandline
# 如果 pattern 匹配变量 variable 的结尾，
# 删除最短匹配（非贪婪匹配）的部分，返回剩余部分
${variable%pattern}

# 如果 pattern 匹配变量 variable 的结尾，
# 删除最长匹配（贪婪匹配）的部分，返回剩余部分
${variable%%pattern}
```
删除路径的文件名部分，只留下目录部分。
```commandline
$ path=/home/cam/book/long.file.name
$ echo ${path%/*}
/home/cam/book
```
替换文件的后缀名。
```commandline
$ file=foo.png
$ echo ${file%.png}.jpg
foo.jpg
```

#### 任意位置的替换
```commandline
# 如果 pattern 匹配变量 variable 的一部分，
# 最长匹配（贪婪匹配）的那部分被 string 替换，但仅替换第一个匹配
${variable/pattern/string}

# 如果 pattern 匹配变量 variable 的一部分，
# 最长匹配（贪婪匹配）的那部分被 string 替换，所有匹配都替换
${variable//pattern/string}
```
最少替换，${var/pattern/pattern}表示将var字符串的第一个匹配的pattern替换为另一个pattern。
```commandline
Franks-Mac:reading frank$ echo ${mypath/frank/tom}
/Users/tom/play/mygithub/reading
```
全局替换，${var//pattern/pattern}表示将var字符串中的所有能匹配的pattern替换为另一个pattern。
```commandline
Franks-Mac:reading frank$ echo ${mypath////#}
#Users#frank#play#mygithub#reading
```
//全局匹配，替换/为#

如果省略了string部分，那么就相当于匹配的部分替换成空字符串，即删除匹配的部分。
```commandline
Franks-Mac:reading frank$ echo ${mypath/reading/}
/Users/frank/play/mygithub/
```

#### 改变大小写
```commandline
# 转为大写
${varname^^}

# 转为小写
${varname,,}
```

## 算术表达式
```commandline
$ ((foo = 5 + 5))
$ echo $foo
10
```
这个语法不返回值，命令执行的结果根据算术运算的结果而定。只要算术结果不是0，命令就算执行成功。
```commandline
Franks-Mac:reading frank$  (3-3)
bash: 3-3: command not found
Franks-Mac:reading frank$ echo $?
127
Franks-Mac:reading frank$ ((3-3))
Franks-Mac:reading frank$ echo $?
1
Franks-Mac:reading frank$ ((3+3))
Franks-Mac:reading frank$ echo $?
0
```

如果要读取算术运算的结果，需要在((...))前面加上美元符号$((...))，使其变成算术表达式，返回算术运算的值。

((...))语法支持的算术运算符如下。
````
+：加法
-：减法
*：乘法
/：除法（整除）
%：余数
**：指数
++：自增运算（前缀或后缀）
--：自减运算（前缀或后缀）
````
### 数值的进制
````commandline
number：没有任何特殊表示法的数字是十进制数（以10为底）。
0number：八进制数。
0xnumber：十六进制数。
base#number：base进制的数。
````
### 位运算
```commandline
<<：位左移运算，把一个数字的所有位向左移动指定的位。
>>：位右移运算，把一个数字的所有位向右移动指定的位。
&：位的“与”运算，对两个数字的所有位执行一个AND操作。
|：位的“或”运算，对两个数字的所有位执行一个OR操作。
~：位的“否”运算，对一个数字的所有位取反。
^：位的异或运算（exclusive or），对两个数字的所有位执行一个异或操作。
```
### 逻辑运算
```commandline
<：小于
>：大于
<=：小于或相等
>=：大于或相等
==：相等
!=：不相等
&&：逻辑与
||：逻辑或
!：逻辑否
expr1?expr2:expr3：三元条件运算符。若表达式expr1的计算结果为非零值（算术真），则执行表达式expr2，否则执行表达式expr3。
```
如果逻辑表达式为真，返回1，否则返回0。

## History
```commandline
Franks-Mac:mygithub frank$ echo $HISTFILE
/Users/frank/.bash_sessions/BF4E38FB-0623-47F1-B547-F80EE6B62A85.historynew

# in goland terminal
Franks-Mac:reading frank$ echo $HISTFILE
/Users/frank/Library/Caches/JetBrains/GoLand2022.3/terminal/history/reading-history

```

`history | grep /usr/bin`
上面命令返回.bash_history文件里面，那些包含/usr/bin的命令。

### History 相关环境变量
#### HISTTIMEFORMAT
```commandline
Franks-Mac:reading frank$ export HISTTIMEFORMAT='%F %T '
Franks-Mac:reading frank$ history 5
 4630  2024-03-22 10:49:59 echo $HISTTIMEFORMAT
 4631  2024-03-22 10:51:16 export HISTTIMEFORMAT='%F %T'
 4632  2024-03-22 10:51:23 history 10
 4633  2024-03-22 10:52:04 export HISTTIMEFORMAT='%F %T '
 4634  2024-03-22 10:52:09 history 5

```
%F相当于%Y - %m - %d（年-月-日），%T相当于%H : %M : %S（时:分:秒）

#### HISTSIZE
环境变量HISTSIZE设置保存历史操作的数量。
`$ export HISTSIZE=10000`
上面命令设置保存过去10000条操作历史。

#### HISTIGNORE
环境变量HISTIGNORE可以设置哪些命令不写入操作历史。
```commandline
echo $HISTIGNORE
&:[ ]*:exit
```
`export HISTIGNORE='pwd:ls:exit'`
上面示例设置，pwd、ls、exit这三个命令不写入操作历史。

### Ctrl+r
输入命令时，按下Ctrl + r快捷键，就可以搜索操作历史，选择以前执行过的命令。

Ctrl + r相当于打开一个.bash_history文件的搜索接口，直接键入命令的开头部分，Shell 就会自动在该文件中反向查询（即先查询最近的命令），
显示最近一条匹配的结果，这时按下回车键，就会执行那条命令。

### !命令

```commandline
Franks-Mac:reading frank$ !!
history 5
 4636  2024-03-22 10:56:55 vi /etc/bashrc
 4637  2024-03-22 10:57:23 vi /etc/bashrc_Apple_Terminal 
 4638  2024-03-22 11:00:39 echo $HISTIGNORE
 4639  2024-03-22 11:02:13 vi ~/.bash_profile 
 4640  2024-03-22 11:04:49 history 5
 
 # 知道了命令的行号以后，可以用感叹号 + 行号执行该命令。
Franks-Mac:reading frank$ !4640
history 5
 4636  2024-03-22 10:56:55 vi /etc/bashrc
 4637  2024-03-22 10:57:23 vi /etc/bashrc_Apple_Terminal 
 4638  2024-03-22 11:00:39 echo $HISTIGNORE
 4639  2024-03-22 11:02:13 vi ~/.bash_profile 
 4640  2024-03-22 11:04:49 history 5
 
 # 想执行本次 Shell 对话中倒数的命令
Franks-Mac:reading frank$ !-1
history 5
 4636  2024-03-22 10:56:55 vi /etc/bashrc
 4637  2024-03-22 10:57:23 vi /etc/bashrc_Apple_Terminal 
 4638  2024-03-22 11:00:39 echo $HISTIGNORE
 4639  2024-03-22 11:02:13 vi ~/.bash_profile 
 4640  2024-03-22 11:04:49 history 5

```
#### ! + 搜索词
感叹号 + 搜索词可以快速执行匹配的命令，倒序搜索，执行最先匹配的命令。
```commandline
Franks-Mac:reading frank$ !echo
echo $HISTIGNORE
&:[ ]*:exit

```
注意，感叹号 + 搜索词语法只会匹配命令，不会匹配参数

#### 其他
!? + 搜索词可以搜索命令的任意部分，包括参数部分。

!$代表上一个命令的最后一个参数，它的另一种写法是$_。

!*代表上一个命令的所有参数，即除了命令以外的所有部分。

如果想匹配上一个命令的某个指定位置的参数，使用!:n。

如果只是想输出上一条命令，而不是执行它，可以使用!:p

如果想输出最近一条匹配的命令，而不执行它，可以使用!<命令>:p。

## Bash 行操作
Bash 内置了 Readline 库，具有这个库提供的很多“行操作”功能，比如命令的自动补全
```commandline
$ set -o vi

$ set -o emacs
```
如果想永久性更改编辑模式（Emacs / Vi），可以将命令写在~/.inputrc文件，这个文件是 Readline 的配置文件。
````
set editing-mode vi
````
### 光标移动
```commandline
Ctrl + a：移到行首。
Ctrl + e：移到行尾。
Alt + f：移动到当前单词的词尾。
Alt + b：移动到当前单词的词首。
Alt + <：向左移动到当前单词的词首
Alt + >：向右移动到当前单词的词尾
Ctrl + b：向行首移动一个字符，与左箭头作用相同。
Ctrl + f：向行尾移动一个字符，与右箭头作用相同。
```

### 编辑操作
```commandline
Ctrl + d：删除光标位置的字符（delete）。
Ctrl + w：删除光标前面的单词。
Ctrl + t：光标位置的字符与它前面一位的字符交换位置（transpose）。
Alt + t：光标位置的词与它前面一位的词交换位置（transpose）。
Alt + l：将光标位置至词尾转为小写（lowercase）。
Alt + u：将光标位置至词尾转为大写（uppercase）。
使用Ctrl + d的时候，如果当前行没有任何字符，会导致退出当前 Shell，所以要小心。

剪切和粘贴快捷键如下。

Ctrl + k：剪切光标位置到行尾的文本。
Ctrl + u：剪切光标位置到行首的文本。
Alt + d：剪切光标位置到词尾的文本。
Alt + Backspace：剪切光标位置到词首的文本。
Ctrl + y：在光标位置粘贴文本。
```
### 自动补全
除了命令或路径，Tab 还可以补全其他值。
如果一个值以$开头，则按下 Tab 键会补全变量；
如果以~开头，则补全用户名；
如果以@开头，则补全主机名（hostname），主机名以列在/etc/hosts文件里面的主机为准。
```commandline
Tab：完成自动补全。
Alt + ?：列出可能的补全，与连按两次 Tab 键作用相同。
Alt + /：尝试文件路径补全。
Alt + !：命令补全。
Alt + .：插入上一个命令的最后一个词。
上面的Alt + .快捷键，对于很长的文件路径，有时会非常方便。因为 Unix 命令的最后一个参数通常是文件路径。

```

## Bash 脚本入门
这一行以#!字符开头，这个字符称为 Shebang，所以这一行就叫做 Shebang 行。

#!后面就是脚本解释器的位置，Bash 脚本的解释器一般是/bin/sh或/bin/bash。
````
#!/bin/sh
# 或者
#!/bin/bash
````
如果 Bash 解释器不放在目录/bin，脚本就无法执行了。为了保险，可以写成下面这样。

`#!/usr/bin/env bash`
```commandline
Franks-Mac:reading frank$ env bash

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
bash-3.2$ 
Franks-Mac:reading frank$ which bash
/bin/bash

```
Shebang 行不是必需的，但是建议加上这行。如果缺少该行，就需要手动将脚本传给解释器。举例来说，脚本是script.sh，有 Shebang 行的时候，可以直接调用执行。
`$ ./script.sh`

如果没有 Shebang 行，就只能手动将脚本传给解释器来执行。
````
$ /bin/sh ./script.sh
# 或者
$ bash ./script.sh
````

### 执行权限
```commandline
# 给所有用户执行权限
$ chmod +x script.sh

# 给所有用户读权限和执行权限
$ chmod +rx script.sh
# 或者
$ chmod 755 script.sh

# 只给脚本拥有者读权限和执行权限
$ chmod u+rx script.sh
```
除了执行权限，脚本调用时，一般需要指定脚本的路径（比如path/script.sh）。
如果将脚本放在环境变量$PATH指定的目录中，就不需要指定路径了。

```
export PATH=$PATH:~/bin
$ source ~/.bashrc
```

### env
#!/usr/bin/env NAME这个语法的意思是，让 Shell 查找$PATH环境变量里面第一个匹配的NAME。
如果你不知道某个命令的具体路径，或者希望兼容其他用户的机器，这样的写法就很有用。

/usr/bin/env bash的意思就是，返回bash可执行文件的位置，前提是bash的路径是在$PATH里面。
```commandline
Franks-Mac:reading frank$ env node
Welcome to Node.js v21.7.1.
Type ".help" for more information.
> 
```

其他脚本文件也可以使用这个命令。比如 Node.js 脚本的 Shebang 行，可以写成下面这样。

`#!/usr/bin/env node`

### 脚本参数
脚本文件内部，可以使用特殊变量，引用这些参数。
````
$0：脚本文件名，即script.sh。
$1~$9：对应脚本的第一个参数到第九个参数。
如果脚本的参数多于9个，那么第10个参数可以用${10}的形式引用，以此类推。
$#：参数的总数。
$@：全部的参数，参数之间使用空格分隔。
$*：全部的参数，参数之间使用变量$IFS值的第一个字符分隔，默认为空格，但是可以自定义。
````
注意，如果命令是command -o foo bar，那么-o是$1，foo是$2，bar是$3。

```commandline
#!/bin/bash
# script.sh

echo "全部参数：" $@
echo "命令行参数数量：" $#
echo '$0 = ' $0
echo '$1 = ' $1
echo '$2 = ' $2
echo '$3 = ' $3
```
```commandline
$ ./script.sh a b c
全部参数：a b c
命令行参数数量：3
$0 =  script.sh
$1 =  a
$2 =  b
$3 =  c
```
用户可以输入任意数量的参数，利用for循环，可以读取每一个参数。
````
#!/bin/bash

for i in "$@"; do
echo $i
done
````
### 命令执行结果
命令执行结束后，会有一个返回值。0表示执行成功，非0（通常是1）表示执行失败。
环境变量$?可以读取前一个命令的返回值。
```commandline
cd /path/to/somewhere
if [ "$?" = "0" ]; then
  rm *
else
  echo "无法切换目录！" 1>&2
  exit 1
fi
```
由于if可以直接判断命令的执行结果，执行相应的操作，上面的脚本可以改写成下面的样子。
```commandline
if cd /path/to/somewhere; then
  rm *
else
  echo "Could not change directory! Aborting." 1>&2
  exit 1
fi
```
更简洁的写法是利用两个逻辑运算符&&（且）和||（或）。
```commandline
# 第一步执行成功，才会执行第二步
cd /path/to/somewhere && rm *

# 第一步执行失败，才会执行第二步
cd /path/to/somewhere || exit 1
```

### source 命令
source命令用于执行一个脚本，通常用于重新加载一个配置文件。

source命令最大的特点是在当前 Shell 执行脚本，不像直接执行脚本时，会新建一个子 Shell，也就导致子 Shell 缺少父 Shell 环境变量。
所以，source命令执行脚本时，不需要export变量。

`Franks-Mac:reading frank$ vi test_source.sh`
```commandline
#!/bin/bash
# test.sh
echo $foo
```
```commandline

Franks-Mac:reading frank$ foo=12
Franks-Mac:reading frank$ bash test_source.sh 

Franks-Mac:reading frank$ sh test_source.sh 

Franks-Mac:reading frank$ source test_source.sh 
12
```
上面例子中，当前 Shell 的变量foo并没有export，所以直接执行无法读取，但是source执行可以读取。

source命令的另一个用途，是在脚本内部加载外部库。
```commandline
#!/bin/bash

source ./lib.sh
function_from_lib
```
source有一个简写形式，可以使用一个点（.）来表示。
```
Franks-Mac:reading frank$ . test_source.sh 
12
```

### 别名，alias 命令
有时为了防止误删除文件，可以指定rm命令的别名。
````
$ alias rm='rm -i'
````
上面命令指定rm命令是rm -i，每次删除文件之前，都会让用户确认。

直接调用alias命令，可以显示所有别名。
````
$ alias
````
unalias命令可以解除别名。
````
$ unalias lt
````

## read 命令
````
read [-options] [variable...]
````
上面语法中，options是参数选项，variable是用来保存输入数值的一个或多个变量名。
```commandline
#!/bin/bash

echo -n "输入一些文本 > "
read text
echo "你的输入：$text"
```
```commandline
$ bash demo.sh
输入一些文本 > 你好，世界
你的输入：你好，世界
```
read可以接受用户输入的多个值。
```commandline
#!/bin/bash
echo Please, enter your firstname and lastname
read FN LN
echo "Hi! $LN, $FN !"
```
如果用户的输入项少于read命令给出的变量数目，那么额外的变量值为空。如果用户的输入项多于定义的变量，那么多余的输入项会包含到最后一个变量中。

```
#!/bin/bash

filename='/etc/hosts'

while read myline
do
echo "$myline"
done < $filename
```
上面的例子通过read命令，读取一个文件的内容。done命令后面的定向符<，将文件内容导向read命令，每次读取一行，存入变量myline，直到文件读取完毕。

## 条件判断
```commandline
if commands; then
  commands
[elif commands; then
  commands...]
[else
  commands]
fi

```
if、elif和else。其中，后两个部分是可选的。

除了多行的写法，if结构也可以写成单行。
```commandline
$ if true; then echo 'hello world'; fi
hello world
```

注意，if关键字后面也可以是一条命令，该条命令执行成功（返回值0），就意味着判断条件成立。
```commandline
$ if echo 'hi'; then echo 'hello world'; fi
hi
hello world
Franks-Mac:reading frank$ if notexit; then echo 'hello world'; fi
bash: notexit: command not found
Franks-Mac:reading frank$ notexit
bash: notexit: command not found
Franks-Mac:reading frank$ if $?; then echo 'last command execute successfully'; fi
bash: 127: command not found
Franks-Mac:reading frank$ echo $?
0
Franks-Mac:reading frank$ notexit
bash: notexit: command not found
Franks-Mac:reading frank$ echo $?
127
Franks-Mac:reading frank$ echo $?
0

```
这一点与其他语言（例如Python）的真假值判断相反，其他语言非0就是为真。

### test 命令
if结构的判断条件，一般使用test命令，有三种形式。
````
# 写法一
test expression

# 写法二
[ expression ]

# 写法三
[[ expression ]]
````
上面的expression是一个表达式。这个表达式为真，test命令执行成功（返回值为0）；表达式为伪，test命令执行失败（返回值为1）。
注意，第二种和第三种写法，[和]与内部的表达式之间必须有空格。

if表达式 = 两端需要留空白
```commandline
Franks-Mac:reading frank$ if test $USER="foo"; then echo "Hello foo"; fi
Hello foo
Franks-Mac:reading frank$ echo $USER
frank
Franks-Mac:reading frank$ if test $USER = "foo"; then echo "Hello foo"; fi
Franks-Mac:reading frank$ if test $USER = "frank"; then echo "Hello frank"; fi
Hello frank

```
```commandline
# 写法一
if test -e /tmp/foo.txt ; then
  echo "Found foo.txt"
fi

# 写法二
if [ -e /tmp/foo.txt ] ; then
  echo "Found foo.txt"
fi

# 写法三
if [[ -e /tmp/foo.txt ]] ; then
  echo "Found foo.txt"
fi
```

### test 的参数说明 output of `man test`
```commandline
     -d file       True if file exists and is a directory.

     -e file       True if file exists (regardless of type).

     -f file       True if file exists and is a regular file.

     -g file       True if file exists and its set group ID flag is set.

     -h file       True if file exists and is a symbolic link.  This operator
                   is retained for compatibility with previous versions of
                   this program.  Do not rely on its existence; use -L
                   instead.

     -k file       True if file exists and its sticky bit is set.

     -n string     True if the length of string is nonzero.

     -p file       True if file is a named pipe (FIFO).

     -r file       True if file exists and is readable.

     -s file       True if file exists and has a size greater than zero.

```

```commandline
#!/bin/bash

FILE=~/.bashrc

if [ -e "$FILE" ]; then
  if [ -f "$FILE" ]; then
    echo "$FILE is a regular file."
  fi
  if [ -d "$FILE" ]; then
    echo "$FILE is a directory."
  fi
  if [ -r "$FILE" ]; then
    echo "$FILE is readable."
  fi
  if [ -w "$FILE" ]; then
    echo "$FILE is writable."
  fi
  if [ -x "$FILE" ]; then
    echo "$FILE is executable/searchable."
  fi
else
  echo "$FILE does not exist"
  exit 1
fi
```
上面代码中，$FILE要放在双引号之中，这样可以防止变量$FILE为空，从而出错。因为$FILE如果为空，这时[ -e $FILE ]就变成[ -e ]，这会被判断为真。
而$FILE放在双引号之中，[ -e "$FILE" ]就变成[ -e "" ]，这会被判断为伪。

### 字符串判断
```commandline
[ string ]：如果string不为空（长度大于0），则判断为真。
[ -n string ]：如果字符串string的长度大于零，则判断为真。
[ -z string ]：如果字符串string的长度为零，则判断为真。
[ string1 = string2 ]：如果string1和string2相同，则判断为真。
[ string1 == string2 ] 等同于[ string1 = string2 ]。
[ string1 != string2 ]：如果string1和string2不相同，则判断为真。
[ string1 '>' string2 ]：如果按照字典顺序string1排列在string2之后，则判断为真。
[ string1 '<' string2 ]：如果按照字典顺序string1排列在string2之前，则判断为真。
```
注意，test命令内部的>和<，必须用引号引起来（或者是用反斜杠转义）。否则，它们会被 shell 解释为重定向操作符。

### 整数判断
```commandline
[ integer1 -eq integer2 ]：如果integer1等于integer2，则为true。
[ integer1 -ne integer2 ]：如果integer1不等于integer2，则为true。
[ integer1 -le integer2 ]：如果integer1小于或等于integer2，则为true。
[ integer1 -lt integer2 ]：如果integer1小于integer2，则为true。
[ integer1 -ge integer2 ]：如果integer1大于或等于integer2，则为true。
[ integer1 -gt integer2 ]：如果integer1大于integer2，则为true。
```

### 正则判断
[[ expression ]]这种判断形式，支持正则表达式。
````
[[ string1 =~ regex ]]
````

### test 判断的逻辑运算
```commandline
AND运算：符号&&，也可使用参数-a。
OR运算：符号||，也可使用参数-o。
NOT运算：符号!。
```

```
if !([ $INT -ge $MIN_VAL ] && [ $INT -le $MAX_VAL ]); then
  echo "$INT is outside $MIN_VAL to $MAX_VAL."
else
  echo "$INT is in range."
fi
```
### 算术判断
```commandline
if ((3 > 2)); then
  echo "true"
fi
```
上面代码执行后，会打印出true。

注意，算术判断不需要使用test命令，而是直接使用((...))结构。这个结构的返回值，决定了判断的真伪。

如果算术计算的结果是非零值，则表示判断成立。这一点跟命令的返回值正好相反，需要小心。

### 普通命令的逻辑运算
````
$ mkdir temp && cd temp
````
上面的命令会创建一个名为temp的目录，执行成功后，才会执行第二个命令，进入这个目录。
````
$ [ -d temp ] || mkdir temp
````
上面的命令会测试目录temp是否存在，如果不存在，就会执行第二个命令，创建这个目录。这种写法非常有助于在脚本中处理错误。
````
[ ! -d temp ] && exit 1
````
上面的命令中，如果temp子目录不存在，脚本会终止，并且返回值为1。

### case 结构
```commandline
case expression in
  pattern )
    commands ;;
  pattern )
    commands ;;
  ...
esac
```
```commandline
#!/bin/bash

echo -n "输入一个1到3之间的数字（包含两端）> "
read character
case $character in
  1 ) echo 1
    ;;
  2 ) echo 2
    ;;
  3 ) echo 3
    ;;
  * ) echo 输入不符合要求
esac
```

case的匹配模式可以使用各种通配符，下面是一些例子。
```commandline
a)：匹配a。
a|b)：匹配a或b。
[[:alpha:]])：匹配单个字母。
???)：匹配3个字符的单词。
*.txt)：匹配.txt结尾。
*)：匹配任意输入，通过作为case结构的最后一个模式。
```

## 循环
Bash 提供三种循环语法for、while和until。
### while
```commandline
#!/bin/bash

number=0
while [ "$number" -lt 10 ]; do
  echo "Number = $number"
  number=$((number + 1))
done
```

### until
until循环与while循环恰好相反，只要不符合判断条件（判断条件失败），就不断循环执行指定的语句。
一旦符合判断条件，就退出循环。
```commandline
until condition
do
  commands
done
```
until的条件部分也可以是一个命令，表示在这个命令执行成功之前，不断重复尝试。
````
until cp $1 $2; do
echo 'Attempt to copy failed. waiting...'
sleep 5
done
````
上面例子表示，只要cp $1 $2这个命令执行不成功，就5秒钟后再尝试一次，直到成功为止。
```commandline
while ! cp $1 $2; do
  echo 'Attempt to copy failed. waiting...'
  sleep 5
done
```
### for in
for...in循环用于遍历列表的每一项。
````
for variable in list
do
commands
done
````
```commandline
#!/bin/bash

for i in word1 word2 word3; do
  echo $i
done

```
```commandline
#!/bin/bash

count=0
for i in $(cat ~/.bash_profile); do
  count=$((count + 1))
  echo "Word $count ($i) contains $(echo -n $i | wc -c) characters"
done

```
上面例子中，cat ~/.bash_profile命令会输出~/.bash_profile文件的内容，然后通过遍历每一个词，计算该文件一共包含多少个词，以及每个词有多少个字符。

in list的部分可以省略，这时list默认等于脚本的所有参数$@。

### for
for循环还支持 C 语言的循环语法。
````
for (( expression1; expression2; expression3 )); do
commands
done
````
它等同于下面的while循环。
````
(( expression1 ))
while (( expression2 )); do
commands
(( expression3 ))
done
````
```commandline
for (( i=0; i<5; i=i+1 )); do
  echo $i
done
```

### select 结构
select结构主要用来生成简单的菜单。
```commandline
select name
[in list]
do
  commands
done

```
- select生成一个菜单，内容是列表list的每一项，并且每一项前面还有一个数字编号。
- Bash 提示用户选择一项，输入它的编号。
- 用户输入以后，Bash 会将该项的内容存在变量name，该项的编号存入环境变量REPLY。如果用户没有输入，就按回车键，Bash 会重新输出菜单，让用户选择。
- 执行命令体commands。
- 执行结束后，回到第一步，重复这个过程。

```commandline
#!/bin/bash
# select.sh

select brand in Samsung Sony iphone symphony Walton
do
  echo "You have chosen $brand"
done
```
```commandline
$ ./select.sh
1) Samsung
2) Sony
3) iphone
4) symphony
5) Walton
#?
```
select可以与case结合，针对不同项，执行不同的命令。

## 函数
函数总是在当前 Shell 执行.
Bash 会新建一个子 Shell 执行脚本。
```commandline
# 第一种
fn() {
  # codes
}

# 第二种
function fn() {
  # codes
}
```
```commandline
hello() {
  echo "Hello $1"
}
```
上面代码中，函数体里面的$1表示函数调用时的第一个参数。

调用时，就直接写函数名，参数跟在函数名后面。
```commandline
$ hello world
Hello world
```
删除一个函数，可以使用unset命令。
````
unset -f functionName
````
### 参数变量
```commandline
$1~$9：函数的第一个到第9个的参数。
$0：函数所在的脚本名。
$#：函数的参数总数。
$@：函数的全部参数，参数之间使用空格分隔。
$*：函数的全部参数，参数之间使用变量$IFS值的第一个字符分隔，默认为空格，但是可以自定义。
如果函数的参数多于9个，那么第10个参数可以用${10}的形式引用，以此类推。
```
```commandline
#!/bin/bash
# test.sh

function alice {
  echo "alice: $@"
  echo "$0: $1 $2 $3 $4"
  echo "$# arguments"

}

alice in wonderland
```
```commandline
$ bash test.sh
alice: in wonderland
test.sh: in wonderland # 由于函数alice只有第一个和第二个参数，所以第三个和第四个参数为空
2 arguments
```
下面是一个日志函数的例子。
````
function log_msg {
echo "[`date '+ %F %T'` ]: $@"
}
````
使用方法如下。
````
$ log_msg "This is sample log message"
[ 2018-08-16 19:56:34 ]: This is sample log message
````

### return 命令
return命令用于从函数返回一个值。函数执行到这条命令，就不再往下执行了，直接返回了。
```commandline
function func_return_value {
  return 10
}
```
### 全局变量和局部变量
Bash 函数体内直接声明的变量，属于全局变量，整个脚本都可以读取。这一点需要特别小心。

函数里面可以用local命令声明局部变量。

## 数组
### 声明数组
```commandline
$ array[0]=val
$ array[1]=val
$ array[2]=val

ARRAY=(value1 value2 ... valueN)
```
注意！没有逗号 ","

也可以在每个值前面指定位置。
```commandline
$ array=([2]=c [0]=a [1]=b)

```

定义数组的时候，可以使用通配符。
````
$ mp3s=( *.mp3 )
````
上面例子中，将当前目录的所有 MP3 文件，放进一个数组。

用declare -a命令声明一个数组，也是可以的。
````
$ declare -a ARRAYNAME
````
read -a命令则是将用户的命令行输入，存入一个数组。
````
$ read -a dice
````
上面命令将用户的命令行输入，存入数组dice。

### 读取数组
```commandline
$ echo ${array[i]}     # i 是索引
```
````
$ array[0]=a

$ echo ${array[0]}
a

$ echo $array[0]
a[0]
````
上面例子中，数组的第一个元素是a。如果不加大括号，Bash 会直接读取$array首成员的值，然后将[0]按照原样输出。

#### 读取所有成员
@和*是数组的特殊索引，表示返回数组的所有成员。
````
$ foo=(a b c d e f)
$ echo ${foo[@]}
a b c d e f
````
@和*放不放在双引号之中，是有差别的。
```commandline
$ activities=( swimming "water skiing" canoeing "white-water rafting" surfing )
$ for act in ${activities[@]}; \
do \
echo "Activity: $act"; \
done

Activity: swimming
Activity: water
Activity: skiing
Activity: canoeing
Activity: white-water
Activity: rafting
Activity: surfing  # 五个元素遍历出七个结果
```
改为
```commandline
$ for act in "${activities[@]}"; \
do \
echo "Activity: $act"; \
done

Activity: swimming
Activity: water skiing
Activity: canoeing
Activity: white-water rafting
Activity: surfing
```
${activities[*]}放在双引号之中，所有成员就会变成单个字符串返回。
```commandline
$ for act in "${activities[*]}"; \
do \
echo "Activity: $act"; \
done

Activity: swimming water skiing canoeing white-water rafting surfing
```
所以，拷贝一个数组的最方便方法，就是写成下面这样。
````
$ hobbies=( "${activities[@]}" )

$ hobbies=( "${activities[@]}" diving ) # 添加新成员
````
#### 默认位置
如果读取数组成员时，没有读取指定哪一个位置的成员，默认使用0号位置。

### 数组的长度
要想知道数组的长度（即一共包含多少成员），可以使用下面两种语法。
````
${#array[*]}
${#array[@]}
````
```commandline
Franks-Mac:reading frank$ a[100]=foo
Franks-Mac:reading frank$ echo ${#a}  # 返回数组a的第一个元素的字符串长度
4
Franks-Mac:reading frank$ echo ${#a[*]} # 返回数组a的元素个数
2
Franks-Mac:reading frank$ echo $a  # 默认位置是0
love
Franks-Mac:reading frank$ echo ${a[0]}
love
Franks-Mac:reading frank$ echo ${a[1]}

Franks-Mac:reading frank$ echo ${a[100]}
foo
Franks-Mac:reading frank$ echo ${#a[100]}
3
Franks-Mac:reading frank$ echo ${#a[@]}
2
```
虽然给数组a赋值第100个位置为foo，但是它的元素个数并不是101，而只是2

### 提取数组序号
${!array[@]}或${!array[*]}，可以返回数组的成员序号，即哪些位置是有值的。
```commandline
Franks-Mac:reading frank$ echo ${!a[@]}
0 100
Franks-Mac:reading frank$ echo ${!a[*]}
0 100

```
### 提取数组成员
${array[@]:position:length}的语法可以提取数组成员。
```commandline
$ food=( apples bananas cucumbers dates eggs fajitas grapes )
$ echo ${food[@]:1:1}
bananas
$ echo ${food[@]:1:3}
bananas cucumbers dates
Franks-Mac:reading frank$ echo ${food[*]:1:-2}
bash: -2: substring expression < 0
Franks-Mac:reading frank$ echo ${food[*]:-2:-1}
apples bananas cucumbers dates eggs fajitas grapes
Franks-Mac:reading frank$ echo ${food[*]:2}
cucumbers dates eggs fajitas grapes

```
### 追加数组成员
数组末尾追加成员，可以使用+=赋值运算符。它能够自动地把值追加到数组末尾。
否则，就需要知道数组的最大序号，比较麻烦。

### 删除数组
删除一个数组成员，使用unset命令。
```commandline
Franks-Mac:reading frank$ echo ${food[@]}
apples bananas cucumbers dates eggs fajitas grapes
Franks-Mac:reading frank$ unset ${food[2]} # 没有这种语法
Franks-Mac:reading frank$ echo ${food[@]}
apples bananas cucumbers dates eggs fajitas grapes
Franks-Mac:reading frank$ unset food[2] # 删除某一个元素
Franks-Mac:reading frank$ echo ${food[@]}
apples bananas dates eggs fajitas grapes
Franks-Mac:reading frank$ unset food  # 删除整个数组
Franks-Mac:reading frank$ echo ${food[@]}

Franks-Mac:reading frank$ echo ${#food[@]}
0

```
unset之后的索引会一直留白，后续的索引并不会依次迁移。
```commandline
Franks-Mac:reading frank$ foo=(a b c d e f)
Franks-Mac:reading frank$ unset foo[3]
Franks-Mac:reading frank$ echo ${foo[*]}
a b c e f
Franks-Mac:reading frank$ echo ${#foo[*]}
5
Franks-Mac:reading frank$ unset foo[3]  # 并不会删除 e元素
Franks-Mac:reading frank$ echo ${#foo[*]}
5
Franks-Mac:reading frank$ echo ${foo[*]}
a b c e f
Franks-Mac:reading frank$ echo ${!foo[*]}
0 1 2 4 5
```
赋值为空、空字符串虽然有隐藏效果，但是其实不为空。
```
Franks-Mac:reading frank$ foo[3]=''
Franks-Mac:reading frank$ echo ${!foo[*]}
0 1 2 3 4 5
Franks-Mac:reading frank$ echo ${#foo[*]}
6
Franks-Mac:reading frank$ unset foo[3]
Franks-Mac:reading frank$ echo ${#foo[*]}
5
Franks-Mac:reading frank$ echo ${!foo[*]}
0 1 2 4 5
Franks-Mac:reading frank$ foo[3]=
Franks-Mac:reading frank$ echo ${#foo[*]}
6
Franks-Mac:reading frank$ echo ${!foo[*]}
0 1 2 3 4 5

```
### 关联数组（Python中的字典）
Bash 的新版本支持关联数组。关联数组使用字符串而不是整数作为数组索引。

declare -A可以声明关联数组。
````
declare -A colors
colors["red"]="#ff0000"
colors["green"]="#00ff00"
colors["blue"]="#0000ff"

echo ${colors["blue"]}
````

MacOS的shell不支持。
```commandline
Franks-Mac:reading frank$ declare -A colors
bash: declare: -A: invalid option
declare: usage: declare [-afFirtx] [-p] [name[=value] ...]

```

## set
set命令用来修改子 Shell 环境的运行参数，即定制环境。一共有十几个参数可以定制
直接运行set，会显示所有的环境变量和 Shell 函数。
### set -u
set -u就用来改变忽略不存在的变量的行为。脚本在头部加上它，遇到不存在的变量就会报错，并停止执行。
### set -x
set -x用来在运行结果之前，先输出执行的那一行命令。方便查看每一条指令的运行结果。
```commandline
#!/bin/bash

number=1

set -x
if [ $number = "1" ]; then
  echo "Number equals 1"
else
  echo "Number does not equal 1"
fi
set +x  # 关闭命令输出, 只对特定的代码段打开命令输出
```

### Bash 的错误处理 与 set -e
如果脚本里面有运行失败的命令（返回值非0），Bash 默认会继续执行后面的命令。

这种行为很不利于脚本安全和除错。实际开发中，如果某个命令失败，往往需要脚本停止执行，防止错误累积。这时，一般采用下面的写法。
````
command || exit 1
````
```commandline
# 写法一
command || { echo "command failed"; exit 1; }

# 写法二
if ! command; then echo "command failed"; exit 1; fi

# 写法三
command
if [ "$?" -ne 0 ]; then echo "command failed"; exit 1; fi

```
如果两个命令有继承关系，只有第一个命令成功了，才能继续执行第二个命令，那么就要采用下面的写法。
```commandline
command1 && command2
```
上面这些写法多少有些麻烦，容易疏忽。set -e从根本上解决了这个问题，它使得脚本只要发生错误，就终止执行。

set +e表示关闭-e选项，set -e表示重新打开-e选项。

还有一种方法是使用command || true，使得该命令即使执行失败，脚本也不会终止执行。
````
#!/bin/bash
set -e

foo || true
echo bar
````

### set -n：等同于set -o noexec，不运行命令，只检查语法是否正确。
上面重点介绍的set命令的几个参数，一般都放在一起使用。
````
# 写法一
set -Eeuxo pipefail

# 写法二
set -Eeux
set -o pipefail

````

refer to
[set manual](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)

## 脚本除错
编写 Shell 脚本的时候，一定要考虑到命令失败的情况，否则很容易出错。
```commandline
#! /bin/bash

dir_name=/path/not/exist

cd $dir_name
rm *

```
上面脚本中，如果目录$dir_name不存在，cd $dir_name命令就会执行失败。
这时，就不会改变当前目录，脚本会继续执行下去，导致rm *命令删光当前目录的文件。

```commandline
cd $dir_name && rm *
```
上面脚本中，只有cd $dir_name执行成功，才会执行rm *。
但是，如果变量$dir_name为空，cd就会进入用户主目录，从而删光用户主目录的文件。

下面的写法才是正确的。
````
[[ -d $dir_name ]] && cd $dir_name && rm *
````
如果不放心删除什么文件，可以先打印出来看一下。
````
[[ -d $dir_name ]] && cd $dir_name && echo rm *
````
上面命令中，echo rm *不会删除文件，只会打印出来要删除的文件。

### bash的-x参数
bash的-x参数可以在执行每一行命令之前，打印该命令。一旦出错，这样就比较容易追查。
```commandline
$ bash -x script.sh
+ echo hello world
hello world
```
与上一节 set -x 差不多

```commandline
#! /bin/bash -x
# trouble: script to demonstrate common errors

number=1
if [ $number = 1 ]; then
  echo "Number is equal to 1."
else
  echo "Number is not equal to 1."
fi
```
```commandline
$ trouble
+ number=1
+ '[' 1 = 1 ']'
+ echo 'Number is equal to 1.'
Number is equal to 1.
```
输出的命令之前的+号，是由系统变量PS4决定，可以修改这个变量。
````
Franks-Mac:reading frank$ echo ${PS4}
+
````
````
$ export PS4='$LINENO + '
$ trouble
5 + number=1
7 + '[' 1 = 1 ']'
8 + echo 'Number is equal to 1.'
Number is equal to 1.
````

### 环境变量
变量LINENO返回它在脚本里面的行号。

### 临时文件的安全问题
直接创建临时文件，尤其在/tmp目录里面，往往会导致安全问题。
- /tmp目录是所有人可读写的
- 如果攻击者知道临时文件的文件名，他可以创建符号链接，链接到临时文件，可能导致系统运行异常
- 临时文件使用完毕，应该删除。但是，脚本意外退出时，往往会忽略清理临时文件。
```commandline
创建前检查文件是否已经存在。
确保临时文件已成功创建。
临时文件必须有权限的限制。
临时文件要使用不可预测的文件名。
脚本退出时，要删除临时文件（使用trap命令）。
```
#### mktemp
虽然在创建临时文件之前，它不会检查临时文件是否存在，但是它支持唯一文件名和清除机制，
```commandline
Franks-Mac:reading frank$ mktemp
/var/folders/6s/kcwgs1kx5jg0v3s5zmgyv8fr0000gn/T/tmp.eJhx5eD9
Franks-Mac:reading frank$ ls -lh /var/folders/6s/kcwgs1kx5jg0v3s5zmgyv8fr0000gn/T/tmp.eJhx5eD9
-rw-------  1 frank  staff     0B Mar 26 08:28 /var/folders/6s/kcwgs1kx5jg0v3s5zmgyv8fr0000gn/T/tmp.eJhx5eD9

```
获取临时文件名称，OR（||）运算符保证创建失败时退出脚本。
```
#!/bin/bash

# 为了保证脚本退出时临时文件被删除，可以使用trap命令指定退出时的清除操作。
trap 'rm -f "$TMPFILE"' EXIT

TMPFILE=$(mktemp) || exit 1
echo "Our temp file is $TMPFILE"
```
-d参数可以创建一个临时目录。

-p参数可以指定临时文件所在的目录。默认值由 TMPDIR 环境变量指定。
```commandline
Franks-Mac:reading frank$ echo $TMPDIR
/var/folders/6s/kcwgs1kx5jg0v3s5zmgyv8fr0000gn/T/

```
-t参数可以指定临时文件的文件名模板，模板的末尾必须至少包含三个连续的X字符，表示随机字符，建议至少使用六个X

```commandline
Franks-Mac:reading frank$ mktemp -t mytemp.XXX -p /tmp/ -d
mktemp: illegal option -- p
usage: mktemp [-d] [-q] [-t prefix] [-u] template ...
       mktemp [-d] [-q] [-u] -t prefix 
Franks-Mac:reading frank$ mktemp -t mytemp.XXX  -d
/var/folders/6s/kcwgs1kx5jg0v3s5zmgyv8fr0000gn/T/mytemp.XXX.o5Rl8hC6
Franks-Mac:reading frank$ ll /var/folders/6s/kcwgs1kx5jg0v3s5zmgyv8fr0000gn/T/mytemp.XXX.o5Rl8hC6
total 0
drwx------    2 frank  staff    64B Mar 26 08:37 .
drwx------@ 370 frank  staff    12K Mar 26 08:37 ..

```
#### trap
trap命令用来在 Bash 脚本中响应系统信号。

最常见的系统信号就是 SIGINT（中断），即按 Ctrl + C 所产生的信号。trap命令的-l参数，可以列出所有的系统信号。
```commandline
Franks-Mac:reading frank$ trap -l
 1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL
 5) SIGTRAP      6) SIGABRT      7) SIGEMT       8) SIGFPE
 9) SIGKILL     10) SIGBUS      11) SIGSEGV     12) SIGSYS
13) SIGPIPE     14) SIGALRM     15) SIGTERM     16) SIGURG
17) SIGSTOP     18) SIGTSTP     19) SIGCONT     20) SIGCHLD
21) SIGTTIN     22) SIGTTOU     23) SIGIO       24) SIGXCPU
25) SIGXFSZ     26) SIGVTALRM   27) SIGPROF     28) SIGWINCH
29) SIGINFO     30) SIGUSR1     31) SIGUSR2     
Franks-Mac:reading frank$ 
```
trap的命令格式如下。
````
$ trap [动作] [信号1] [信号2] ...
````
上面代码中，“动作”是一个 Bash 命令，“信号”常用的有以下几个。
````
HUP：编号1，脚本与所在的终端脱离联系。
INT：编号2，用户按下 Ctrl + C，意图让脚本终止运行。
QUIT：编号3，用户按下 Ctrl + 斜杠，意图退出脚本。
KILL：编号9，该信号用于杀死进程。
TERM：编号15，这是kill命令发出的默认信号。
EXIT：编号0，这不是系统信号，而是 Bash 脚本特有的信号，不管什么情况，只要退出脚本就会产生。
````
有点像是 Golang里面的 defer

## Session
Session 有两种类型：登录 Session 和非登录 Session，也可以叫做 login shell 和 non-login shell。

### 登录 Session
登录 Session 一般进行整个系统环境的初始化，启动的初始化脚本依次如下。
````
/etc/profile：所有用户的全局配置脚本。
/etc/profile.d目录里面所有.sh文件
~/.bash_profile：用户的个人配置脚本。如果该脚本存在，则执行完就不再往下执行。
~/.bash_login：如果~/.bash_profile没找到，则尝试执行这个脚本（C shell 的初始化脚本）。如果该脚本存在，则执行完就不再往下执行。
~/.profile：如果~/.bash_profile和~/.bash_login都没找到，则尝试读取这个脚本（Bourne shell 和 Korn shell 的初始化脚本）。
````
Linux 发行版更新的时候，会更新/etc里面的文件，比如/etc/profile，因此不要直接修改这个文件。
如果想修改所有用户的登陆环境，就在/etc/profile.d目录里面新建.sh脚本。

如果想修改你个人的登录环境，一般是写在~/.bash_profile里面。
```commandline
Franks-Mac:reading frank$ ls -al ~
-rw-------    1 frank  staff   100K Mar 21 16:55 .bash_history
-rw-r--r--    1 frank  staff   3.0K Mar 22 11:04 .bash_profile
drwx------   12 frank  staff   384B Mar 11 11:59 .bash_sessions
Franks-Mac:reading frank$ ls -al ~/.bash_sessions/
1F865DFC-E573-4D05-AD51-9DF4B979C915.history
1F865DFC-E573-4D05-AD51-9DF4B979C915.historynew
1F865DFC-E573-4D05-AD51-9DF4B979C915.session
433DDABC-4D45-48B2-A748-AE974D7E8EFC.history
433DDABC-4D45-48B2-A748-AE974D7E8EFC.historynew
AD1812A9-A4B7-4016-9F05-58FF7010ACCE.history
AD1812A9-A4B7-4016-9F05-58FF7010ACCE.historynew
AD1812A9-A4B7-4016-9F05-58FF7010ACCE.session
BF4E38FB-0623-47F1-B547-F80EE6B62A85.historynew
_expiration_check_timestamp
```
```commandline
# .bash_profile
PATH=/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/bin
PATH=$PATH:$HOME/bin

SHELL=/bin/bash
MANPATH=/usr/man:/usr/X11/man
EDITOR=/usr/bin/vi
PS1='\h:\w\$ '
PS2='> '

if [ -f ~/.bashrc ]; then # 判断如果文件存在
. ~/.bashrc  # = source ~/.bashrc
fi

export PATH
export EDITOR
```
### 非登录 Session
非登录 Session 是用户进入系统以后，手动新建的 Session，这时不会进行环境初始化。
比如，在命令行执行bash命令，就会新建一个非登录 Session。

非登录 Session 的初始化脚本依次如下。
````
/etc/bash.bashrc：对全体用户有效。
~/.bashrc：仅对当前用户有效。
````
~/.bashrc通常是最重要的脚本。非登录 Session 默认会执行它，而登录 Session 一般也会通过调用执行它。

`bash --norc` 可以禁止在非登录 Session 执行~/.bashrc脚本。

`bash --rcfile testrc` 指定另一个脚本代替.bashrc

### bash_logout
~/.bash_logout脚本在每次退出 Session 时执行，通常用来做一些清理工作和记录工作，比如删除临时文件，记录用户在本次 Session 花费的时间。

如果没有退出时要执行的命令，这个文件也可以不存在。

### 启动选项
```commandline
$ bash -n scriptname  # 不运行脚本，只检查是否有语法错误。
$ bash -v scriptname  # 输出每一行语句运行结果前，会先输出该行语句。
$ bash -x scriptname  # 每一个命令处理之前，先输出该命令，再执行该命令。
```

## 命令提示符

### 环境变量 PS1
命令提示符通常是美元符号$，对于根用户则是井号#。这个符号是环境变量PS1决定的，
```commandline
Franks-Mac:reading frank$ echo $PS1
\h:\W \u\$
# 本机的主机名：当前目录名 当前用户名
Franks-Mac:reading frank$ sudo su
Password:
sh-3.2# 
sh-3.2# echo $PS1
\s-
   \$
# Shell 的名称
```
```commandline
\a：响铃，计算机发出一记声音。
\d：以星期、月、日格式表示当前日期，例如“Mon May 26”。
\h：本机的主机名。
\H：完整的主机名。
\j：运行在当前 Shell 会话的工作数。
\l：当前终端设备名。
\n：一个换行符。
\r：一个回车符。
\s：Shell 的名称。
\t：24小时制的hours:minutes:seconds格式表示当前时间。
\T：12小时制的当前时间。
\@：12小时制的AM/PM格式表示当前时间。
\A：24小时制的hours:minutes表示当前时间。
\u：当前用户名。
\v：Shell 的版本号。
\V：Shell 的版本号和发布号。
\w：当前的工作路径。
\W：当前目录名。
\!：当前命令在命令历史中的编号。
\#：当前 shell 会话中的命令数。
\$：普通用户显示为$字符，根用户显示为#字符。
\[：非打印字符序列的开始标志。
\]：非打印字符序列的结束标志。
```
### 颜色
命令提示符是显示终端预定义的颜色

设定其后文本的颜色。
```commandline
\033[0;30m：黑色
\033[1;30m：深灰色
\033[0;31m：红色
\033[1;31m：浅红色
\033[0;32m：绿色
\033[1;32m：浅绿色
\033[0;33m：棕色
\033[1;33m：黄色
\033[0;34m：蓝色
\033[1;34m：浅蓝色
\033[0;35m：粉红
\033[1;35m：浅粉色
\033[0;36m：青色
\033[1;36m：浅青色
\033[0;37m：浅灰色
\033[1;37m：白色

```

```commandline
PS1='\[\033[0;31m\]<\u@\h \W>\$\[\033[00m\]'
```
以上设置提示符设为红色，但是`\[\033[00m\]` 避免用户在提示符后面输入的文本也是红色的，恢复默认色。

Bash 还允许设置背景颜色。
````
\033[0;40m：蓝色
\033[1;44m：黑色
\033[0;41m：红色
\033[1;45m：粉红
\033[0;42m：绿色
\033[1;46m：青色
\033[0;43m：棕色
\033[1;47m：浅灰色
````

### 环境变量 PS2，PS3，PS4
环境变量PS2是命令行折行输入时系统的提示符，默认为>。
```commandline
sh-3.2# echo $PS2
>
Franks-Mac:reading frank$ echo $PS2
>

```
环境变量PS3是使用select命令时，系统输入菜单的提示符。
环境变量PS4默认为+。它是使用 Bash 的-x参数执行脚本时，每一行命令在执行前都会先打印出来，并且在行首出现的那个提示符。
```commandline
Franks-Mac:reading frank$ echo $PS3

Franks-Mac:reading frank$ echo $PS4
+

```

## Reference
- [Bash 脚本教程](https://wangdoc.com/bash/)
- [bash-tutorial](https://github.com/wangdoc/bash-tutorial)
- [set manual](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)
