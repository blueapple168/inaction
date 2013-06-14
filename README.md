Inaction
========

根据项目的规则文件(Inactionfile), 使用Linux内核提供的inotify接口监测文件系统事件,
针对指定文件发生的预期事件执行指定命令.

不同于[incron](http://linux.die.net/man/8/incrond),
[inaction](https://github.com/wonderbeyond/inaction)旨在为一个项目提供文件监测和自动化响应服务.

## Dependencies

- Linux ≥ 2.6.13
- Python ≥ 2.4(not including Python 3.x)

## Install

### Install inaction from PyPI with pip

    $ sudo pip install pyinotify

### Or install inaction directly from source

    # get into source directory
    $ sudo python setup.py install

## Start to use

### Create Inactionfile

在项目下建立 Inactionfile 文件, Inactionfile 的语法类似 [incrontab](http://linux.die.net/man/5/incrontab),
用来申明指定文件在指定事件触发时执行的操作.

Inactionfile中每个规则各占一行, 可以使用 `#` 作为注释行, 空行将被忽略.
示例如下:

    #<path> <event> <command>
    static/css/style.less  IN_CLOSE_WRITE   lessc $pathname > ${path}/style.css

其中 *path* 是相对于项目根目录的路径(也可以是绝对路径), 代表被监测的文件.
path中可以用 `,` 分隔多个路径, 每个路径可以使用Unix路径通配符.

*event* 表示对应文件上预期发生的事件类型, 多个事件用 `,` 分开.
可选的事件类型有:

- **IN_ACCESS** File was accessed
- **IN_ATTRIB** Metadata changed (permissions, timestamps, extended attributes, etc.)
- **IN_CLOSE_WRITE** File opened for writing was closed
- **IN_CLOSE_NOWRITE** File not opened for writing was closed
- **IN_CREATE** File/directory created in watched directory
- **IN_DELETE** File/directory deleted from watched directory
- **IN_DELETE_SELF** Watched file/directory was itself deleted
- **IN_MODIFY** File was modified
- **IN_MOVE_SELF** Watched file/directory was itself moved
- **IN_MOVED_FROM** File moved out of watched directory
- **IN_MOVED_TO** File moved into watched directory
- **IN_OPEN** File was opened

*command* 表示当预期的事件发生时执行的命令, 可以用python内建的模版语法替换出上下文变量, 其中

- pathname: 完整的文件路径名
- path: 文件所在目录
- name: 文件名(不包含路径)

### Start monitoring

    $ cd path/to/my/project/
    $ inaction.py
