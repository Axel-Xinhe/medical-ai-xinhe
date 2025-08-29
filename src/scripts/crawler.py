# -*- coding: utf-8 -*- 

import os
import gzip
import shutil
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup  
from tqdm import tqdm # 进度条

# ===== 企业级配置（避免硬编码）=====
CONFIG = {
    "BASE_URL": "https://ftp.ncbi.nlm.nih.gov/pub/lu/PubMedPhrase/",
    "TARGET_FILE": "medline19n0001.xml.gz",
    "OUTPUT_DIR": "data",
    "MAX_RECORDS": 10  # 任务要求只取10条
}


def parse_medline_xml(xml_path: str, max_records: int) -> pd.DataFrame:
    """精准解析PubMed XML（医药数据关键）"""
    records = []
    #open(xml_path, 'rb').read(3)  # 检查BOM头
    with open(xml_path, 'rb') as f:  # 显式指定UTF-8
        soup = BeautifulSoup(f, 'lxml-xml')  # 用lxml解析XML
        
        for i, article in enumerate(soup.find_all('PubmedArticle')):
            if i >= max_records:
                break
            
            # 企业级字段提取（医药场景关键）
            pmid = article.find('PMID').text if article.find('PMID') else "N/A"
            title = article.find('ArticleTitle').text if article.find('ArticleTitle') else "N/A"
            abstract = ""
            
            # 处理多段摘要（PubMed常见结构）
            if article.find('Abstract'):
                for abstract_text in article.find('Abstract').find_all('AbstractText'):
                    label = abstract_text.get('Label', '')
                    text = abstract_text.text
                    abstract += f"[{label}] {text}\n" if label else text + "\n"
            
            records.append({
                "pmid": pmid,
                "title": title.strip(),
                "abstract": abstract.strip()
            })
    
    return pd.DataFrame(records)

def main():
    # 1. 下载压缩文件
    os.makedirs(CONFIG["OUTPUT_DIR"], exist_ok=True)
    download_path = Path(CONFIG["OUTPUT_DIR"]) / CONFIG["TARGET_FILE"]
    # download_file(CONFIG["BASE_URL"] + CONFIG["TARGET_FILE"], download_path)
    
    # 2. 解压文件
    xml_path = Path(CONFIG["OUTPUT_DIR"]) /"medline19n0001.xml"
    
    # 3. 解析XML → CSV
    df = parse_medline_xml(xml_path, CONFIG["MAX_RECORDS"])
    output_csv = Path(CONFIG["OUTPUT_DIR"]) / "pubmed_sample.csv"
    df.to_csv(output_csv, index=False)
    print(f"✅ 生成样本数据: {output_csv} (共{len(df)}条)")

if __name__ == "__main__":
    main()