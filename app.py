import os

def main():
    secret_user = os.getenv("MY_SECRET_USER", "default_user")
    secret_pass = os.getenv("MY_SECRET_PASS", "default_pass")

    print(f"Hello from Python app!")
    print(f"Secret username: {secret_user}")
    print(f"Secret password: {secret_pass}")

    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
