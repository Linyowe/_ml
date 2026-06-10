# 機器學習課程期末總整報告 (Final Portfolio)

這份文件總結了本學期「機器學習」課程的所有平時習題與期中專案。所有程式碼皆已經過整理與測試，並由 AI 助手 (Gemini 3.1 Pro) 輔助編寫完成。以下為各項作業的詳細說明與程式碼導覽。

---

## 📂 目錄 (Table of Contents)

### 1. [平時作業 1：TSP 爬山演算法 (hw1)](file:///d:/%E6%A9%9F%E6%A2%B0%E5%AD%B8%E7%BF%92/hw1/%E7%BF%92%E9%A1%8C%E4%B8%80.txt)
*   **專案路徑**：`hw1/習題一.txt`
*   **作業說明**：使用爬山演算法 (Hill Climbing) 解決旅行推銷員問題 (TSP)。
*   **實作重點**：
    *   定義城市座標與距離計算。
    *   實作 `height` 函數將尋找最短距離轉換為尋找最高點。
    *   實作 `neighbor` 函數，使用 2-opt 交換法找出最佳鄰居路徑。

### 2. [平時作業 2：演算法圖表與結果 (hw2)](file:///d:/%E6%A9%9F%E6%A2%B0%E5%AD%B8%E7%BF%92/hw2/image.png)
*   **專案路徑**：`hw2/image.png`
*   **作業說明**：平時作業 2 的執行結果截圖或相關圖表展示。

### 3. [平時作業 3：輕量級神經網路訓練 (hw3)](file:///d:/%E6%A9%9F%E6%A2%B0%E5%AD%B8%E7%BF%92/hw3/run_task.py)
*   **專案路徑**：`hw3/run_task.py`
*   **作業說明**：使用輕量級神經網路框架 `nn0` 進行字元生成訓練。
*   **實作重點**：
    *   建構 Tokenizer 將字串 "hello ai model" 轉換為 Token ID 序列。
    *   串接底層訓練框架進行梯度下降 (Gradient Descent) 模型訓練。

### 4. [平時作業 4：Transformer 語言模型實作 (hw4)](file:///d:/%E6%A9%9F%E6%A2%B0%E5%AD%B8%E7%BF%92/hw4/gpt.py)
*   **專案路徑**：`hw4/gpt.py`
*   **作業說明**：參考 Andrej Karpathy "Let's build GPT" (影片 #6) 教學，實作基礎 Transformer 語言模型。
*   **實作重點**：
    *   使用 PyTorch 實作核心元件，包含 Self-Attention (自注意力機制)、Multi-Head Attention、FeedForward 網路與標準 Transformer Block。
    *   內建自動下載 Tiny Shakespeare 資料集進行訓練的邏輯。
    *   用於學習字元層級 (Character-level) 的語言預測與文本生成。

### 5. [平時作業 5：AI Agent 安全框架實作 (hw5)](file:///d:/%E6%A9%9F%E6%A2%B0%E5%AD%B8%E7%BF%92/hw5/agent0.py)
*   **專案路徑**：`hw5/agent0.py`
*   **作業說明**：撰寫一個具有檔案存取權限控管與防呆機制的 LLM Agent。
*   **實作重點**：
    *   **XML 格式防呆 (`v2-agent-xml`)**：規定 Agent 只能透過 `<tool_call>` 的 XML 標籤輸出工具請求，解決了早期 JSON 格式容易出錯與幻覺的問題。
    *   **安全控管與攔截 (`v3-agent-secure`)**：實作了 `is_safe_path` 函數。確保 Agent 只能存取執行目錄內部的檔案；若企圖存取外部檔案，系統會主動攔截並在終端機提示，要求人類使用者手動核可 `(y/n)` 後才放行。

### 6. [平時作業 6：傳統非 Transformer 語言模型 (hw6)](file:///d:/%E6%A9%9F%E6%A2%B0%E5%AD%B8%E7%BF%92/hw6/generate.py)
*   **專案路徑**：`hw6/generate.py`
*   **作業說明**：不依賴現代神經網路與 Attention 機制，使用傳統機率統計方法實作文字預測。
*   **實作重點**：
    *   使用純 Python 實作 **馬可夫鏈 (Markov Chain / N-gram)** 模型。
    *   設定 `N=2`，透過統計「前兩個字」與「下一個字」的轉移機率矩陣，以隨機抽籤的方式生成下一個出現的字。
    *   輕量、無須 GPU、訓練極快，展示了早期自然語言處理的經典演算法。

### 7. [期中專案：喵塞塔石碑 - AI 貓語翻譯機 (midterm)](file:///d:/%E6%A9%9F%E6%A2%B0%E5%AD%B8%E7%BF%92/midterm/report.md)
*   **專案路徑**：`midterm/`
*   **專案類別**：用 LLM/AI 解讀其他語言（貓） / 參考：羅塞塔石碑
*   **實作重點**：
    *   **合成資料生成** (`generate_cat_data.py`)：因為缺乏真實貓語頻譜，撰寫程式產生了包含貓叫種類、音頻、長度、時間與「碗是否空了」等多維度特徵的 1,500 筆資料集。
    *   **機器學習分類器** (`cat_translator_model.py`)：使用 `scikit-learn` 的隨機森林 (Random Forest) 演算法，學習並翻譯貓咪真實意圖 (Hungry, Angry, Pet_Me, Open_Door)，在測試集上準確率高達 92.67%。
    *   **期中書面報告** (`report.md`)：詳實紀錄了研究動機、資料預處理方式、實驗結果（Precision, Recall, F1-score）與未來展望，並註明由 Gemini 輔助編寫。

---

## 🛠️ 開發環境與執行方式 (Requirements)

要執行上述的所有作業腳本，請確保您的 Python 環境安裝了以下依賴套件：

```bash
# 基礎數值運算與機器學習 (hw6, midterm)
pip install pandas numpy scikit-learn joblib

# 深度學習框架 (hw4)
pip install torch

# LLM 串接測試 (hw5 選擇性安裝)
pip install openai
```

進入各自的資料夾後，使用 `python <檔名>.py` 即可執行。各個專案內皆有包含防呆機制（例如自動建立測試語料庫等），以確保程式能在無預先配置的環境下順利演示。
