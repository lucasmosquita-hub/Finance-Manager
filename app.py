from flask import Flask, render_template, request, redirect
from database import conectar, criar_tabela

app = Flask(__name__)

criar_tabela()


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        descricao = request.form["descricao"]
        valor = float(request.form["valor"])
        tipo = request.form["tipo"]

        conexao = conectar()

        conexao.execute(
            """
            INSERT INTO movimentacoes (descricao, valor, tipo)
            VALUES (?, ?, ?)
            """,
            (descricao, valor, tipo)
        )

        conexao.commit()
        conexao.close()

        return redirect("/")

    conexao = conectar()

    movimentacoes = conexao.execute(
        "SELECT * FROM movimentacoes ORDER BY id DESC"
    ).fetchall()

    conexao.close()

    receitas = sum(
        m["valor"] for m in movimentacoes
        if m["tipo"] == "receita"
    )

    despesas = sum(
        m["valor"] for m in movimentacoes
        if m["tipo"] == "despesa"
    )

    saldo = receitas - despesas

    return render_template(
        "index.html",
        receitas=receitas,
        despesas=despesas,
        saldo=saldo,
        movimentacoes=movimentacoes
    )


if __name__ == "__main__":
    app.run(debug=True)