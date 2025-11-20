# --- Ví dụ sử dụng (bạn có thể thay thế bằng dữ liệu thực tế) ---
if __name__ == '__main__':
    # Giả lập lớp Document và dữ liệu
    class Document:
        def __init__(self, page_content, metadata=None):
            self.page_content = page_content
            self.metadata = metadata if metadata is not None else {}
        def __repr__(self):
            return f"Document(page_content='{self.page_content[:30]}...')"

    # Tạo một danh sách lớn các tài liệu để kiểm tra hiệu suất
    long_text = "Đây là một câu dài để kiểm tra. " * 50
    docs_to_process = [Document(page_content=f"Tài liệu số {i}. {long_text}") for i in range(1000)]

    # Chạy phiên bản gốc
    # print("Running original function:")
    # original_chunks = chunk_documents(docs_to_process)

    # Chạy phiên bản tối ưu
    print("\nRunning optimized function:")
    optimized_chunks = chunk_documents_optimized(docs_to_process)

    # So sánh số lượng chunks
    # print(f"\nOriginal function produced {len(original_chunks)} chunks.")
    print(f"Optimized function produced {len(optimized_chunks)} chunks.")