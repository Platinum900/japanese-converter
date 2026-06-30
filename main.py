from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pykakasi

app = FastAPI()

# 允許任何來源連線 (方便本地開發與測試)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


kks = pykakasi.kakasi()
kks.setMode("J", "H") # J=Japanese(漢字), H=Hiragana(平假名)
kks.setMode("K", "H") # K=Katakana(片假名), H=Hiragana(平假名)

# 核心調整：
# mode='H' 代表強制輸出平假名
kks.setMode('r', 'Hepburn') # 雖然我們用不到羅馬拼音，但先設定好以免衝突

# 為了確保轉換執行
conv = kks.getConverter()

@app.get("/convert")
@app.get("/convert")
def convert_text(text: str = ""):
    # 使用 splitlines 保留原本的段落格式
    lines = text.splitlines()
    result_data = []
    
    for line in lines:
        line_data = []
        # 將句子轉換並保留對應關係
        converted = conv.do(line)
        for item in converted:
            # item['orig'] 是原字，item['hira'] 是對應假名
            line_data.append({"orig": item['orig'], "hira": item['hira']})
        result_data.append(line_data)
        
    return {"lines": result_data}

# 這是讓你可以直接執行這個檔案
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
