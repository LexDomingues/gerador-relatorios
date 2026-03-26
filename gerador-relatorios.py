from flask import Flask, render_template, request
import csv
from pathlib import Path

app = Flask(__name__)

ROOT_PATH = Path(__file__).parent
arquivo_produtos = ROOT_PATH / "produtos.csv"
arquivo_vendas = ROOT_PATH / "vendas.csv"


# Página principal
@app.route("/")
def index():
    produtos = []

    with open(arquivo_produtos, newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            produtos.append(linha)

    return render_template("index.html", produtos=produtos)


# Registrar venda
from flask import redirect, url_for

@app.route("/venda", methods=["POST"])
def venda():
    with open(arquivo_produtos, newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        produtos = list(leitor)

    with open(arquivo_vendas, "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)

        for produto in produtos:
            codigo = produto["codigo"]
            quantidade = request.form.get(f"qtd_{codigo}")

            if quantidade and int(quantidade) > 0:
                escritor.writerow([
                    produto["nome"],
                    quantidade,
                    produto["preco"]
                ])

    return redirect(url_for("index"))


app.run(debug=True)