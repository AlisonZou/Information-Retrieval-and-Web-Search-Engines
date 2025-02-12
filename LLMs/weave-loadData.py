from weaviate import Client
import json

# 初始化 Weaviate 客户端
client = Client(url="http://localhost:8080/")

# 检查并删除现有类（如果需要）
class_name = "SimSearch"
existing_classes = [class_["class"] for class_ in client.schema.get().get("classes", [])]
if class_name in existing_classes:
    client.schema.delete_class(class_name)
    print(f"Deleted existing class '{class_name}'.")

# 创建新类
class_obj = {
    "class": "SimSearch",
    "vectorizer": "text2vec-transformers",
}
client.schema.create_class(class_obj)
print(f"Class '{class_name}' created successfully.")

# 从本地文件读取数据
try:
    with open("data.json", "r") as file:
        data = json.load(file)
    print(f"Loaded {len(data)} records from data.json")
except Exception as e:
    print(f"Failed to load data.json: {e}")
    exit(1)

# 发送数据到 Weaviate
with client.batch as batch:
    batch.batch_size = 100
    for i, d in enumerate(data):
        print(f"\nImporting datum: {i}")
        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        }
        print(f"Properties: {properties}")
        client.batch.add_data_object(properties, "SimSearch")
