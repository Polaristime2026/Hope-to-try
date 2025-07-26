# Richards

# 文脉点睛1.0 - 开发文档

## 项目概述

本项目是一个基于微信小程序的汉语盲文翻译工具，主要由前端小程序和后端 Flask 服务器组成。后端提供汉语转换为盲文的 API，前端调用该 API 以完成翻译功能。

## 代码结构

```
├── api.py                 # Flask API 服务器
├── ChineseToBraille.py     # 汉语转盲文核心逻辑
├── main.py                 # 服务器入口
├── app.js                 # 小程序入口文件
├── app.json               # 小程序全局配置
├── project.config.json     # 微信小程序配置文件
├── project.private.config.json # 微信小程序私有配置
```

---

## 1. `main.py` - 服务器入口

### 功能概述

* 该文件是服务器的主入口，负责启动 Flask 服务器。

### 代码解析

```python
from api import app

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
```

* `from api import app`：从 `api.py` 导入 Flask 应用。
* `app.run(host='0.0.0.0', port=5000)`：启动 Flask 服务器，监听 `0.0.0.0:5000`。
* `if __name__ == '__main__':` 确保代码在作为主程序运行时执行。

---

## 2. `api.py` - API 服务器

### 功能概述

* 提供 HTTP API，将用户输入的汉字转换为盲文。

### 代码解析

```python
from flask import Flask, jsonify, request
from ChineseToBraille import se_is_ts

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    txt = data.get('text', '')
    if txt == '':
        rtxt = ''
    else:
        rtxt = se_is_ts(txt)
    return jsonify({'braille': rtxt})

if __name__ == '__main__':
    app.run(debug=True)
```

* `@app.route('/translate', methods=['POST'])`：定义 `/translate` API，支持 `POST` 请求。
* `request.json`：获取请求数据。
* `se_is_ts(txt)`：调用 `ChineseToBraille.py` 中的转换函数。
* `jsonify({'braille': rtxt})`：返回 JSON 格式的盲文翻译结果。

---

## 3. `ChineseToBraille.py` - 汉语转盲文核心逻辑

### 功能概述

* 解析汉字的拼音并转换为盲文。
* 处理声母、韵母、声调和标点符号。

### 代码解析

```python
from pypinyin import pinyin, Style
import re
```

* `pypinyin`：用于获取汉字拼音。
* `re`：用于匹配汉字和符号。

#### 盲文映射字典

```python
dict0, dict1, dict2, dict3, num_dict = {...}  # 盲文映射字典
```

* `dict0`：特定拼音直接对应的盲文。
* `dict1`：声母对应盲文。
* `dict2`：韵母对应盲文。
* `dict3`：声调对应盲文。
* `num_dict`：数字对应盲文。

#### 汉字转拼音

```python
def ch_to_py(chtxt):
    return [item[0] for item in pinyin(chtxt, style=Style.TONE3)]
```

* `pinyin(chtxt, style=Style.TONE3)`：获取带声调的拼音。
* 返回拼音列表。

#### 拆分拼音（声母 + 韵母）

```python
def sp_py(pytxt):
    ...
    return initial, final
```

* 解析拼音的声母和韵母。
* 处理 `j, q, x` + `u` 变 `v` 的特殊情况。

#### 主要转换函数

```python
def se_is_ts(txt):
    ret = ''
    for char in txt:
        if re.match('[\u4e00-\u9fff]', char):
            pys = ch_to_py(char)
            for py in pys:
                tone = py[-1] if py[-1].isdigit() else ''
                py_body = py[:-1] if tone else py
                if py_body in dict0:
                    ret += dict0[py_body] + dict3.get(tone, '')
                else:
                    shengmu, yunmu = sp_py(py_body)
                    ret += dict1.get(shengmu, '') + dict2.get(yunmu, '') + dict3.get(tone, '')
        else:
            if char in dict0:
                ret += dict0[char]
            elif char.isdigit():
                ret += '⠼' + num_dict.get(char, '')
            else:
                ret += char
    return ret
```

* 遍历输入文本。
* 识别汉字并转换为拼音。
* 根据拼音查找盲文编码。
* 处理特殊字符和数字。

---

## 4. 部署与运行

### 运行服务器

```sh
python main.py
```

服务器将监听 `0.0.0.0:5000`，可通过 `POST /translate` 访问。

### 调用 API

请求示例：

```sh
curl -X POST http://localhost:5000/translate -H "Content-Type: application/json" -d '{"text": "你好"}'
```

返回示例：

```json
{"braille": "⠉⠊⠓⠁⠕"}
```

---

## 5. 未来改进方向

* 增强异常处理。
* 增加拼音纠错功能。
* 支持更多符号和格式。

---

本开发文档可供后续开发者参考，便于理解代码逻辑和进行二次开发。

该文件将记录对文脉点睛2.0版本的开发记录
