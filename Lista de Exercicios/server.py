import socket
import json

def start_server():
    # Configurações do servidor
    host = "127.0.0.1"
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Servidor ouvindo em {host}:{port}")

    # Lista de questões e respostas corretas
    questions_data = [
        {
            "question": "Qual é a capital do Brasil?",
            "options": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"],
            "answer": "Brasília"
        },
        {
            "question": "Quanto é 7 + 8?",
            "options": ["14", "15", "16", "13"],
            "answer": "15"
        }
    ]

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão recebida de {addr}")

        # 1. Envia as questões para o cliente
        questions_to_send = [
            {
                "question": q["question"],
                "options": q["options"]
            } for q in questions_data
        ]
        client_socket.send(json.dumps(questions_to_send).encode())

        # 2. Recebe as respostas do cliente
        client_answers_json = client_socket.recv(1024).decode()
        client_answers = json.loads(client_answers_json)
        print(f"Respostas do cliente: {client_answers}")

        # 3. Processa e avalia as respostas
        score = 0
        results = []
        for i, q in enumerate(questions_data):
            user_answer = client_answers[i]
            correct_answer = q["answer"]
            
            if user_answer == correct_answer:
                score += 1
                result_text = "Correto"
            else:
                result_text = "Incorreto"
            
            results.append({
                "question": q["question"],
                "resultado": result_text
            })

        # 4. Envia o resultado de volta para o cliente
        feedback = {
            "score": score,
            "results": results
        }
        client_socket.send(json.dumps(feedback).encode())

        client_socket.close()

if __name__ == "__main__":
    start_server()