import socket
import json

def start_client():
    host = "127.0.0.1"
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Recebe as questões
    data = client_socket.recv(1024).decode()
    questions = json.loads(data)

    answers = []
    for q in questions:
        print("\n" + q["question"])
        for i, opt in enumerate(q["options"]):
            print(f"{i+1}) {opt}")
        choice = int(input("Escolha a opção (1-4): "))
        answers.append(q["options"][choice-1])

    # Envia respostas para o servidor
    client_socket.send(json.dumps(answers).encode())

    # Recebe resultado
    feedback = client_socket.recv(1024).decode()
    feedback = json.loads(feedback)

    print("\n--- RESULTADO FINAL ---")
    print(f"Acertos: {feedback['score']}/{len(questions)}")
    for r in feedback["results"]:
        print(f"{r['question']} -> {r['resultado']}")

    client_socket.close()

if __name__ == "__main__":
    start_client()