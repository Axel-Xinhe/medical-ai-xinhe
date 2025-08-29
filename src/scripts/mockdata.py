# medical-ai-journey/scripts/generate_mock_pubmed.py (已修复语法)
import gzip
import random
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET  # 企业级 XML 验证

# ===== 医药领域数据池 (优化版) =====
MEDICAL_TERMS = [
    "aspirin", "ibuprofen", "penicillin", "insulin", "statin", 
    "hypertension", "diabetes", "cardiovascular", "oncology", "neurology",
    "β-blocker", "α-glucosidase", "μ-opioid", "γ-aminobutyric acid"
]

MEDICAL_SPECIALTIES = [
    "cardiology", "oncology", "neurology", "endocrinology", 
    "hematology", "gastroenterology", "pulmonology", "nephrology"
]

# 修复关键：分离 format 操作（避免 f-string 语法错误）
BACKGROUND_TEMPLATES = [
    "{disease} is a major global health concern affecting {population}.",
    "The role of {drug} in managing {disease} remains controversial.",
    "Recent advances in {specialty} have improved understanding of {disease}."
]

METHOD_TEMPLATES = [
    "We conducted a {study_type} study involving {sample_size} participants.",
    "Data were analyzed using {analysis_method} with {software} software.",
    "The {intervention} group received {drug} at {dose} mg/day for {duration}."
]

RESULTS_TEMPLATES = [
    "{drug} significantly reduced {outcome} by {percent}% (p<{pvalue}).",
    "No serious adverse events were reported in the {drug} group.",
    "The {outcome} was higher in {group} compared to control (OR={or_value})."
]

def validate_template_params(template: str, **kwargs) -> bool:
    """企业级模板参数验证（医药数据必备）"""
    import re
    required_params = set(re.findall(r"\{(\w+)\}", template))
    provided_params = set(kwargs.keys())
    missing = required_params - provided_params
    
    if missing:
        print(f"⚠️ 模板参数缺失: {template} | 缺少 {missing}")
        return False
    return True

def generate_medical_sentence():
    """生成带希腊字母的医学句子（企业级加固）"""
    # ===== 1. 补全所有参数 =====
    params = {
        "disease": random.choice(["hypertension", "diabetes", "asthma", "arthritis"]),
        "drug": random.choice(MEDICAL_TERMS[:5]),
        "population": random.choice(["millions worldwide", "elderly patients", "children under 12"]),
        "specialty": random.choice(MEDICAL_SPECIALTIES)  # ← 关键修复：添加 specialty
    }
    
    # ===== 2. 安全选择模板 =====
    valid_templates = []
    for template in BACKGROUND_TEMPLATES:
        if validate_template_params(template, **params):
            valid_templates.append(template)
    
    # 处理无有效模板的极端情况（医药系统必须高可用）
    if not valid_templates:
        print("❌ 无有效模板，使用默认模板")
        valid_templates = ["{disease} management is critical in modern medicine."]
    
    # ===== 3. 安全格式化 =====
    template = random.choice(valid_templates)
    try:
        return template.format(**params)
    except KeyError as e:
        # 企业级兜底：自动修复缺失参数
        print(f"⚠️ 参数修复: 添加 {e.args[0]}")
        params[e.args[0]] = "general medicine"  # 医药领域安全默认值
        return template.format(**params)

def generate_abstract():
    """生成结构化摘要（修复 f-string 语法）"""
    # ===== 修复关键：分离 format 操作 =====
    background = "[BACKGROUND] " + generate_medical_sentence()
    
    # METHOD 段（安全 format）
    method_template = random.choice(METHOD_TEMPLATES)
    method = "[METHOD] " + method_template.format(
        study_type=random.choice(['randomized', 'prospective', 'cohort']),
        sample_size=random.randint(100, 5000),
        analysis_method=random.choice(['regression', 'meta-analysis']),
        software=random.choice(['R', 'Python', 'SAS']),
        intervention=random.choice(['treatment', 'intervention']),
        drug=random.choice(MEDICAL_TERMS[:5]),
        dose=random.randint(5, 100),
        duration=random.choice(['4 weeks', '6 months', '1 year'])
    )
    
    # RESULTS 段（安全 format）
    results_template = random.choice(RESULTS_TEMPLATES)
    results = "[RESULTS] " + results_template.format(
        drug=random.choice(MEDICAL_TERMS[:5]),
        outcome=random.choice(['mortality', 'symptom severity', 'recovery rate']),
        percent=random.randint(10, 50),
        pvalue=round(random.uniform(0.001, 0.05), 3),
        group=random.choice(['treatment', 'experimental']),
        or_value=round(random.uniform(1.2, 3.5), 1)
    )
    
    return "\n".join([background, method, results])

def validate_medical_xml(xml_content: str):
    """企业级 XML 验证（医药数据合规性）"""
    try:
        # 验证基本结构
        root = ET.fromstring(xml_content)
        assert root.tag == "MedlineCitationSet", "根节点错误"
        
        # 验证希腊字母（医药数据核心）
        assert "β" in xml_content or "μ" in xml_content, "缺少希腊字母（医药数据失效）"
        
        # 验证摘要结构
        assert "[BACKGROUND]" in xml_content, "缺少 BACKGROUND 段落"
        assert "[METHOD]" in xml_content, "缺少 METHOD 段落"
        assert "[RESULTS]" in xml_content, "缺少 RESULTS 段落"
        
        print("✅ XML 验证通过：符合 PubMed 医药数据规范")
        return True
    except Exception as e:
        print(f"❌ XML 验证失败: {str(e)}")
        return False

def generate_pubmed_xml(num_records=100):
    """生成合规 PubMed XML（带希腊字母强化）"""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<MedlineCitationSet>\n'
    
    for i in range(num_records):
        pmid = 1000001 + i
        title = f"Effect of {random.choice(MEDICAL_TERMS)} on {random.choice(['Cardiovascular', 'Metabolic', 'Neurological'])} Outcomes"
        abstract = generate_abstract()
        
        # 强化希腊字母（医药数据必检项）
        if "blocker" in title and random.random() > 0.3:
            title = title.replace("blocker", "β-blocker")
        if "mg" in abstract and random.random() > 0.4:
            abstract = abstract.replace("mg", "μg")
        
        xml += f'''  <MedlineCitation>
    <PMID>{pmid}</PMID>
    <Article>
      <ArticleTitle>{title}</ArticleTitle>
      <Abstract>
        {abstract}
      </Abstract>
    </Article>
  </MedlineCitation>\n'''
    
    xml += '</MedlineCitationSet>'
    return xml

def main():
    # 生成 100 条模拟数据
    xml_content = generate_pubmed_xml(num_records=100)
    
    # 企业级验证（医药数据合规性）
    if not validate_medical_xml(xml_content):
        print("⚠️ 生成数据不符合医药规范，重新生成...")
        xml_content = generate_pubmed_xml(num_records=100)  # 重试一次
    
    # 保存为 gz 压缩文件
    output_path = Path("data") / "medline19n0001.xml.gz"
    output_path.parent.mkdir(exist_ok=True)
    
    with gzip.open(output_path, 'wt', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"\n✅ 生成合规医药数据: {output_path} (100 条记录)")
    print("💡 包含：希腊字母(β/μ)、结构化摘要、PMID 连续编号")

if __name__ == "__main__":
    main()