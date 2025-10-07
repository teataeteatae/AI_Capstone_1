import json

# 원본 파일 경로
input_file = "Multistage-Collaborative-Knowledge-Distillation/src/dataset/all_task_train_right_wronghint_answer_B.json"
# 결과 파일 경로
output_file = "Multistage-Collaborative-Knowledge-Distillation/src/dataset/all_task_train_right_wronghint_answer_B_clean.json"

# JSON 파일 읽기
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# 각 항목에서 'response' 값만 빈 문자열로 변경
for item in data:
    if "response" in item:
        item["response"] = ""

# 수정된 JSON 저장
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"✅ 변환 완료! 결과 파일: {output_file}")
