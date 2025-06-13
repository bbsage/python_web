import os
import signal
import time


def init():
    # 註冊訊號處理器
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)  # 支援 Ctrl+C 手動中斷


# 優雅關機函式
def graceful_shutdown(signum, frame):
    print(f"\n📦 收到訊號 {signum}，正在關閉中...")
    print("✅ 清理完成，安全退出")
    os.kill(os.getpid(), signal.SIGTERM)


# 主程式邏輯
def main():
    print("🚀 程式啟動中...")

    try:
        while True:
            print("💡 模擬主程式運作中...")
            time.sleep(5)
    except Exception as e:
        print(f"❗ 程式發生例外: {e}")


# 程式進入點
if __name__ == "__main__":
    init()
    main()
