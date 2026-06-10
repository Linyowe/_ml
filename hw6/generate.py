import os
import random
from collections import defaultdict

class MarkovLanguageModel:
    def __init__(self, n=2):
        """
        初始化馬可夫模型
        n: 狀態長度（N-gram），預設 2 代表使用前 2 個字來預測下一個字
        """
        self.n = n
        # model 結構：model[prefix][next_char] = 出現次數
        self.model = defaultdict(lambda: defaultdict(int))
    
    def train(self, text):
        """訓練模型，建立轉移矩陣 (次數統計)"""
        print(f"正在訓練馬可夫模型 (N={self.n})...")
        # 遍歷文本，收集每個長度為 n 的前綴，以及緊接在後的字
        for i in range(len(text) - self.n):
            prefix = text[i:i+self.n]
            next_char = text[i+self.n]
            self.model[prefix][next_char] += 1
            
        print(f"訓練完成！共學習到 {len(self.model)} 種狀態轉移組合。")

    def generate(self, max_length=100, start_prefix=None):
        """根據模型生成文字"""
        if not self.model:
            return "模型尚未訓練！"

        # 如果沒有指定開頭，隨機挑選一個存在於模型中的 prefix 作為開頭
        if start_prefix is None or start_prefix not in self.model:
            start_prefix = random.choice(list(self.model.keys()))
        
        result = list(start_prefix)
        current_prefix = start_prefix

        # 開始一個字一個字生成
        for _ in range(max_length - self.n):
            next_char_options = self.model.get(current_prefix)
            
            if not next_char_options:
                # 如果遇到沒有看過的 prefix (Dead end)，就隨機挑一個重新開始或中斷
                break
                
            chars = list(next_char_options.keys())
            weights = list(next_char_options.values())
            
            # 根據次數(權重)機率性地隨機挑選下一個字
            next_char = random.choices(chars, weights=weights, k=1)[0]
            result.append(next_char)
            
            # 更新目前的 prefix (往後平移一個字)
            current_prefix = "".join(result[-self.n:])
            
        return "".join(result)

def main():
    # 準備存放程式的資料夾 (hw6) 並切換路徑
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    file_path = "tw.txt"
    
    # 如果找不到 tw.txt，我們自動寫入一個測試用的繁體中文語料
    if not os.path.exists(file_path):
        print(f"找不到測試資料 '{file_path}'，系統自動產生一份簡易的 AI 知識語料供測試。")
        sample_text = (
            "人工智慧是計算機科學的一個分支，它企圖了解智能的實質，並生產出一種新的能以人類智能相似的方式做出反應的智能機器。"
            "機器學習是人工智慧的核心，是使計算機具有智能的根本途徑。"
            "深度學習是機器學習研究中的一個新的領域，其動機在於建立、模擬人腦進行分析學習的神經網路。"
            "我們可以使用馬可夫模型來進行自然語言處理，這是一種非注意力的傳統語言模型方法。"
            "馬可夫模型可以用前兩個字預測下一個字，這就是我們這次習題要實作的內容。"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(sample_text)
    
    # 讀取測試資料
    print(f"讀取資料檔案: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    # 清理不必要的換行與空白
    text = text.replace('\n', ' ').replace('\r', '').strip()

    if len(text) < 3:
        print("文本長度太短，無法訓練 N=2 的模型")
        return

    # 實例化模型 (N=2 代表利用前 2 個字預測第 3 個字)
    model = MarkovLanguageModel(n=2)
    model.train(text)
    
    # 生成測試
    print("\n" + "="*40)
    print("隨機文本生成測試 (長度 50 字):")
    print("="*40)
    print("[結果 1]：")
    print(model.generate(max_length=50))
    print("\n[結果 2]：")
    print(model.generate(max_length=50))
    print("="*40)

if __name__ == "__main__":
    main()
