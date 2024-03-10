# A Philosophy of Software Design
《A Philosophy of Software Design》是斯坦福大学 John Ousterhout 教授写的一本关于如何减少软件复杂度的书。
软件复杂度在软件的迭代中会不可避免的增加，复杂度增加对于程序代码的阅读者来说会增加学习成本，增加后继开发者的出bug的几率。
简单的软件设计可以让复杂度增加的慢一些，所以在软件开发的生命全周期里面软件设计需要一直应用。而软件设计的技能并不是天生的，
是可以习得的。
## The Nature of Complexity
开发人员拥有鉴别复杂度的能力很重要。那么什么是软件复杂度？
软件复杂度是指任何让软件系统难以阅读，难以理解和难以修改的结构。
写软件的人通常无法准确意识到自己的程序的复杂度，但是其他阅读的人更能明白，以阅读者的评判为准。

### Symptoms of Complexity
- 放大需要更改的地方 Change Amplification：The first symptom of complexity is that
  a seemingly simple change requires code modifications in many different places. 
  例如css中给多个div定义同样的行内样式，那会导致修改样式时候需要修改多个地方。然而把样式定义为一个变量，
  在需要的div里面引用，那么修改的时候只需要修改定义处。
- 开发人员的认知的负荷 Cognitive Load： The second symptom of complexity is cognitive load, 
  which refers to how much a developer needs to know in order to complete a task.
  有些人可能以为代码的行数代表认知的负荷，但是有时候更多行的代码会更简单，更容易理解。
- Unknown unknowns: The third symptom of complexity is that it is not obvious 
  which pieces of code must be modified to complete a task, or what information 
  a developer must have to carry out the task successfully. 
  通常由代码风格不一致，有些设计没有记录文档导致的。后继开发者不知道修改哪里，
  或者修改了feature直到上线了才能暴露的bug。所以好设计应该追求简单明显，容易理解。
  
### Cause of Complexity
- 依赖 dependencies。修改一个方法的参数，会导致需要修改所有调用方法的地方。
  依赖是软件的基础特性，是无法消除的。只能尽量减少依赖，并且使依赖尽可能的简单明显，容易理解。
- 晦涩 obscurity。当重要的信息不明显的时候，就会产生晦涩难懂。例如不充分的文档记录，依赖关系不明显。
  不过的好的设计可以减少文档量，如果一个设计所需要的文档记录比较多的话，那就是一个危险信号。
  
dependencies -> change amplification and cognitive load
obscurity -> unknown unknowns and cognitive load

### Complexity is incremental
复杂度是递增的，累积的。每次引入一点点的复杂度，开发者往往不以为意，但是需要 "零容忍"的态度来对待引入复杂度。

## Working code isn't enough -- Strategic vs. Tactical Programming
战略路径 strategic approach -> better design -> slower -> require an investment mindset 
-> proactive investment on good documentation -> the real hero -> 
take a few to fix it when discovering design problem

战术路径 tactical approach -> 尽快交付（新功能或者bug）-> complexities accumulation  -> need refactor

### How much to invest?
大的一次性的全局的design并不是有效率的 -> 随着开发系统的进行，理想的设计会一点一点的浮现出来 -> 
10%-20% 的时间投资在思考更好的设计上 -> 投资会在未来收到回报

### Startups and investment
初创公司更加偏向于短期的战术编程，以后再重构。但是如果代码最终变得像意大利面条spaghetti一样错综复杂，重构是很难的

软件工程师的质量也是很重要的，少量的优秀的会设计的工程师会比大量的平庸的工程师更加有生产力，
清晰的系统设计后期也更加可以吸引优秀的工程师加入团队。

- Facebook: encourage tactical programming at beginning but switch to strategic later
- Google/VMware: encourage strategic programming

## Modules should be deep
### What is modules design
One of the most important techniques for managing software complexity is to
design systems so that developers only need to face a small fraction of the 
overall complexity at any given time. 各个模块相对独立，可以多人同步进行开发。

### Modular Design
In modular design, a software system is decomposed into a collection of modules 
that are relatively independent. Modules can take many forms, 
such as classes, subsystems, or services.
但是module可能互相调用，需要直到彼此的一些信息，所以不存在绝对的module独立性，总该有点依赖。

- Each class in an object-oriented programming language is a module.
- Methods within a class, or functions in a language that isn’t object-oriented, 
  can also be thought of as modules
  
管理依赖的入手点
- interface: Typically, the interface describes what the module does but not how it does it
- implementation: The implementation consists of the code that carries out the 
  promises made by the interface.

The best modules are those whose interfaces are much simpler than their implementations.
- 简单接口最小化该模块对于系统中其他模块的影响的复杂度。
- 如果一个模块的修改而能不改变它的接口定义，那么它的修改不会影响其他模块。

### What is an interface
- formal information: its signature(includes the names and types of its parameters, 
  the type of its return value, and information about exceptions thrown by the method)
- informal information: If there are constraints on the usage of a class 
  (perhaps one method must be called before another) 通常在文档中记录

### Abstractions
抽象 An abstraction is a simplified view of an entity, which omits unimportant details.

The key to designing abstractions is to understand what is important, 
and to look for designs that minimize the amount of information that is important.

### Deep modules
he best modules are those that provide powerful functionality yet have simple interfaces. 
I use the term deep to describe such modules

- 深模块设计 deep modules: they allow a lot of functionality to be accessed through a simple interface
- 浅模块设计 shallow module is one with a relatively complex interface, but not much functionality: 
  it doesn’t hide much complexity.

Unfortunately, the value of deep classes is not widely appreciated today. 
The conventional wisdom in programming is that classes should be small, not deep.

吐槽下java IO的设计，没有把 Buffer 当作默认设置，而是每次都要声明使用，导致程序员容易忘记。
没有 buffer 的IO会很慢的，应该没有这样的使用场景。
```java
FileInputStream fileStream =
        new FileInputStream(fileName);
BufferedInputStream bufferedStream =
        new BufferedInputStream(fileStream);
ObjectInputStream objectStream =
        new ObjectInputStream(bufferedStream);
```

## How to make modules deep
- Information Hiding
- Design General Purpose Modules
- Different Layers, Different Abstraction
- Pull Complexity Downwards


### Information Hiding(and leakage)
#### Information Hiding
The knowledge(例如数据接口和算法) is embedded in the module's implementation 
but doesn't appear in its interface.

Benefits of information hiding
- 简化模块接口复杂度
- 系统演进更容易

Hiding variables and methods in a class by declaring them private 
isn’t the same thing as information hiding

#### Information Leakage
相反，涉及到多个模块关联的设计决定就是信息泄漏，会产生依赖关系，涉及到设计的修改会牵扯到多个模块的修改。

例如两个模块都要操作同一个文件，一个读，一个写。即是接口中没有明示依赖关系，这种依赖难以察觉。

遇到了多个模块共享信息该怎么处理？
- If the affected classes are relatively small and closely tied to the leaked information, 
  it may make sense to merge them into a single class
- Another possible approach is to pull the information out of all of the affected classes 
  and create a new class that encapsulates just that information

##### The common reason of information leakage
One common cause of information leakage is a design style called temporal decomposition,
一种以操作的时间先后顺序进行设计的结构。例如对一个文件的操作的设计分为三个步骤，也想当然的分为三个类：读文件，写文件，存文件。

When designing modules, focus on the knowledge that’s needed to perform each task, 
not the order in which tasks occur.

##### Overexposure
If the API for a commonly used feature forces users to learn about other features that are rarely used, 
this increases the cognitive load on users who don’t need the rarely used features.

such as buffer in java IO

### Make classes somewhat general-purpose
The phrase “somewhat general-purpose” means that the module’s functionality should reflect your current needs, 
but its interface should not. Instead, the interface should be general enough to support multiple uses.

Example: Building a GUI text editor
- special-purpose design
```
void backspace(Cursor cursor);
void delete(Cursor cursor);
void deleteSelection(Selection selection);
```
- general-purpose design
```
void insert(Position position, String newText);
void delete(Position start, Position end);
Position changePosition(Position position, int numChars);
text.delete(cursor, text.changePosition(cursor, 1)); // delete
text.delete(text.changePosition(cursor, -1), cursor); //backspace
```
a bit longer and more obvious, but has less code overall than the specialized approach

#### Generality leads to better information hiding
- The general-purpose approach provides a cleaner separation between the text and user interface classes
- The general-purpose interface also reduces cognitive load: a developer working on the user interface 
  only needs to learn a few simple methods, which can be reused for a variety of purposes.
  
#### How to design general-purpose module
- If you reduce the number of methods in an API without reducing its overall capabilities, 
  then you are probably creating more general-purpose methods.
- if you have to introduce lots of additional arguments in order to reduce the number of methods, 
  then you may not really be simplifying things.  
- If a method is designed for one particular use, such as the backspace method, that is a red flag 
  that it may be too special-purpose
- If you have to write a lot of additional code to use a class for your current purpose, that’s a red flag 
  that the interface doesn’t provide the right functionality. 
  例如上面GUI editor 基于单个字符操作的设计 single-character operation， 虽然底层设计很通用和简单，
  但是上层调用的时候需要写许多的额外循环代码
  
### Different layer, different abstraction
- In a well-designed system, each layer provides a different abstraction from the layers above and below it
- If a system contains adjacent layers with similar abstractions, this is a red flag 
  that suggests a problem with the class decomposition.
  
#### Pass-through methods:
A pass-through method is one that does nothing except pass its arguments to another method, 
usually with the same API as the pass-through method. This typically indicates that 
there is not a clean division of responsibility between the classes.

#### Having methods with the same signature is not always bad
One example where it’s useful for a method to call another method with the same signature is a dispatcher.
the dispatcher provides useful functionality: it chooses which of several other methods should carry out each task.

Examples:
- Web browser ->HTTP request -> server -> dispatcher ->response(file/js)
- Interface with multiple implementations

#### Decorators 装饰器
The decorator design pattern (also known as a “wrapper”) is one that encourages API duplication across layers.
A decorator object takes an existing object and extends its functionality

Examples:
- BufferedInputStream in Java IO

The motivation for decorators is to separate special-purpose extensions of a class from a more generic core.

Before creating a decorator class, consider alternatives such as the following:
- Could you add the new functionality directly to the underlying class, rather than creating a decorator class? 
- If the new functionality is specialized for a particular use case, would it make sense to merge it with the use case, 
  rather than creating a separate class?
- Could you merge the new functionality with an existing decorator, rather than creating a new decorator?
- Finally, ask yourself whether the new functionality really needs to wrap the
  existing functionality: could you implement it as a stand-alone class that is independent of the base class?

#### Interface versus implementation
The interface of a class should normally be different from its implementation

#### Pass-through variables
Pass-through variables add complexity because they force all of the intermediate methods to be aware of their existence, 
even though the methods have no use for the variables.

Eliminating pass-through variables can be challenging.
- One approach is to see if there is already an object shared between the topmost and bottommost methods
- Another approach is to store the information in a global variable 全局变量.
  global variables make it impossible to create two independent instances of the same system in the same process, 
  since accesses to the global variables will conflict.
- Context. A context stores all of the application’s global state 
  (anything that would otherwise be a pass-through variable or global variable)
  The context allows multiple instances of the system to coexist in a single process, each with its own context.
  If a new variable needs to be added, it can be added to the context object; 
  no existing code is affected except for the constructor and destructor for the context.

Contexts are far from an ideal solution:
- it may not be obvious why a particular variable is present, or where it is used.
- Contexts may also create thread-safety issues

### Pull Complexity Downwards 将复杂度拉向底层代码
It is more important for a module to have a simple interface than a simple implementation.
Most modules have more users than developers, so it is better for the developers to suffer than the users.

开发人员很乐于把复杂度推给用户，但是对于降低软件复杂度不可取：
- 向上抛异常
- 打包成配置参数，让用户抉择怎么设置。
  - 用户或者管理员有时候也不知道该怎么正确配置。
  - 有些配置应该是动态的，而不是死的，例如重试时间间隔，重试次数。
    
## Better Together or Better Apart?
When deciding whether to combine or separate, 
the goal is to reduce the complexity of the system as a whole and improve its modularity.

The disadvantages of apart:
- Some complexity comes just from the number of components: the more components, 
  the harder to keep track of them all and the harder to find a desired component within the large collection
- Subdivision can result in additional code to manage the components.
- Subdivision creates separation: the subdivided components will be farther apart than they were before subdivision.
  If the components are truly independent, then separation is good
- Subdivision can result in duplication 

Indications that two pieces of code are related(better together):
- They share information;
- They are used together
- They overlap conceptually (such as: substring and case conversion)
- It is hard to understand one of the pieces of code without looking at the other.

### Separate general-purpose and special-purpose code
In general, the lower layers of a system tend to be more general-purpose and the upper layers more special-purpose.

### Example: editor undo mechanism
Some of the student projects implemented the entire undo mechanism as part of the text class. 
The text class maintained a list of all the undoable changes. 

These problems can be solved by extracting the general-purpose core of the undo/redo mechanism 
and placing it in a separate class
```
public class History {
    public interface Action {
        public void redo();
        public void undo();
    }
    History() {...}
    void addAction(Action action) {...}
    void addFence() {...}
    void undo() {...}
    void redo() {...}
}
```
The History class knows nothing about the information stored in the actions or 
how they implement their undo and redo methods.

History.Actions are special-purpose objects

There are a number of ways to group actions; the History class uses fences

### Splitting and joining methods
You shouldn’t break up a method unless it makes the overall system simpler
Methods containing hundreds of lines of code are fine if they have a simple signature and are easy to read.
Each method should do one thing and do it completely.

Conjoined Methods: If you can’t understand the implementation of one method without also understanding 
the implementation of another, that’s a red flag.

## Define Errors Out Of Existence
Exception handling is one of the worst sources of complexity in software systems.
The key overall lesson from this chapter is to reduce the number of places where exceptions must be handled;
in many cases the semantics of operations can be modified so that the normal behavior handles all situations 
and there is no exceptional condition to report. 改变方法或者接口的功能描述，就可以把异常纳入正常的代码中。

### Why exceptions add complexity
How to deal with the exceptions
- The first approach is to move forward and complete the work in progress in spite of the exception. 
  (network packet is lost)
- The second approach is to abort the operation in progress and report the exception upwards.(memory run out)

The exception handling code must restore consistency, such as by unwinding any changes made 
before the exception occurred.
Exception handling code creates opportunities for more exceptions.
To prevent an unending cascade of exceptions, the developer must eventually find a way to handle exceptions 
without introducing more exceptions.

处理异常的代码自己有错误那是最致命的：When exception handling code fails, it’s difficult to debug the problem, 
since it occurs so infrequently.

### Too many exceptions
Tcl contains an unset command that can be used to remove a variable. I defined unset so that 
it throws an error if the variable doesn’t exist.
However, one of the most common uses of unset is to clean up temporary state created by some previous operation.

classes with lots of exceptions have complex interfaces, and they are shallower than classes with fewer exceptions.

The best way to reduce the complexity damage caused by exception handling is to reduce the number of places 
where exceptions have to be handled.

### Define errors out of existence 通过语义定义让错误异常消失
I should have changed the definition of unset slightly: rather than deleting a variable, 
unset should ensure that a variable no longer exists. There is no longer an error case to report.

#### Example: file deletion in Windows
The Windows operating system does not permit a file to be deleted if it is open in a process

In Unix, if a file is open when it is deleted, Unix does not delete the file immediately. 
Instead, it marks the file for deletion, then the delete operation returns successfully. 
The file name has been removed from its directory, so no other processes can open the old file 
and a new file with the same name can be created, but the existing file data persists. 
Processes that already have the file open can continue to read it and write it normally. 
Once the file has been closed by all of the accessing processes, its data is freed.

#### Example: Java substring method
if either index is outside the range of the string, then substring throws IndexOutOfBoundsException.

The Java substring method would be easier to use if it performed this adjustment automatically, 
so that it implemented the following API: “returns the characters of the string 
(if any) with index greater than or equal to beginIndex and less than endIndex.”

### Mask exceptions 底层代码处理掉异常以掩盖异常
The second technique for reducing the number of places where exceptions must be handled is exception masking. 
With this approach, an exceptional condition is detected and handled at a low level in the system, 
so that higher levels of software need not be aware of the condition.

TCP masks packet loss by resending lost packets within its implementation, 
so all data eventually gets through and clients are unaware of the dropped packets.

### Exception aggregation 让异常上抛，把异常处理集中到一处进行处理（与掩盖异常相反的方法，适用于不同场景）
The third technique for reducing complexity related to exceptions is exception aggregation. 
The idea behind exception aggregation is to handle many exceptions with a single piece of code;

Instead of catching the exceptions in the individual service methods, 
let them propagate up to the top- level dispatch method for the Web server,

This is the opposite of exception masking: masking usually works best if an exception is handled in a low-level method.
For masking, the low-level method is typically a library method used by many other methods, 
so allowing the exception to propagate would increase the number of places where it is handled.

缺点：
One disadvantage of promoting a corrupted object into a server crash is that 
it increases the cost of recovery considerably. 
Error promotion may not make sense for errors that happen frequently. 

如何衡量什么时候用 exception aggregation：
One way of thinking about exception aggregation is that it replaces several special-purpose mechanisms, 
each tailored for a particular situation, with a single general-purpose mechanism that can handle multiple situations.

### Just crash
The fourth technique for reducing complexity related to exception handling is to crash the application.
these errors are difficult or impossible to handle and don’t occur very often.
The simplest thing to do in response to these errors is to print diagnostic information and then abort the application.

Example: 
- out of memory
- I/O error
    -  reading or writing an open file (such as a disk hard error)
    - a network socket cannot be opened

Whether or not it is acceptable to crash on a particular error depends on the application. 
For a replicated storage system, it isn’t appropriate to abort on an I/O error. 
Instead, the system must use replicated data to recover any information that was lost.

### Design special cases out of existence 减少特殊用例，减少if语句
Special cases can result in code that is riddled with if statements, 
which make the code hard to understand and lead to bugs. 
Thus, special cases should be eliminated wherever possible. 

The best way to do this is by designing the normal case in a way that automatically handles the special cases 
without any extra code.

Example:
- introduce a state variable indicate "no selection" -> "empty selection"

## Design it Twice
Designing software is hard, so it’s unlikely that your first thoughts about 
how to structure a module or system will produce the best design.

Example:
GUI text editor line-oriented -> character-oriented -> string-oriented -> range-oriented

Try to pick approaches that are radically different from each other; you’ll learn more that way.
Even if you are certain that there is only one reasonable approach, consider a second design anyway, 
no matter how bad you think it will be.

make a list of the pros and cons of each one. 
- The most important consideration for an interface is ease of use for higher level software.
- Does one alternative have a simpler interface than another?
- Is one interface more general-purpose than another?
- Does one interface enable a more efficient implementation than another? 

make a decision
- The best choice may be one of the alternatives
- combine features of multiple alternatives into a new design that is better than any of the original choices.
- Use the problems you identified with the original alternatives to drive the new design(s)

## Write Comments
- Comments are essential to help developers understand a system and work efficiently
- Documentation also plays an important role in abstraction; without comments, you can’t hide complexity.
- the process of writing comments, if done correctly, will actually improve a system’s design.

### Good code is self-documenting
However, there is still a significant amount of design information that can’t be represented in code.
The informal aspects of an interface, such as a high-level description of what each method does 
or the meaning of its result, can only be described in comments.
If users must read the code of a method in order to use it, then there is no abstraction

### Benefits of well-written comments
The overall idea behind comments is to capture information that was in the mind of the designer 
but couldn’t be represented in the code.

there is a risk of bugs if the new developer misunderstands the original designer’s intentions
if it has been more than a few weeks since you last worked in a piece of code, 
you will have forgotten many of the details of the original design.

## Comments Should Describe Things that Aren’t Obvious from the Code 注释
Developers should be able to understand the abstraction provided by a module without reading any code 
other than its externally visible declarations. (obvious)
- reading code is time-consuming
- and consider a lot of information that isn’t needed to use

### Pick conventions
Javadoc for Java, Doxygen for C++, or godoc for Go

consistency

### Don’t repeat the code
If the information in a comment is already obvious from the code next to the comment, then the comment isn’t helpful.

A first step towards writing good comments is to use different words in the comment 
from those in the name of the entity being described. 
```
/*
 * The amount of blank space to leave on the left and
 * right sides of each line of text, in pixels.
 */
private static final int textHorizontalPadding = 4;
```

### Lower-level comments add precision
Some comments provide information at a lower, more detailed, level than the code; 
these comments add precision by clarifying the exact meaning of the code.

Other comments provide information at a higher, more abstract, level than the code; these comments offer intuition, 
such as the reasoning behind the code, or a simpler and more abstract way of thinking about the code. 

Precise comments can fill in missing details such as:
- What are the units for this variable?
- Are the boundary conditions inclusive or exclusive?
- If a null value is permitted, what does it imply?
- If a variable refers to a resource that must eventually be freed or closed, 
  who is responsible for freeing or closing it?
- Are there certain properties that are always true for the variable (invariants), 
  such as “this list always contains at least one entry”?

When documenting a variable, think nouns, not verbs. 
In other words, focus on what the variable represents, not how it is manipulated.

### Higher-level comments enhance intuition
They omit details and help the reader to understand the overall intent and structure of the code.

Higher-level comments are more difficult to write than lower-level comments

being able to ignore the low-level details and think about the system only in terms of 
its most fundamental characteristics.

### Interface documentation
The first step in documenting abstractions is to separate interface comments from implementation comments.

Interface comments provide information that someone needs to know in order to use a class or method; 
they define the abstraction.

Implementation comments describe how a class or method works internally in order to implement the abstraction.

The interface comment:
- describe the behavior of the method as perceived by callers; this is the higher-level abstraction.
- describe each argument and the return value (lower-level)
- describe any constraints on argument values as well as dependencies between arguments.(lower-level)
- side effects, writing to the file system is also a side effect.
- describe any exceptions that can emanate from the method.
- any preconditions that must be satisfied before a method is invoked

### Implementation comments: what and why, not how
The main goal of implementation comments is to help readers understand what the code is doing (not how it does it).

In addition to describing what the code is doing, implementation comments are also useful to explain why.

- If there are tricky aspects to the code that won’t be obvious from reading it, you should document them
- For bug fixes where there is a well-written bug report describing the problem, 
  the comment can refer to the issue in the bug tracking database rather than repeating all its details
- if the variable is used over a large span of code, then you should consider adding a comment to describe the variable.

### Documents for Cross-module design decisions
- Sometimes there is an obvious central place to put such documentation
- cross-module issues are documented in a central file called designNotes, 
  if there is not an obvious central place to put cross-module documentation
  Then, in any piece of code that relates to one of these issues there is a short comment 
  referring to the designNotes file:
  ```// See "Zombies" in designNotes.```

## Write The Comments First
(Use Comments As Part Of The Design Process)
The best time to write comments is at the beginning of the process, as you write the code. 
Writing the comments first makes documentation part of the design process. 
Not only does this produce better documentation, but it also produces better designs 
and it makes the process of writing documentation more enjoyable.

- For a new class, I start by writing the class interface comment.
- Next, I write interface comments and signatures for the most important public methods, 
  but I leave the method bodies empty.
- I iterate a bit over these comments until the basic structure feels about right. 
  At this point I write declarations and comments for the most important class instance variables in the class.
- Finally, I fill in the bodies of the methods, adding implementation comments as needed.
- While writing method bodies, I usually discover the need for additional methods and instance variables. 
  For each new method I write the interface comment before the body of the method; 
  for instance variables I fill in the comment at the same time that I write the variable declaration.

Benefits of writing the comments at the beginning:
- It produces better comments. 
  you can focus on the method’s abstraction and interface without being distracted by its implementation
- It improves the system design.
  If a method or variable requires a long comment, it is a red flag that you don’t have a good abstraction.
- it makes comment- writing more fun.  


## Choosing Names 变量命名
### Example: bad names cause bugs
The file system code used the variable name `block` for two different purposes. 
In some situations, block referred to a `physical block number on disk`; 
in other situations, block referred to a `logical block number within a file`

Unfortunately, at one point in the code there was a block variable containing a logical block number, 
but it was accidentally used in a context where a physical block number was needed; as a result, 
an unrelated block on disk got overwritten with zeroes.

block -> fileBlock and diskBlock

Take a bit of extra time to choose great names, which are precise, unambiguous, and intuitive.

### Create an image
names become unwieldy if they contain more than two or three words. 
Thus, the challenge is to find just a few words that capture the most important aspects of the entity.

### Names should be precise
Good names have two properties: precision and consistency. 

- getCount -> getActiveIndexlets/numIndexlets
- x, y -> charIndex and lineIndex
- blinkStatus -> cursorVisible
- VOTED_FOR_SENTINEL_VALUE -> NOT_YET_VOTED
- result
- selection -> range

Vague Name: If a variable or method name is broad enough to refer to many different things, 
then it doesn’t convey much information to the developer and the underlying entity is more likely to be misused.

it’s fine to use generic names like i and j as loop iteration
variables, as long as the loops only span a few lines of code.

### Use names consistently
Consistent naming reduces cognitive load 

## Modifying Existing Code 更改已有代码的建议
the design of a mature system is determined more by changes made during the system’s evolution 
than by any initial conception.

### Stay strategic
If you want to have a system that is easy to maintain and enhance, then “working” isn’t a high enough standard; 
you have to prioritize design and think strategically.

Unfortunately, when developers go into existing code to make changes such as bug fixes or new features, 
they don’t usually think strategically. 
A typical mindset is “what is the smallest possible change I can make that does what I need?”

must resist the temptation to make a quick fix

If you’re not making the design better, you are probably making it worse.

什么时候选择不选择重构并提升设计？
- you may have to take the quick and dirty approach, particularly if you are working against a tight deadline.
- if refactoring the system would create incompatibilities that affect many other people and teams, 
  then the refactoring may not be practical.

### Maintaining comments: keep the comments near the code
It’s easy to forget to update comments when you modify code, which results in comments that are no longer accurate.

The best way to ensure that comments get updated is to position them close to the code they describe, 
so developers will see them when they change the code. 

Example: 
- C/C++别放头文件中，放在方便看到的地方 if place the interface comments next to the method’s declaration in the .h file. However, 
  this is a long way from the code; developers won’t see those comments when modifying the method’s body, 
  and it takes additional work to open a different file and find the interface comments to update them.
- 分步注释 if a method has three major phases, don’t write one comment at the top of the method 
  that describes all of the phases in detail. Instead, write a separate comment for each phase 
  and position that comment just above the first line of code in that phase.
- 方法的头上放全局的描述，越抽象总结越好，省得方法更改之后需要同步修改注释 
  have a comment at the top of a method’s implementation that describes the overall strategy 

### Comments belong in the code, not the commit log

### Maintaining comments: avoid duplication
If documentation is duplicated, it is more difficult for developers to find and update all of the relevant copies.
Instead, find the most obvious single place to put the documentation.
In addition, add short comments in the other places that refer to the central location: 
“See the comment in xyz for an explanation of the code below.”

If information is already documented someplace outside your program, don’t repeat the documentation inside the program; 
just reference the external documentation.

### Maintaining comments: check the diffs before commit

## Consistency
once you have learned how something is done in one place, 
you can use that knowledge to immediately understand other places that use the same approach.
Consistency allows developers to work more quickly with fewer mistakes.

### Examples of consistency
Consistency can be applied at many levels in a system:
- Names
- Coding style.
  - indentation,
  - curly-brace placement,
  - order of declarations, 
  - naming, 
  - commenting, 
  - restrictions on language features considered dangerous
- Interfaces: multiple implementations
- Design patterns: model-view-controller
- Invariants: each line is terminated by a newline character. 

### Ensuring consistency
- Document. Create a document that lists the most important overall conventions, such as coding style guidelines.
- Enforce. write a tool that checks for violations, 
  and make sure that code cannot be committed to the repository unless it passes the checker.
  - writing a short script that was executed automatically before changes are committed to the source code repository.
  - Code reviews 
- When in Rome, do as the Romans do.
  - public variables and methods declared before private ones?
  - alphabetical order?
  - camel case versus snake case?
- Don’t change existing conventions.    

## Code Should be Obvious
the best way to determine the obviousness of code is through code reviews.

### Things that make code more obvious
- choosing good names
- consistency
- Judicious use of white space.
  Blank lines are also useful to separate major blocks of code within a method
- Comments  

### Things that make code less obvious
- Event-driven programming. 事件驱动的编程，代码段执行是动态dispatch的
  Event-driven programming makes it hard to follow the flow of control. 
  The event handler functions are never invoked directly; they are invoked indirectly by the event module, 
  typically using a function pointer or interface.
  To compensate for this obscurity, use the interface comment for each handler function to indicate when it is invoked
- Generic containers. 通用的容器，如接口，基类
  Many languages provide generic classes for grouping two or more items into a single object, 
  such as Pair in Java or std::pair in C++.
- Different types for declaration and allocation.  变量声明和赋初始值类型不一致
  ```
    private List<Message> incomingMessageList;
    ...
    incomingMessageList = new ArrayList<Message>();
  ```
- Code that violates reader expectations. 代码逻辑符合读者预期，例如main函数返回应该退出程序。

## Software Trends
### Object-oriented programming and inheritance
### Agile development
One of the risks of agile development is that it can lead to tactical programming.
Developing incrementally is generally a good idea, but the increments of development should be abstractions, not features.

### Unit tests
- Unit tests are the ones most often written by developers. 
  They are small and focused: each test usually validates a small section of code in a single method. 
  Unit tests can be run in isolation, without setting up a production environment for the system
- System tests (sometimes called integration tests), 
  which ensure that the different parts of an application all work together properly. 
  They typically involve running the entire application in a production environment. 
  System tests are more likely to be written by a separate QA or testing team.

### Test-driven development
When creating a new class, the developer first writes unit tests for the class, based on its expected behavior.
Then the developer works through the tests one at a time, writing enough code for that test to pass. 
When all of the tests pass, the class is finished.

The problem with test-driven development is that it focuses attention on getting specific features working, 
rather than finding the best design.

One place where it makes sense to write the tests first is when fixing bugs. 
Before fixing a bug, write a unit test that fails because of the bug.
Then fix the bug and make sure that the unit test now passes.

### Design patterns
If a design pattern works well in a particular situation, 
it will probably be hard for you to come up with a different approach that is better.

The greatest risk with design patterns is over-application.

### Getters and setters
Getters and setters are shallow methods

## Designing for Performance
The most important idea is still simplicity: not only does simplicity improve a system’s design, 
but it usually makes systems faster.

### How to think about performance
The best approach is something between these extremes, 
where you use basic knowledge of performance to choose design alternatives 
that are “naturally efficient” yet also clean and simple.

a few examples of operations that are relatively expensive today:
- Network communication: even within a datacenter, a round-trip message exchange can take 10–50 μs, 
  which is tens of thousands of instruction times. Wide-area round-trips can take 10–100 ms.
- I/O to secondary storage: 
  - disk I/O operations typically take 5–10 ms, which is millions of instruction times.
  - Flash storage takes 10–100 μs. 
  - New emerging nonvolatile memories may be as fast as 1 μs, but this is still around 2000 instruction times.
- Dynamic memory allocation (malloc in C, new in C++ or Java) typically involves significant overhead for allocation, 
  freeing, and garbage collection. 一次性分配大内存比多次分配小内存更加高效率
- Cache misses: fetching data from DRAM into an on-chip processor cache takes a few hundred instruction times; 
  in many programs, overall performance is determined as much by cache misses as by computational costs.

Efficiency 与 Complexity 矛盾时候：
If the faster design adds a lot of implementation complexity, or if it results in more complicated interfaces, 
then it may be better to start off with the simpler approach and optimize later if performance turns out to be a problem.

### Measure before modifying
If you start making changes based on intuition, you’ll waste time on things that don’t actually improve performance, 
and you’ll probably make the system more complicated in the process.

Before making any changes, measure the system’s existing behavior.
- First, the measurements will identify the places where performance tuning will have the biggest impact.
  You’ll need to measure deeper to identify in detail the factors that contribute to overall performance
- The second purpose of the measurements is to provide a baseline, so that you can re-measure performance
  after making your changes to ensure that performance actually improved.

### Design around the critical path




