from google import genai

# 1. Dán API KEY MỚI vào đây
client = genai.Client(api_key="AIzaSyBmfTa7gKY94vvR4Ri5FXNI_P8QmIfwu9g")

print("--- Đang thử kết nối với Gemini 2.0 Flash... ---")
try:
    # Thư viện mới dùng client.models.generate_content
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents="Xin chào, hãy dịch từ 'Apple' sang tiếng Việt"
    )
    print("AI trả lời:", response.text)
    print("--- THÀNH CÔNG RỰC RỠ! ---")
except Exception as e:
    print(f"Lỗi: {e}")