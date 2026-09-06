from backend.ollama_client import (
    OllamaClient,
    OllamaConnectionError,
    OllamaModelError,
    OllamaTimeoutError,
    OllamaHTTPError,
)


def run():
    client = OllamaClient()
    messages: list[dict[str, str]] = []

    print("=== Prototipo v0.1 — Chat con Ollama ===")
    print("Escriba 'exit' o 'salir' para terminar.\n")

    try:
        while True:
            try:
                user_input = input("Tú: ").strip()
            except EOFError:
                break

            if not user_input:
                continue
            if user_input.lower() in ("exit", "salir"):
                break

            messages.append({"role": "user", "content": user_input})

            try:
                reply = client.send_messages(messages)
            except (
                OllamaConnectionError,
                OllamaModelError,
                OllamaTimeoutError,
                OllamaHTTPError,
            ) as e:
                print(f"\n[Error] {e}\n")
                messages.pop()
                continue

            messages.append({"role": "assistant", "content": reply})
            print(f"\nAsistente: {reply}\n")
    except KeyboardInterrupt:
        print("\n\nSesión terminada.")
    finally:
        client.close()


if __name__ == "__main__":
    run()
