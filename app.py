from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select

from models import *

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

app.config['SECRET_KEY'] = "SECRET"



@app.route('/produto', methods=['GET'])
def produto():
    sql_produto = select(Produto)
    resultado_produto = db_session.execute(sql_produto).scalars()
    lista_produto = []
    for n in resultado_produto:
        lista_produto.append(n.serialize_produto())
        print(lista_produto[-1])
    return render_template('lista_produto.html',
                           lista_produto=lista_produto)


@app.route('/novo_produto', methods=['POST', 'GET'])
def criar_produto():
    # quando clicar no botao de salva
    if request.method == "POST":

        if (not request.form['form_nome']
                or not request.form['form_preco']
                or not request.form['form_quantidade_produto']):
            flash("Preencher todos os campos", "error")
        else:
            form_nova_produto = Produto(nome=request.form["form_nome"],
                                        PRECO=request.form['form_preco'],
                                        quantidade_produto=int(request.form['form_quantidade_produto'])
                                        )
            print(form_nova_produto)
            form_nova_produto.save()
            db_session.close()
            flash("Evento criado !!!", "success")

            # dentro do url sempre chamar função
            return redirect(url_for("produto"))
    # sempre no render chamar html
    return render_template('novo_produto.html')








if __name__ == '__main__':
    app.run(debug=True)