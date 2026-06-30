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
def convert_text(text: str = ""):
    # 簡單且暴力的方式
    result = conv.do(text)
    # 如果 result 本身就是字串，直接回傳
    if isinstance(result, str):
        return {"original": text, "hiragana": result}
    # 如果是列表，嘗試轉換
    return {"original": text, "hiragana": "".join([str(item.get('hira', '')) for item in result])}

# 這是讓你可以直接執行這個檔案
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)