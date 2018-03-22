# hexo-python-admin

这是一个使用Python为hexo写的管理页面，基于Django

目前还在开发中 [开发日志](https://www.epis2048.net/categories/hexo-python-admin/ "开发日志") / [最新日志（2018-3-22）](https://www.epis2048.net/2018/hexo-python-admin-updatelog-2018-3-22/ "最新日志（2018-3-22）") / [基础配置](https://www.epis2048.net/2018/about-basic-config/ "基础配置")

目前必须运行于和hexo部署的同一台服务器上面，远期可能会增加远程推送的功能

### 关于目前进度的说明

较[这里](https://www.epis2048.net/2018/hexo-python-admin/ "这里")比仅仅完成了文章和页面的基础功能，文章尚不支持tag和category。

> update 2018-3-22:

> 完成了密码登录等......但还差不少

### 关于运行环境的说明

因为未完成管理员登录的部分，所以程序目前未经hexo实际服务器的测试，只是将我博客的内容下载下来查看效果。

我主要用Windows写，可以通过wfastcgi.py链接到IIS运行。

> update 2018-3-22:

> 快了。。再多完成一部分我就准备放在服务器上测试了

### 关于代码比较凌乱的事情

时间仓促，各种凌乱...应该还有不少遗留的没啥用的代码，回来找时间检查一下。

目前data.py下两个class未增添实际内容，待完成大部分之后会使用这两个class的
