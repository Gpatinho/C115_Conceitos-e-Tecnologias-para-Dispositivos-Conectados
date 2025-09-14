import threading
import time
import random
import tkinter as tk

# Configuração da janela
janela = tk.Tk()
janela.title("Show de Fogos de Artifício")
canvas = tk.Canvas(janela, width=600, height=400, bg="black")
canvas.pack()

# Controle global
rodando = False

# Cores disponíveis
cores = ["red", "green", "blue", "yellow", "magenta", "cyan", "orange"]

# Função principal
def fogo_de_artificio(nome, rajada):
    x = random.randint(50, 550)
    y = 380
    cor = random.choice(cores)

    altura_max = random.randint(3, 10)  # altura aleatória
    print(f"[Rajada {rajada}] {nome} lançado 🚀")

    # Sobe até altura definida
    for i in range(altura_max):
        canvas.create_oval(x-2, y-2, x+2, y+2, fill="white")
        janela.update()
        print(f"[Rajada {rajada}] {nome} subindo... altura {i+1}")
        time.sleep(0.05)
        y -= 20

    # Explode
    explosoes = ["BOOM!!!", "POW!!!", "KABUM!!!", "BANG!!!"]
    explosao = random.choice(explosoes)
    print(f"[Rajada {rajada}] {nome} EXPLODIU -> {explosao}")

    for _ in range(15):
        dx = random.randint(-50, 50)
        dy = random.randint(-50, 50)
        canvas.create_oval(x+dx, y+dy, x+dx+5, y+dy+5, fill=cor, outline=cor)
        janela.update()
        time.sleep(0.05)

    print(f"[Rajada {rajada}] {nome} desapareceu...\n")

# Loop que dispara fogos continuamente
def controlador(qtd):
    i = 0
    rajada = 0

    while rodando:
        rajada += 1
        print("\n" + "="*40)
        print(f"🎇 Iniciando RAJADA {rajada} com {qtd} fogos")
        print("="*40)

        threads = []
        for _ in range(qtd):  # quantidade por rajada = nº threads
            i += 1
            nome = f"Fogo-{i}"
            t = threading.Thread(target=fogo_de_artificio, args=(nome, rajada))
            t.start()
            threads.append(t)
            time.sleep(0.1)  # pequeno intervalo dentro da rajada

        atraso = random.uniform(0.8, 2.0)  # intervalo entre rajadas
        print(f"⏳ Aguardando {atraso:.2f}s até próxima rajada...\n")
        time.sleep(atraso)

# Iniciar Show
def iniciar_show():
    global rodando
    if not rodando:
        try:
            qtd = int(entry_qtd.get())
            if qtd < 1:
                qtd = 1
        except:
            qtd = 1
        rodando = True
        threading.Thread(target=controlador, args=(qtd,), daemon=True).start()
        print("🎆 Show iniciado!\n")

# Parar Show
def parar_show():
    global rodando
    rodando = False
    print("⛔ Show interrompido!\n")

# Função para limpar o canvas
def limpar_canvas():
    canvas.delete("all")
    print("🧹 Tela limpa!\n")

# Botões e entrada
frame_botoes = tk.Frame(janela, bg="black")
frame_botoes.pack(pady=10)

tk.Label(frame_botoes, text="Qtd por rajada:", bg="black", fg="white").pack(side="left")
entry_qtd = tk.Entry(frame_botoes, width=5)
entry_qtd.insert(0, "3")
entry_qtd.pack(side="left", padx=5)

botao_show = tk.Button(frame_botoes, text="Iniciar Show", command=iniciar_show)
botao_show.pack(side="left", padx=10)

botao_parar = tk.Button(frame_botoes, text="Parar", command=parar_show)
botao_parar.pack(side="left", padx=10)

botao_limpar = tk.Button(frame_botoes, text="Limpar", command=limpar_canvas)
botao_limpar.pack(side="left", padx=10)

janela.mainloop()
