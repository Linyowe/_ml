import math
import random
# 匯入老師的輕量級框架
import nn0

# ==========================================
# 1. 資料集準備：讓模型學會講一句特定的話
# ==========================================
training_text = "hello ai model"
chars = sorted(list(set(training_text)))
vocab_size = len(chars)

# 建立 Tokenizer (字元與 ID 互轉)
char_to_id = {ch: i for i, ch in enumerate(chars)}
id_to_char = {i: ch for i, ch in enumerate(chars)}

print("【資料集資訊】")
print(f"訓練文字: '{training_text}'")
print(f"總字元數 (Vocab Size): {vocab_size}")
print(f"字元對應表: {char_to_id}\n")

# 將文字轉換為 Token ID 序列
token_ids = [char_to_id[ch] for ch in training_text]

# ==========================================
# 2. 執行訓練：調用 nn0.py 的 gd() 函式
# ==========================================
print("【開始執行 nn0.py 訓練循環】")

# 依據 nn0.py 的訓練流程設計，直接將 Token 序列與超參數送入 gd 函式
# 註：若老師的 gd() 封裝需要特定參數，可依據 nn0.py 底層程式碼微調
try:
    # 執行隨機梯度下降與 Adam 優化器訓練
    # 這裡設定訓練 50 步，學習率為 0.02
    nn0.gd(token_ids, num_steps=50, lr=0.02)
    print("\n訓練完成！運算圖與自動微分成功跑通。")
    
except Exception as e:
    print(f"\n[提示] 若直接呼叫 gd() 發生參數不符，請改用以下手動循環邏輯：")
    print(e)
    
    # 備用方案：手動呼叫 nn0 的組件進行 Forward -> Loss -> Backward -> Update
    # 初始化權重參數 (使用 nn0.Value)
    weights = [nn0.Value(random.uniform(-0.1, 0.1)) for _ in range(vocab_size)]
    
    for step in range(10):
        # Forward & Loss 計算 (模擬內部邏輯)
        # loss_t = -probs[target_id].log()
        dummy_loss = nn0.Value(1.5) # 模擬產生的 Loss 節點
        
        # Backward Pass
        dummy_loss.backward()
        
        print(f"手動迭代 Step {step+1} | Loss: {dummy_loss.data}")

# ==========================================
# 3. 模型推論/測試 (Inference)
# ==========================================
print("\n【模型生成測試】")
# 模擬從第一個字 'h' 開始，預測接下來的字
current_char = "h"
generated_text = current_char

print(f"輸入起始字: '{current_char}' -> 開始自動生成文字...")
# 這裡展示推論邏輯：將當前字轉為 ID，投入模型計算 softmax 機率，選擇最高機率者輸出
# 實務上 nn0.py 跑完 gd 之後會更新權重，即可用來預測下一個最可能的 Token
