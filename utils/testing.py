def error_report(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"{e} occurred while executing {func.__name__}")
            return e
    return wrapper
