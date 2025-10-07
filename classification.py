import json, re, os

# ========= 사용자 설정 =========
# 여기에 원본 파일 경로만 넣으면 됨!
input_path = "D:/Capstone/Multistage-Collaborative-Knowledge-Distillation/src/dataset/response_Model_B_to_dataset_A.json"

# 결과는 자동으로 같은 폴더에 저장됨
output_correct = os.path.splitext(input_path)[0] + "_correct.json"
output_wrong   = os.path.splitext(input_path)[0] + "_wrong.json"
# =================================

# ---------- 정규식 ----------
OPT_RE   = re.compile(r'\(([A-Z])\)\s', flags=re.I)
GOLD_RE  = re.compile(r'\(([A-Z])\)', flags=re.I)
FINAL_RE = re.compile(r'(?is)(?:therefore,?\s+)?the\s+answer\s+is\s*[:=]?\s*[\[\(\s]*([A-Z])[\]\)\s]*[\.!\s]*$')

# ---------- 파서 ----------
def extract_option_labels(instruction: str):
    labels = OPT_RE.findall(instruction or "")
    seen, out = set(), []
    for x in (lbl.upper() for lbl in labels):
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def parse_gold_label(output_text: str):
    if not output_text:
        return None
    m = GOLD_RE.search(output_text.strip())
    if m:
        return m.group(1).upper()
    txt = output_text.strip().upper()
    if len(txt) == 1 and 'A' <= txt <= 'Z':
        return txt
    return None

def parse_pred_label(response_text: str):
    if not response_text:
        return None
    lines = [ln.strip() for ln in response_text.strip().splitlines() if ln.strip()]
    if lines:
        m = FINAL_RE.search(lines[-1])
        if m:
            return m.group(1).upper()
    m2 = FINAL_RE.search(response_text)
    if m2:
        return m2.group(1).upper()
    m3 = GOLD_RE.findall(response_text)
    if m3:
        return m3[-1].upper()
    return None

def is_correct_record(rec):
    gold = parse_gold_label(rec.get("output", ""))
    pred = parse_pred_label(rec.get("response", ""))
    if gold is None or pred is None:
        return False

    opts = extract_option_labels(rec.get("instruction", "")) or []
    if opts:
        if gold not in opts or pred not in opts:
            return False

    return pred == gold

# ---------- 입출력 ----------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        head = f.read(4096)
        f.seek(0)
        # JSONL 처리
        if "\n" in head and head.lstrip().startswith("{") and not head.strip().endswith("]"):
            items = []
            for ln in f:
                if ln.strip():
                    items.append(json.loads(ln))
            return items
        return json.load(f)

def save_json(path, records):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

# ---------- 실행 ----------
def main():
    records = load_json(input_path)
    D_plus, D_minus = [], []
    for r in records:
        (D_plus if is_correct_record(r) else D_minus).append(r)

    save_json(output_correct, D_plus)
    save_json(output_wrong, D_minus)

    total = len(records)
    print(f"총 {total}개 중 정답 {len(D_plus)}개 ({len(D_plus)/total*100:.2f}%), 오답 {len(D_minus)}개 ({len(D_minus)/total*100:.2f}%)")
    print(f"정답 파일: {output_correct}")
    print(f"오답 파일: {output_wrong}")

# ---------- 실행 ----------
if __name__ == "__main__":
    main()
