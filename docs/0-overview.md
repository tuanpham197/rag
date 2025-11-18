# 1. Hướng Dẫn Xây Dựng Ứng Dụng RAG Đơn Giản
 - Một ứng dụng RAG (Retrieval-Augmented Generation) cơ bản được chia thành hai giai đoạn chính: Giai đoạn Chuẩn bị Dữ liệu (Indexing) và Giai đoạn Truy vấn (Querying).

# 1.1. Kiến Trúc Tổng Thể và Các Bước Xây Dựng
 - Giai đoạn 1: Chuẩn bị Dữ liệu (Indexing Pipeline):
    + Mô tả: Xử lý tài liệu nguồn và lưu trữ chúng dưới dạng vector trong Vector Database.
    + Thực hiện: 
        1. Tải dữ liệu: Đọc tài liệu (PDF, Markdown, TXT, v.v.).  
        2. Chia đoạn (Chunking): Cắt tài liệu dài thành các đoạn nhỏ, dễ quản lý.  
        3. Vector hóa (Embedding): Chuyển mỗi đoạn văn bản thành một vector số (embedding).  
        4. Lưu trữ: Lưu các vector này vào Vector Database.
 - Giải đoạn 2: Truy vấn (Querying Pipeline)
    + Mô tả: Nhận câu hỏi từ người dùng, tìm kiếm thông tin liên quan và tạo câu trả lời.
    + Thực hiện:
        1. Nhận truy vấn: Lấy câu hỏi của người dùng.  
        2. Vector hóa truy vấn: Chuyển câu hỏi thành vector.  
        3. Vector Search: Tìm kiếm các vector tương đồng nhất trong Vector Database.  
        4. Tăng cường (Augmentation): Gửi các đoạn văn bản tìm được (ngữ cảnh) và câu hỏi đến LLM.  
        5. Tạo sinh (Generation): LLM tạo ra câu trả lời cuối cùng.
# 1.2. Công cụ và thành phần
 - Khung RAG (Orchestration): LangChain hoặc LlamaIndex
 - Tải & Xử lý Dữ liệu: PyPDF2, MarkdownLoader (của LangChain/LlamaIndex)
 - Mô hình Vector hóa (Embedding Model): all-MiniLM-L6-v2 (lựa chọn model free cân nhắc Qodo/Qodo-Embed-1-1.5B hoặc dùng openAI có phí)
 - Vector Database (Vector Store): ChromaDB
 - Mô hình Ngôn ngữ Lớn (LLM): gpt-4.1-mini

# 1.3. Chi tiết luồng hoạt động
# 1.3.1 Giai đoạn 1: Chuẩn bị Dữ liệu (Indexing)
    - Tải và Chia đoạn:
        Giả sử bạn có một file PDF chứa tài liệu hướng dẫn.
        Sử dụng PyPDF2 hoặc PDFLoader để trích xuất toàn bộ văn bản.
        Sử dụng một chiến lược chia đoạn (ví dụ: chia thành các đoạn 500 ký tự, chồng lấn 50 ký tự) để đảm bảo ngữ cảnh không bị mất giữa các đoạn.
    - Vector hóa và Lưu trữ:
        Mỗi đoạn văn bản được đưa qua Embedding Model để tạo ra một vector (ví dụ: một chuỗi 384 hoặc 1536 con số).
        Các vector này, cùng với đoạn văn bản gốc tương ứng, được lưu trữ vào Vector Database (ví dụ: ChromaDB).
        Kết quả: Vector Database đã sẵn sàng cho việc tìm kiếm.
# 1.3.2. Giai đoạn 2: Truy vấn (Querying)
    - Nhận truy vấn: Người dùng nhập câu hỏi: "Các bước để khởi động hệ thống là gì?"
    - Vector hóa truy vấn: Câu hỏi này được đưa qua cùng một Embedding Model đã dùng ở Giai đoạn 1 để tạo ra một vector truy vấn.
    - Vector Search (Truy xuất):
        + Vector truy vấn được gửi đến Vector Database.
        + Database sử dụng thuật toán tìm kiếm lân cận gần nhất (Nearest Neighbor Search) để tìm ra k vector (ví dụ: k=4) gần nhất với vector truy vấn.
        + Database trả về 4 đoạn văn bản gốc tương ứng với 4 vector đó. Đây chính là ngữ cảnh liên quan.
    - Tăng cường và Tạo sinh:
        + Hệ thống tạo ra một Prompt gửi đến LLM, có cấu trúc như sau:
        ```
        bash
        Bạn là một trợ lý AI chuyên nghiệp. Hãy trả lời câu hỏi sau dựa trên ngữ cảnh được cung cấp.
        Nếu ngữ cảnh không chứa thông tin, hãy nói rằng bạn không tìm thấy câu trả lời.

        Ngữ cảnh:
        [Đoạn văn bản 1]
        [Đoạn văn bản 2]
        [Đoạn văn bản 3]
        [Đoạn văn bản 4]

        Câu hỏi: Các bước để khởi động hệ thống là gì?
        ```
LLM xử lý Prompt này và tạo ra câu trả lời chi tiết, chính xác, chỉ dựa trên thông tin trong ngữ cảnh.
Việc sử dụng các framework như LangChain hoặc LlamaIndex sẽ giúp bạn đơn giản hóa đáng kể quá trình này, vì chúng đã tích hợp sẵn các bước tải, chia đoạn, vector hóa và kết nối với LLM