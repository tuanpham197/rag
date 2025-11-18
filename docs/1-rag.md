# 1. RAG là gì ? 
 - RAG là viết tắt của Retrieval-Augmented Generation, có thể dịch là "Tạo sinh Tăng cường bằng Truy xuất". 
    Đây là một kỹ thuật AI tiên tiến giúp cải thiện chất lượng câu trả lời của các Mô hình Ngôn ngữ Lớn (LLM) như ChatGPT.
    Thay vì chỉ dựa vào kiến thức đã được "học" từ trước (vốn có thể bị lỗi thời hoặc không đầy đủ), RAG cho phép LLM truy cập và sử dụng thông tin từ các nguồn dữ liệu bên ngoài một cách linh hoạt.

 - Cách hoạt động cơ bản của RAG:
    Tiếp nhận yêu cầu: Hệ thống nhận một câu hỏi hoặc yêu cầu từ người dùng.
    Truy xuất thông tin (Retrieval): Thay vì trả lời ngay, hệ thống tìm kiếm trong một kho kiến thức (ví dụ: tài liệu nội bộ của công ty, cơ sở dữ liệu, website) để tìm ra những thông tin liên quan nhất đến yêu cầu.
    Tăng cường ngữ cảnh: Những thông tin vừa tìm được sẽ được kết hợp với câu hỏi ban đầu của người dùng để tạo thành một "lời nhắc" (prompt) đầy đủ và giàu ngữ cảnh hơn.
    Tạo câu trả lời (Generation): Lời nhắc tăng cường này được gửi đến LLM. Dựa trên ngữ cảnh được cung cấp, LLM sẽ tạo ra một câu trả lời chính xác, phù hợp và đáng tin cậy hơn.

 - Lợi ích chính của RAG:
    Giảm "ảo giác" (hallucination): Hạn chế việc LLM bịa đặt thông tin vì câu trả lời được dựa trên dữ liệu thực tế được truy xuất.
    Tăng tính cập nhật: Cho phép LLM truy cập thông tin mới nhất mà không cần huấn luyện lại toàn bộ mô hình, giúp tiết kiệm chi phí và thời gian.
    Tăng độ tin cậy: Câu trả lời có thể đi kèm trích dẫn nguồn, giúp người dùng dễ dàng kiểm chứng