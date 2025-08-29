from bs4 import BeautifulSoup
import csv
import re

# 从文件读取XML数据并使用BeautifulSoup解析
def parse_xml_file_with_bs4(file_path):
    try:
        # 读取XML文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            xml_content = file.read()
        
        # 使用BeautifulSoup解析XML，指定'xml'解析器
        soup = BeautifulSoup(xml_content, 'xml')
        
        # 查找所有PubmedArticle元素
        articles = soup.find_all('PubmedArticle')
        
        # 准备存储数据的列表
        data = []
        
        # 遍历每个文章
        for article in articles:
            # 提取PMID
            pmid_elem = article.find('PMID')
            pmid = pmid_elem.text.strip() if pmid_elem and pmid_elem.text else "N/A"
            
            # 提取文章标题
            title_elem = article.find('ArticleTitle')
            title = title_elem.text.strip() if title_elem and title_elem.text else "N/A"
            
            # 提取摘要文本
            abstract_elem = article.find('Abstract')
            abstract = abstract_elem.text.strip() if abstract_elem and abstract_elem.text else ""
            
            # 解析摘要中的各个部分
            background = ""
            method = ""
            results = ""
            
            # 使用正则表达式提取各部分
            background_match = re.search(r'\[BACKGROUND\](.*?)(?=\[|$)', abstract, re.DOTALL)
            if background_match:
                background = background_match.group(1).strip()
            
            method_match = re.search(r'\[METHOD\](.*?)(?=\[|$)', abstract, re.DOTALL)
            if method_match:
                method = method_match.group(1).strip()
            
            results_match = re.search(r'\[RESULTS\](.*?)(?=\[|$)', abstract, re.DOTALL)
            if results_match:
                results = results_match.group(1).strip()
            
            # 添加到数据列表
            data.append([pmid, title, background, method, results])
        
        return data
    
    except Exception as e:
        print(f"解析XML文件时出错: {e}")
        return []

# 将数据写入CSV文件
def write_to_csv(data, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # 写入表头
            writer.writerow(['PMID', 'ArticleTitle', 'Background', 'Method', 'Results'])
            # 写入数据
            writer.writerows(data)
        
        print(f"CSV文件已生成: {output_file}，包含 {len(data)} 条记录")
        return True
    
    except Exception as e:
        print(f"写入CSV文件时出错: {e}")
        return False

# 主函数
def main():
    # 输入和输出文件路径
    xml_file_path = 'data/medline19n0001.xml'  # 替换为您的XML文件路径
    csv_file_path = 'data/pubmed_sample.csv'
    
    # 解析XML文件
    data = parse_xml_file_with_bs4(xml_file_path)
    
    if data:
        # 写入CSV文件
        write_to_csv(data, csv_file_path)
        
        # 打印前几行数据作为预览
        print("\n前几行数据预览:")
        for i, row in enumerate(data[:2]):  # 显示前2条记录
            print(f"记录 {i+1}: {row}")
    else:
        print("没有解析到数据，请检查XML文件路径和格式")

if __name__ == "__main__":
    main()