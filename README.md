# ofd2txt

## 使用截图

![](./screenshot.png)

## Usage

命令行调用
```bash
python3 ofd_test.py 1.ofd
```

代码中引用
```python
from ofdtotext import OFDFile


doc = OFDFile('test.ofd')
print(doc.get_text())
```
# Need Help?
有任何问题请提Issue或者联系 **albertofwb@gmail.com**。

# ref
核心代码参考自 [ofd2img](https://github.com/geniusnut/ofd2img)
