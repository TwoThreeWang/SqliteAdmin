# SqliteAdmin

宝塔面板sqlite数据库可视化管理(简单版)

**详细介绍：https://blog.wangtwothree.com/code/209.html**

sqlite 是一款简单好用的数据库，但是在宝塔面板中现在却没有一款可用的可视化管理插件，我在网上找到了一款叫 pySqliteAdmin 的插件，可是官方的插件库里却搜不到了，好不容易找到了离线安装包，却到处报错无法使用。

![图片alt](https://cdn.wangtwothree.com/imgur/8b8NLXL.png ''图片title'')

本想在 pySqliteAdmin 的基础上修改一下，但是发现报错太多了，本人才疏学浅，查找问题太费劲，索性重新开发一款，SqliteAdmin 就是在这样的前提下诞生的，外观是仿照 pySqliteAdmin 来搞的，但是功能比 pySqliteAdmin 简单了许多，一切以本人实际需求出发，能用就行。

# 安装

1、下载

github：https://github.com/TwoThreeWang/SqliteAdmin

下载后如果不是 ZIP 压缩包，自己重新压一下吧

2、安装

登录宝塔后台，选择 软件商店，选择 第三方应用

点击导入插件，选择插件的 ZIP 压缩包

![图片alt](https://cdn.wangtwothree.com/imgur/PalRBjq.png ''图片title'')

点击确定安装

![图片alt](https://cdn.wangtwothree.com/imgur/xrn5wt2.png ''图片title'')

# 使用

1、保留了 pySqliteAdmin 的扫描功能，增加了数据库连接存储功能

- 顶部可以直接输入 sqlite 的绝对路径，点击添加会保存到下方，下次打开就不用再输入了
- 已保存的数据库有两个操作选项，点击管理可以查看数据库下所有表，点击删除会删除保存的链接，不会删除原文件
- 最后是数据库文件扫描，可以设置扫描的目录和文件类型，扫描的结果可以直接点击添加保存

![图片alt](https://cdn.wangtwothree.com/imgur/wVR9mLo.png ''图片title'')

2、这是数据库下所有表的展示界面

- 点击查看会展示表内所有数据

![图片alt](https://cdn.wangtwothree.com/imgur/y0mCTz7.png ''图片title'')

3、SQL 语句执行

- select 语句会展示查询结果
- 非 selct 直接执行

![图片alt](https://cdn.wangtwothree.com/imgur/zhrCubK.png ''图片title'')

![图片alt](https://cdn.wangtwothree.com/imgur/ydLb4Xa.png ''图片title'')
