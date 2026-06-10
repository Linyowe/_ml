import os
import re
import xml.etree.ElementTree as ET

# 如果你有安裝其他 LLM 套件 (如 google-generativeai 或 ollama)，可以自行替換
try:
    from openai import OpenAI
    client = OpenAI() # 需要設定 OPENAI_API_KEY 環境變數
except ImportError:
    client = None

def is_safe_path(target_path):
    """
    安全控管 (v3-agent-secure)
    檢查路徑是否在當前程式資料夾內部。
    如果是內部的檔案 -> 直接放行
    如果是外部的檔案 -> 攔截並詢問使用者是否核可
    """
    current_dir = os.path.abspath(os.getcwd())
    abs_target_path = os.path.abspath(target_path)
    
    # 如果目標路徑以當前目錄開頭，表示在內部，允許存取
    if abs_target_path.startswith(current_dir):
        return True
    
    # 否則，表示試圖存取專案外的檔案，需要攔截並詢問
    print(f"\n[安全警告] Agent 試圖存取外部檔案: {abs_target_path}")
    while True:
        ans = input("是否核可此次存取？ (y/n): ").strip().lower()
        if ans == 'y':
            return True
        elif ans == 'n':
            return False
        else:
            print("請輸入 y 或 n")

def execute_tool(action, path, content=None):
    """執行工具並回傳結果"""
    # 執行前先過安全控管
    if not is_safe_path(path):
        return f"Error: Permission denied to access {path}. User rejected the request."

    try:
        if action == "read_file":
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        elif action == "write_file":
            # 如果目錄不存在，自動建立
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content or "")
            return f"Success: Wrote to {path}"
        else:
            return f"Error: Unknown action {action}"
    except Exception as e:
        return f"Error executing {action}: {e}"

def parse_xml_and_execute(xml_text):
    """解析 XML (v2-agent-xml) 並執行對應工具"""
    # 尋找 <tool_call> ... </tool_call> 區塊
    match = re.search(r'<tool_call>(.*?)</tool_call>', xml_text, re.DOTALL)
    if not match:
        return None, None
    
    xml_content = match.group(0)
    try:
        root = ET.fromstring(xml_content)
        action = root.find('action').text if root.find('action') is not None else None
        path = root.find('path').text if root.find('path') is not None else None
        
        # content 節點可能不存在（如 read_file）
        content_node = root.find('content')
        content = content_node.text if content_node is not None else None
        
        if action and path:
            print(f"-> Agent 觸發動作: {action} , 目標檔案: {path}")
            result = execute_tool(action, path, content)
            return xml_content, result
        return None, "Error: Invalid XML format, missing action or path."
    except Exception as e:
        return None, f"Error parsing XML: {e}"

SYSTEM_PROMPT = """
你是一個實用的 AI Agent (版本: v3-agent-secure)。
你可以透過輸出 XML 格式來呼叫工具存取檔案。
注意：請不要使用 JSON，一律使用 XML 格式來避免格式錯誤。

支援的工具格式：
1. 讀取檔案：
<tool_call>
    <action>read_file</action>
    <path>檔案路徑</path>
</tool_call>

2. 寫入檔案：
<tool_call>
    <action>write_file</action>
    <path>檔案路徑</path>
    <content>寫入內容</content>
</tool_call>

請在你的思考後，如果有需要操作檔案，輸出上述 XML。
"""

def chat_loop():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    print("=== Agent0 (v3-agent-secure) 已啟動 ===")
    print("提示：已支援 XML 格式防呆，並加入檔案安全控管機制。")
    print("輸入 'exit' 或 'quit' 離開\n")
    
    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            break
            
        if user_input.lower() in ['exit', 'quit']:
            break
            
        messages.append({"role": "user", "content": user_input})
        
        # --- 呼叫 LLM ---
        if client:
            try:
                # 這裡使用 gpt-4o-mini 當範例，你可以換成 gpt-3.5-turbo 等
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                agent_message = response.choices[0].message.content
            except Exception as e:
                print(f"LLM Error: {e}")
                continue
        else:
            # 假資料模擬測試 (當沒有 API key 或環境未設定時)
            print("[警告] 尚未連接真正的 LLM API，啟用 Mock 模式模擬...")
            if "寫" in user_input:
                agent_message = "好的，我將把內容寫入外部檔案。\n<tool_call>\n<action>write_file</action>\n<path>../test_outside.txt</path>\n<content>Hello World</content>\n</tool_call>"
            else:
                agent_message = "我需要讀取上一層目錄的設定檔。\n<tool_call>\n<action>read_file</action>\n<path>../config.ini</path>\n</tool_call>"
            
        print(f"\nAgent: {agent_message}\n")
        messages.append({"role": "assistant", "content": agent_message})
        
        # --- 解析並執行工具 ---
        xml_called, result = parse_xml_and_execute(agent_message)
        if xml_called:
            print(f"Tool Result: {result}\n")
            # 將結果送回給 LLM 繼續判斷
            messages.append({"role": "user", "content": f"工具執行結果:\n{result}"})

if __name__ == "__main__":
    chat_loop()
