# Python-SM3
最近的密码学实验作业，用python实现的国密SM3标准

由于作者是个十足的傻逼/辣鸡，所以代码冗长难读，所幸经过测试加密结果是正确的，还望轻喷。

## 使用方法

修改明文字符串c的内容即可

```python
if __name__ == "__main__":
    c = 'abc' # 要加密的内容
    m = Fill(c)
    w = Expand(m)
    b = Iteration(m,w)
    print(b)
```

