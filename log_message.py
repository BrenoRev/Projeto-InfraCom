def log_message(text: str, server_id: int = None):
    if server_id:
        text = f"[Server {server_id}]: {text}"

    print(text)
    with open("log.txt", "a") as file:
        file.write(f'\n----------\n{text}')