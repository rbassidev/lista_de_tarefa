import tkinter as tk
from tkinter import ttk, font, messagebox
from tkinter import PhotoImage

#criando janela
janela = tk.Tk()
janela.title("To-do list")
janela.configure(bg="#F0F0F0")
janela.geometry("500x600")

frame_edicao = None

#Função adiconar tarefa
def adicionar_tarefa():
    global frame_edicao

    tarefa = input_tarefa.get().strip()
    if tarefa and tarefa != "Escreva a sua tarefa aqui":
        if frame_edicao is not None:
            atualizar_tarefa(tarefa)
            frame_edicao = None
        else:
            adicionar_item_tarefa(tarefa)
            input_tarefa.delete(0, tk.END)
    else:
        messagebox.showwarning("Entrada inválida", "Por favor, insira uma tarefa")
def adicionar_item_tarefa(tarefa):
    frame_tarefa = tk.Frame(canvas_interior, bg= "white", bd=1, relief=tk.SOLID)

    label_tarefa = tk.Label(frame_tarefa, text=tarefa, font=("Garamond", 16),
                            bg="white", width=25, height=2, anchor="w")
    label_tarefa.pack(side="left", fill="x", padx=10, pady=5)

    botao_editar = tk.Button(frame_tarefa, image=icon_editar, command=lambda f=frame_tarefa,
                         l=label_tarefa: preparar_edicao(f, l), bg="white", relief="flat")
                        
    botao_editar.pack(side="right", padx=5)

    botao_deletar = tk.Button(frame_tarefa, image=icon_deletar, command=lambda f=frame_tarefa:
                          deletar_tarefa(f), bg="white", relief=tk.FLAT)
    botao_deletar.pack(side="right", padx=5)

    frame_tarefa.pack(fill=tk.X, padx=5, pady=5)

    checkbuttom = ttk.Checkbutton(frame_tarefa, command=lambda
                                  label=label_tarefa: alterar_sublinhado(label))
    checkbuttom.pack(side="right", padx=5)

    canvas_interior.update_idletasks()
    canvas.configure(scrollregion= canvas.bbox("all"))

def preparar_edicao(frame_tarefa, label_tarefa):
    global frame_edicao
    frame_edicao = frame_tarefa
    input_tarefa.delete(0, tk.END)
    input_tarefa.insert(0, label_tarefa.cget("text"))

def atualizar_tarefa(nova_tarefa):
    global frame_edicao
    for widget in frame_edicao.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(text=nova_tarefa)

def deletar_tarefa(frame_tarefa):
    frame_tarefa.destroy()
    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def alterar_sublinhado(label):
    fonte_atual = label.cget("font")
    if "overstrike" in fonte_atual:
        nova_fonte = fonte_atual.replace(" overstrike", "")
    else:
        nova_fonte = fonte_atual + " overstrike"
    label.config(font=nova_fonte)

icon_editar = PhotoImage(file="editar.png").subsample(25,25)
icon_deletar = PhotoImage(file="excluir.png").subsample(25,25)

#Cabeçalho
fonte_cabecalho = font.Font(family="Garamond", size=24, weight="bold")
titulo_cabecalho = tk.Label(janela, text="To-do list", font=fonte_cabecalho,
                            bg="#F0F0F0", fg="#333").pack(pady=20)
frame = tk.Frame(janela, bg="#F0F0F0")
frame.pack(pady=10)

input_tarefa = tk.Entry(frame, font=("Garamond", 14), relief=tk.FLAT,
                        bg="white", fg="grey", width=30)
input_tarefa.pack(side=tk.LEFT, padx=10)

#botão
botao_input = tk.Button(frame, command=adicionar_tarefa, text="Adicionar tarefa", bg="#4CAF50", fg="white",
                        height=1 , width=15, font=("Roboto", 11), relief=tk.FLAT)
botao_input.pack(side=tk.LEFT, padx=10)

#criando frame para lista de tarefas com rolagem
frame_lista = tk.Frame(janela, bg="white")
frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

canvas = tk.Canvas(frame_lista, bg="white")
canvas.pack(side=tk.LEFT, fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command= canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas_interior = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=canvas_interior, anchor="nw")

canvas_interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

janela.mainloop()
