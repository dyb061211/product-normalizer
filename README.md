# Product Normalizer

Product Normalizer 是一个基于 Python 和 Pandas 的商品数据标准化工具。

程序读取 UPC 数据和商品数据，对列名和字段内容进行标准化，
检查缺失值、重复值等数据质量问题，合并两份数据并最终导出标准化 Excel 文件。

## 功能

- 读取 Excel 数据
- 根据配置文件统一列名
- 标准化 SKU、UPC 和文本字段
- 检查必需列
- 检测空值和重复值
- 生成数据校验报告
- 清洗无效数据
- 根据 SKU 合并 UPC 和商品数据
- 导出标准化 Excel
- 记录程序运行日志
- 使用 pytest 进行自动化测试

## 项目结构

```text
product-normalizer/
├── config/
│   └── column_aliases.json
│
├── data/
│   ├── input/
│   │   ├── upc.xlsx
│   │   └── products.xlsx
│   └── output/
│       ├── standardized_products.xlsx
│       └── validation_report.xlsx
│
├── logs/
│   └── app.log
│
├── product_normalizer/
│   ├── cleaner.py
│   ├── exceptions.py
│   ├── exporter.py
│   ├── logging_config.py
│   ├── mapper.py
│   ├── merger.py
│   ├── reader.py
│   ├── settings.py
│   └── validator.py
│
├── tests/
├── main.py
├── README.md
└── requirements.txt
```

## 安装依赖

创建并激活虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
```

安装依赖：

```bash
python -m pip install -r requirements.txt
```

## 输入文件

UPC 文件：

```text
data/input/upc.xlsx
```

至少需要：

```text
sku
upc
```

商品文件：

```text
data/input/products.xlsx
```

至少需要：

```text
sku
```

原始 Excel 的列名可以通过：

```text
config/column_aliases.json
```

配置别名。

## 运行程序

在项目根目录执行：

```bash
python main.py
```

## 输出文件

标准化商品数据：

```text
data/output/standardized_products.xlsx
```

数据校验报告：

```text
data/output/validation_report.xlsx
```

运行日志：

```text
logs/app.log
```

## 运行测试

执行全部测试：

```bash
python -m pytest
```