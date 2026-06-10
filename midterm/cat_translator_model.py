import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def train_cat_translator():
    # 1. 讀取資料
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cat_language_dataset.csv')
    if not os.path.exists(file_path):
        print(f"找不到資料集：{file_path}，請先執行 generate_cat_data.py")
        return
        
    df = pd.read_csv(file_path)
    print("資料集載入成功！")
    
    # 2. 資料預處理 (Preprocessing)
    # 將類別變數 (sound_type) 轉換為數值
    le_sound = LabelEncoder()
    df['sound_type_encoded'] = le_sound.fit_transform(df['sound_type'])
    
    # 將目標標籤 (intention) 轉換為數值
    le_intent = LabelEncoder()
    df['intention_encoded'] = le_intent.fit_transform(df['intention'])
    
    # 選擇特徵 (Features) 與目標 (Target)
    X = df[['sound_type_encoded', 'duration_sec', 'pitch_hz', 'time_of_day', 'bowl_empty']]
    y = df['intention_encoded']
    
    # 3. 切分訓練集與測試集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. 建立與訓練模型 (Random Forest)
    print("正在訓練 Random Forest 模型...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # 5. 模型評估
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n模型訓練完成！測試集準確率 (Accuracy): {accuracy:.2%}")
    print("\n詳細分類報告：")
    print(classification_report(y_test, y_pred, target_names=le_intent.classes_))
    
    # 6. 儲存模型與 Encoder (供後續預測使用)
    model_dir = os.path.dirname(os.path.abspath(__file__))
    joblib.dump(clf, os.path.join(model_dir, 'cat_translator_rf_model.pkl'))
    joblib.dump(le_sound, os.path.join(model_dir, 'le_sound.pkl'))
    joblib.dump(le_intent, os.path.join(model_dir, 'le_intent.pkl'))
    print("模型與標籤編碼器已成功儲存！")
    
def translate_cat_behavior(sound_type, duration_sec, pitch_hz, time_of_day, bowl_empty):
    """
    載入模型並測試單筆貓咪行為翻譯
    """
    model_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        clf = joblib.load(os.path.join(model_dir, 'cat_translator_rf_model.pkl'))
        le_sound = joblib.load(os.path.join(model_dir, 'le_sound.pkl'))
        le_intent = joblib.load(os.path.join(model_dir, 'le_intent.pkl'))
    except FileNotFoundError:
        print("尚未訓練模型，請先執行 train_cat_translator()")
        return
        
    try:
        sound_encoded = le_sound.transform([sound_type])[0]
    except ValueError:
        print(f"未知的聲音類型：{sound_type}")
        return
        
    features = [[sound_encoded, duration_sec, pitch_hz, time_of_day, bowl_empty]]
    pred_encoded = clf.predict(features)[0]
    prediction = le_intent.inverse_transform([pred_encoded])[0]
    
    # 加入人類可讀的有趣解釋
    translation_dict = {
        'Hungry': "「人類！我的碗空了，立刻給我罐罐！」",
        'Pet_Me': "「過來摸我，但只能摸三下，多一下我就咬你。」",
        'Angry':  "「滾開！別惹我生氣！」",
        'Open_Door': "「放我出去！...不對，我只是想看門開著，我沒有要出去。」"
    }
    
    print("\n" + "="*50)
    print("正在翻譯貓咪行為...")
    print(f"輸入特徵：聲音=[{sound_type}], 長度=[{duration_sec}s], 音調=[{pitch_hz}Hz], 時間=[{time_of_day}點], 碗是空的=[{bool(bowl_empty)}]")
    print(f"預測意圖：{prediction}")
    print(f"翻譯結果：{translation_dict.get(prediction, '未知')}")
    print("="*50 + "\n")

if __name__ == "__main__":
    # 訓練模型
    train_cat_translator()
    
    # 測試幾個手動案例
    print("\n--- 模擬實際場景翻譯 ---")
    # 場景 1：半夜 3 點，喵喵叫很久，碗是空的
    translate_cat_behavior(sound_type='Meow', duration_sec=3.5, pitch_hz=850, time_of_day=3, bowl_empty=1)
    
    # 場景 2：發出呼嚕聲，靠近你
    translate_cat_behavior(sound_type='Purr', duration_sec=1.5, pitch_hz=200, time_of_day=14, bowl_empty=0)
    
    # 場景 3：嘶嘶叫
    translate_cat_behavior(sound_type='Hiss', duration_sec=2.2, pitch_hz=600, time_of_day=20, bowl_empty=0)
