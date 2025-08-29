# medical-ai-journey/scripts/parse_pubmed.py
import gzip
import pandas as pd
from bs4 import BeautifulSoup

def parse_pubmed_xml(xml_gz_path, output_csv, max_records=10):
    """纯净解析：XML → CSV（仅核心逻辑）"""
    records = []
    
    # 1. 读取压缩XML
    with open(xml_gz_path, 'rt', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml-xml')
    
    # 2. 遍历每篇文章（严格匹配PubMed结构）
    for i, article in enumerate(soup.find_all('PubmedArticle')):
        if i >= max_records:
            break
        
        # 3. 提取核心字段（医药数据关键）
        pmid = article.find('PMID').text
        title = article.find('ArticleTitle').text
        
        # 4. 提取摘要（保留结构化标签）
        abstract = ""
        if article.find('Abstract'):
            for text in article.find('Abstract').find_all('AbstractText'):
                label = text.get('Label', '')
                content = text.text
                abstract += f"[{label}] {content}\n" if label else content + "\n"
        
        records.append({
            "pmid": pmid,
            "title": title.strip(),
            "abstract": abstract.strip()
        })
    
    # 5. 保存为CSV（仅此一步输出）
    pd.DataFrame(records).to_csv(output_csv, index=False)

if __name__ == "__main__":
    # 配置路径（与Day2任务完全匹配）
    XML_PATH = "data/medline19n0001.xml"  # 输入文件
    OUTPUT_CSV = "data/pubmed_sample.csv"    # 输出文件
    
    parse_pubmed_xml(XML_PATH, OUTPUT_CSV)
    print(f"✅ 已生成: {OUTPUT_CSV} (共10条记录)")