import threading
from app import app
from app.scheduler import run_scheduler

if __name__ == "__main__":
    print("启动后台任务调度器...")
    # 在一个单独的线程中运行调度器
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # 启动 Flask 应用
    # use_reloader=False 很重要，因为重载器会启动两次应用，导致调度器运行两次
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)