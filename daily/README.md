# 每日练习

每天的 Python/C++ 代码与学习日志放在 `YYYY-MM-DD/` 下，多天共用本目录的 uv 环境。

在仓库根目录运行：

```bash
./scripts/new_day.sh
./scripts/py.sh sync --locked --project daily
./scripts/py.sh run --locked --project daily python daily/2026-11-10/ITR01.py
```

`new_day.sh` 创建当天的 README、`python/` 和 `cpp/` 目录。日志记录学习来源、完成内容、测试结果和下一步。

添加常用依赖：`./scripts/py.sh add --project daily <包名>`。
