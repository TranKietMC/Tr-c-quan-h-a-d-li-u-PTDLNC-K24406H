# Real-Time Quantitative Financial Analytics Dashboard

Ứng dụng trực tuyến giám sát và phân tích kỹ thuật tài chính thời gian thực (Real-Time Updates) 24/7.

## 🚀 Hướng dẫn Triển khai Online 24/7 (Miễn phí qua Streamlit Community Cloud)

### Bước 1: Đưa Code lên GitHub
1. Tạo một Repository mới trên GitHub (Công khai - Public hoặc Riêng tư - Private).
2. Upload toàn bộ các file trong thư mục này lên Repository:
   - `app.py`
   - `requirements.txt`
   - `README.md`

### Bước 2: Deploy ứng dụng lên Streamlit Cloud
1. Truy cập [share.streamlit.io](https://share.streamlit.io) và đăng nhập bằng tài khoản GitHub.
2. Nhấn nút **"New app"**.
3. Chọn Repository, Branch (`main`), và Main file path là `app.py`.
4. Nhấn **"Deploy!"**. 
5. Sau 1-2 phút, ứng dụng sẽ có đường dẫn công khai 24/7 dạng: `https://<ten-app>.streamlit.app`.

---

## 🔬 Hàm lượng Khoa học & Kỹ thuật Nổi bật
1. **Real-Time Data Ingestion Engine**: Sử dụng API REST Coinbase để stream giá BTC/USD và thuật toán Geometric Brownian Motion mô phỏng cổ phiếu S&P500 / Apple.
2. **Streaming Technical Indicators**: Tính toán trực tiếp chỉ báo EMA (12, 26), Relative Strength Index (RSI-14), và dải Bollinger Bands theo từng tick giá.
3. **Cross-Asset Pearson Correlation Heatmap**: Tính toán ma trận tương quan biến động giá theo thời gian thực giữa Crypto và Thị trường chứng khoán.
4. **Flicker-Free Canvas Rendering**: Tối ưu hóa render phía Client với Plotly `uirevision` và Streamlit dynamic containers, đảm bảo 0% chớp nháy.
