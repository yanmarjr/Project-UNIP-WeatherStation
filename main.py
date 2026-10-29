from tkinter import *
from tkmacosx import Button
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dados_processados import (dados, porcentagem_de_chuva, porcentagem_de_luz,
                               pressao_average, pressao_somente_valor)
import os
from PIL import Image, ImageTk


FONT = "Courier"

janela = Tk()
janela.title("Dados de Estação Meteorológica")
janela.geometry("1000x700")
# make page fill the space under the buttons
janela.columnconfigure(0, weight=1)
janela.rowconfigure(1, weight=1)
# focus window
janela.focus_force()


# Convert the "Data" column to real datetimes so matplotlib can plot a time axis
datas = pd.to_datetime(dados["Data"], format="%d/%m/%Y, %H:%M:%S")


# ---------- Charts (gráficos) ----------
def grafico_pizza(porcentagem, rotulo_sim, rotulo_nao, cor_sim):
    """Pie chart (gráfico de pizza) with the % of intervals for yes/no."""
    fig = Figure(figsize=(5, 3.5), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(
        [porcentagem, 100 - porcentagem],
        labels=[rotulo_sim, rotulo_nao],
        colors=[cor_sim, "#cccccc"],
        autopct="%1.1f%%",
        startangle=90,
    )
    ax.axis("equal")
    fig.tight_layout()
    return fig


def grafico_pressao():
    """Line chart (gráfico de linhas) of pressure over time + average line."""
    fig = Figure(figsize=(8, 3.5), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(datas, pressao_somente_valor, color="tab:purple", linewidth=0.8, label="Pressão")
    ax.axhline(pressao_average, color="red", linestyle="--",
               label=f"Média: {pressao_average:.2f} hPa")
    ax.set_xlabel("Data")
    ax.set_ylabel("Pressão (hPa)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def make_page(titulo, descricao, valor, figura):
    """Monta uma página com título, descrição, grande valor e um gráfico"""
    page = Frame(janela)
    page.grid(row=1, column=0, columnspan=4, sticky="nsew")
    Label(page, text=titulo, font=(FONT, 20)).pack()
    Label(page, text=descricao, font=(FONT, 16)).pack()
    Label(page, text=valor, font=(FONT, 32)).pack(pady=10)

    # embed the matplotlib figure in the tkinter page
    canvas = FigureCanvasTkAgg(figura, master=page)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    return page


# Folder where main.py lives, so the image is found no matter where you run the script from
PASTA = os.path.dirname(os.path.abspath(__file__))

# home
home = Frame(janela)
home.grid(row=1, column=0, columnspan=4, sticky="nsew")
Label(home, text="Estação Meteorológica", font=(FONT, 24)).pack(pady=40)
Label(home, text="Use os botões acima para ver os dados.", font=(FONT, 16)).pack()
imagen = Image.open(os.path.join(PASTA,"estacao.jpg"))
imagen.thumbnail((500,450))
foto = ImageTk.PhotoImage(imagen)
label_imagem = Label(home, image=foto)
label_imagem.pack(pady=10)


# make pages:
page_chuva = make_page(
    "Chuva", "Intervalos com chuva:", f"{porcentagem_de_chuva:.2f} %",
    grafico_pizza(porcentagem_de_chuva, "Com chuva", "Sem chuva", "tab:blue"),
)
page_luz = make_page(
    "Luz", "Intervalos com luz:", f"{porcentagem_de_luz:.2f} %",
    grafico_pizza(porcentagem_de_luz, "Com luz", "Sem luz", "gold"),
)
page_pressao = make_page(
    "Pressão", "Pressão média:", f"{pressao_average:.2f} hPa",
    grafico_pressao(),
)


# navigation bar (row 0)
nav = Frame(janela)
nav.grid(row=0, column=0, padx=10, pady=10)
Button(nav, text="Home", command=home.tkraise).pack(side="left", padx=5)
Button(nav, text="Chuva", command=page_chuva.tkraise).pack(side="left", padx=5)
Button(nav, text="Luz", command=page_luz.tkraise).pack(side="left", padx=5)
Button(nav, text="Pressão", command=page_pressao.tkraise).pack(side="left", padx=5)


home.tkraise()  # start on the home page


janela.mainloop()
