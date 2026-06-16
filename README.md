# AI 图像医院 (Image Hospital V2.0)

基于大模型的图像质量诊断与智能修复平台

## 🎯 项目概述

Image Hospital 是一个将图像修复流程医疗化的智能Web应用，集以下功能于一体：

- **AI 挂号** - 上传图像并生成患者ID
- **图像体检** - 自动分析图像质量（IQA）
- **智能诊断** - 利用大模型分析问题原因
- **治疗方案** - 推荐修复策略
- **图像修复** - 调用AIGC模型修复图像
- **术后复查** - 前后对比和量化分析
- **病历生成** - 自动生成PDF诊疗报告
- **历史档案** - 数据库管理患者记录

## 📋 项目结构

```
image-hospital/
├── app.py                  # Flask主应用
├── config.py              # 配置文件
├── requirements.txt       # 依赖列表
├── .env.example          # 环境变量示例
├── models/               # 数据库模型
│   ├── image.py         # 图像记录模型
│   ├── diagnosis.py     # 诊断结果模型
│   └── treatment.py     # 治疗记录模型
├── routes/              # API路由
│   ├── main.py         # 主页路由
│   ├── upload.py       # 上传路由
│   ├── diagnosis.py    # 诊断路由
│   ├── treatment.py    # 治疗路由
│   ├── report.py       # 报告生成路由
│   └── history.py      # 历史查询路由
├── services/           # 业务逻辑服务
│   ├── upload_service.py        # 上传服务
│   ├── iqa_service.py          # 图像质量评估服务
│   ├── deepseek_service.py     # DeepSeek API集成
│   ├── replicate_service.py    # Replicate API集成
│   └── pdf_service.py          # PDF生成服务
├── templates/          # HTML模板
│   ├── base.html      # 基础模板
│   └── index.html     # 首页
├── static/            # 静态资源
│   ├── css/          # 样式表
│   └── js/           # JavaScript文件
├── uploads/           # 上传图像存储
├── restored/          # 修复图像存储
└── reports/           # PDF报告存储
```

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/z-fei421/image-hospital.git
cd image-hospital
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env`，配置数据库和API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```
FLASK_ENV=development
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/image_hospital
DEEPSEEK_API_KEY=your_api_key
REPLICATE_API_TOKEN=your_token
```

### 5. 创建数据库

```bash
# 创建MySQL数据库
mysql -u root -p
CREATE DATABASE image_hospital CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 6. 运行应用

```bash
python app.py
```

访问 `http://localhost:5000`

## 🔧 核心功能说明

### IQA 质量评价

系统使用以下指标评估图像质量（0-100）：

- **清晰度** - Laplacian Variance
- **对比度** - 标准差
- **亮度** - 平均灰度值
- **噪声** - 局部方差统计
- **压缩损伤** - JPEG Block Artifact Estimation

综合健康度计算：

```
Health Score = 0.35×Sharpness + 0.25×Contrast + 0.20×Brightness + 0.20×Noise
```

等级划分：

- A: 85-100 (优秀)
- B: 70-84 (良好)
- C: 50-69 (一般)
- D: 0-49 (较差)

### API 接口

#### 上传图像

```
POST /api/upload
Content-Type: multipart/form-data
Body: file=<image_file>

Response:
{
  "success": true,
  "patient_id": "P202606220001",
  "image_id": 1,
  "resolution": "1920x1080"
}
```

#### 图像体检

```
POST /api/check/<image_id>

Response:
{
  "success": true,
  "diagnosis_id": 1,
  "metrics": {
    "health_score": 75.5,
    "sharpness": 80.0,
    "contrast": 72.0,
    "brightness": 70.0,
    "noise": 80.0,
    "compression": 85.0,
    "health_grade": "B"
  }
}
```

#### AI诊断

```
POST /api/ai-diagnosis/<diagnosis_id>

Response:
{
  "success": true,
  "diagnosis": { ... },
  "ai_result": {
    "diagnosis_text": "患者存在明显JPEG压缩损伤...",
    "problems": ["低清晰度", "高噪声"],
    "recommendations": ["超分辨率增强", "去噪处理"],
    "risk_level": "medium"
  }
}
```

#### 获取历史记录

```
GET /api/history

Response:
{
  "success": true,
  "total": 5,
  "history": [ ... ]
}
```

## 📊 数据库模型

### ImageRecord (图像记录)

存储上传的图像基本信息

### DiagnosisRecord (诊断结果)

存储IQA分析结果和AI诊断

### TreatmentRecord (治疗记录)

存储修复过程和结果

## 🔐 环境变量

| 变量 | 说明 | 示例 |
|-----|------|------|
| FLASK_ENV | 运行环境 | development |
| DATABASE_URL | 数据库连接 | mysql+pymysql://user:pass@host/db |
| DEEPSEEK_API_KEY | DeepSeek API密钥 | sk-xxx |
| REPLICATE_API_TOKEN | Replicate API令牌 | xxx |

## 📦 依赖库

- Flask - Web框架
- SQLAlchemy - ORM
- Pillow - 图像处理
- OpenCV - 计算机视觉
- NumPy - 数值计算
- ReportLab - PDF生成
- requests - HTTP库

## 🎨 前端技术

- Bootstrap 5 - UI框架
- Chart.js - 图表库
- Vanilla JavaScript - 交互

## 📄 许可证

MIT

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**每一张受损图像，都值得一次重生。** ✨
