import subprocess
import sys


def run_tests():
    try:
        # Chạy pytest và xuất báo cáo HTML
        result = subprocess.run(['pytest', '--html=report.html'], check=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        # In ra kết quả của pytest (nếu cần)
        print(result.stdout.decode())

        # Trả về mã exit của pytest
        return result.returncode

    except subprocess.CalledProcessError as e:
        # In ra lỗi nếu có
        print("Error occurred while running tests:", e.stderr.decode())
        return e.returncode


if __name__ == "__main__":
    # Gọi hàm run_tests khi chạy file này
    exit_code = run_tests()
    sys.exit(exit_code)
