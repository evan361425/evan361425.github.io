# evan361425

Hi 我的資料整理處，詳見 [GitHub Page](https://evan361425.github.io)

## 客製 Plugins

為了滿足我的一些需求，自己寫了些 [plugins](./lib/)，有需要歡迎取用：

- 在圖片下面加個標題；
- 在表格上面加個標題；
- 在本地端測試時，只建制特定文件，這樣不用每次重建一大堆東西。

## 本地端啟動

需求：

- python >= 3.8

建置：

```bash
# MkDocs
pip install -r requirements.txt
# 我的客製化 plugins
pip install -e lib
```

啟動：

```bash
mkdocs build   
mkdocs serve   
```
