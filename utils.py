import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time
        h = int(run_time // 3600)
        m = int((run_time % 3600) // 60)
        s = (run_time % 60)
        if h > 0:
            run_time_str = f'{h}时{m}分{s:.3f}秒'
        elif m > 0:
            run_time_str = f'{m}分{s:.3f}秒'
        else:
            run_time_str = f'{s:.3f}秒'
        print(f"函数{func.__name__}运行时长: {run_time_str}")
        return result
    return wrapper


def time2str(timestamp):
    return time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(timestamp)) + f'_{int(timestamp * 1000) % 1000:03d}'



if __name__ == "__main__":
    @timer
    def add(a, b):
        time.sleep(0.1)
        return a + b

    add(1, 2)