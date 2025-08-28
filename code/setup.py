# -*- coding: utf-8 -*- 

from setuptools import setup, find_packages

setup(
    name="medical_ai_xinhe",  # 项目名（必须唯一）
    version="0.1.0",    # 版本号（企业必填）
    packages=find_packages(),  # 自动发现所有Python模块
    install_requires=[      
        "requests>=2.31.0",   # 指定精确版本（避免依赖冲突）
        "pandas==2.0.3",      # 用==锁定版本（生产环境必须）
        "python-dotenv"       # 后续会用于管理API密钥
    ],
    entry_points={  # 生成可执行命令
        "console_scripts": [
            "medical-crawler=scripts.crawler:main"  # 定义命令：medical-crawler
        ]
    },
    author="Axel",
    description="Medical AI pipeline for PubMed data processing",  
   # long_description=open("README.md").read(),
    #long_description_content_type="text/markdown",
)