资产配置分类更新流程

1. 首先，通过 deal-record 项目，可以查询所有的成交记录，更新“资产配置分类表.xlsx” 文件。
2. 运行 .\assetCategoryManager.py，更新 json 配置。
3. 可以进行估值计算了。

账户更新流程

1. 首先，更新 accountManager.py 的代码并运行。
2. account.json 自动更新，可以开始使用了。

指数更新流程

1. 首先，打开 indexValueInfo.json，新增对应的指数条目，填写估值网站和点数网站。
2. 调用 indexValueInfo.py 更新。
3. 可以使用了。