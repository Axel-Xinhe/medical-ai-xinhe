from pinecone import Pinecone,ServerlessSpec
from sentence_transformers import SentenceTransformer

pc = Pinecone(api_key="pcsk_6ZFwxg_3QSAqZAGL3Bk3pN6VZeJzqCVXWUgg44kg5bw8dDZ7xKe4wfS8jRRZ9GVBnNkkB8")

# 创建索引
index_name = "quickstart"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # 使用 all-MiniLM-L6-v2 模型的维度
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        )  # serverless 配置
    )

index = pc.Index(index_name)

model = SentenceTransformer('all-MiniLM-L6-v2')

texts = [
    "人工智能是未来的方向",
    "机器学习需要大量数据",
    "通义千问是一个大语言模型",
    "Pinecone 用于向量搜索"
]

# 生成嵌入
embeddings = model.encode(texts)

# 准备数据
vectors = []
for i, (text, embedding) in enumerate(zip(texts, embeddings)):
    vectors.append({
        "id": f"vec{i}",
        "values": embedding.tolist(),
        "metadata": {"text": text}
    })

# 插入到 Pinecone
index.upsert(vectors=vectors)

query = "什么是大语言模型？"
query_embedding = model.encode([query]).tolist()[0]

# 搜索最相似的向量
result = index.query(
    vector=query_embedding,
    top_k=2,
    include_metadata=True
)

for match in result['matches']:
    print(f"相似度: {match['score']}, 文本: {match['metadata']['text']}")