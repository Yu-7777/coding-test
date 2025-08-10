## 実行手順
### podman無しの場合
- 標準入力(要EOF)
```bash
python main.py
```
- ファイル入力
```bash
python main.py < sample.txt
```

### podmanありの場合
- 標準入力(要EOF)
```bash
podman compose run --rm app
```
- ファイル入力
```bash
podman compose run --rm -T sample.txt
```