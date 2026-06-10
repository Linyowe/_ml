import pandas as pd
import numpy as np
import random
import os

def generate_synthetic_cat_data(num_samples=1000):
    """
    生成貓咪行為特徵資料與對應的真實意圖
    """
    data = []
    
    intentions = ['Hungry', 'Pet_Me', 'Angry', 'Open_Door']
    sound_types = ['Meow', 'Purr', 'Hiss', 'Trill', 'Silence']
    
    for _ in range(num_samples):
        intention = random.choice(intentions)
        
        # 根據不同的意圖，產生具有統計分布差異的特徵
        if intention == 'Hungry':
            sound_type = random.choices(sound_types, weights=[0.7, 0.05, 0.0, 0.1, 0.15])[0]
            duration_sec = max(0.1, np.random.normal(3.0, 1.0)) # 叫聲較長
            pitch_hz = max(100, np.random.normal(800, 150)) # 音調較高
            time_of_day = int(np.random.normal(7, 2)) % 24 # 容易發生在清晨或傍晚
            bowl_empty = random.choices([True, False], weights=[0.9, 0.1])[0] # 碗通常是空的
            
        elif intention == 'Pet_Me':
            sound_type = random.choices(sound_types, weights=[0.3, 0.6, 0.0, 0.1, 0.0])[0]
            duration_sec = max(0.1, np.random.normal(1.5, 0.5)) # 呼嚕聲長度不一，叫聲短
            pitch_hz = max(50, np.random.normal(300, 100)) # 音調低，特別是呼嚕聲
            time_of_day = random.randint(0, 23) # 隨時都可能
            bowl_empty = random.choices([True, False], weights=[0.3, 0.7])[0]
            
        elif intention == 'Angry':
            sound_type = random.choices(sound_types, weights=[0.1, 0.0, 0.8, 0.0, 0.1])[0]
            duration_sec = max(0.1, np.random.normal(2.0, 0.8)) # 嘶嘶聲
            pitch_hz = max(100, np.random.normal(600, 200)) # 音調起伏大
            time_of_day = random.randint(0, 23)
            bowl_empty = random.choices([True, False], weights=[0.5, 0.5])[0]
            
        elif intention == 'Open_Door':
            sound_type = random.choices(sound_types, weights=[0.8, 0.0, 0.0, 0.1, 0.1])[0]
            duration_sec = max(0.1, np.random.normal(1.0, 0.3)) # 短促連續的叫聲
            pitch_hz = max(100, np.random.normal(500, 100)) # 中等音調
            time_of_day = random.randint(0, 23)
            bowl_empty = random.choices([True, False], weights=[0.5, 0.5])[0]
            
        # 確保時間在合法範圍
        if time_of_day < 0:
            time_of_day += 24
            
        data.append({
            'sound_type': sound_type,
            'duration_sec': round(duration_sec, 2),
            'pitch_hz': round(pitch_hz, 2),
            'time_of_day': time_of_day,
            'bowl_empty': int(bowl_empty), # True -> 1, False -> 0
            'intention': intention
        })
        
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("正在生成貓語羅塞塔石碑合成資料集...")
    # 確保目錄存在
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    df = generate_synthetic_cat_data(1500)
    
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cat_language_dataset.csv')
    df.to_csv(file_path, index=False)
    print(f"資料集已成功生成並儲存至：{file_path}")
    print("前 5 筆資料預覽：")
    print(df.head())
