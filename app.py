from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select

from models import *

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

app.config['SECRET_KEY'] = "SECRET"


@app.route('/')
def template():
    return render_template('template.html')



@app.route('/lista_produto', methods=['GET'])
def produto():
    sql_produto = select(Produto)
    resultado_produto = db_session.execute(sql_produto).scalars()
    lista_produto = []
    for n in resultado_produto:
        lista_produto.append(n.serialize_produto())
        print(lista_produto[-1])
    return render_template('lista_produto.html',
                           lista_produto=lista_produto)

@app.route('/funcionario', methods=['GET'])
def funcionario():
    sql_funcionario = select(Funcionario)
    resultado_funcionario = db_session.execute(sql_funcionario).scalars()
    lista_funcionario = []
    for n in resultado_funcionario:
        lista_funcionario.append(n.serialize_funcionario())
        print(lista_funcionario[-1])
    return render_template('lista_funcinario.html',
                           lista_funcionario=lista_funcionario)


@app.route('/lista_categoria', methods=['GET'])
def categoria():
    sql_categoria = select(Categoria)
    resultado_categoria = db_session.execute(sql_categoria).scalars()
    lista_categoria = []
    for n in resultado_categoria:
        lista_categoria.append(n.serialize_Categoria())
        print((lista_categoria[-1]))
    return render_template('lista_categoria.html',
                           lista_categoria=lista_categoria)


@app.route('/novo_produto', methods=['POST', 'GET'])
def criar_produto():
    # quando clicar no botao de salva
    if request.method == "POST":

        if (not request.form['form_nome']
                or not request.form['form_descricao']
                or not request.form['form_quantidade_produto']
                or not request.form['form_categoria_id']):
            flash("Preencher todos os campos", "error")
        else:
            form_novo_produto = Produto(nome=request.form["form_nome"],
                                        descricao=request.form['form_descricao'],
                                        quantidade_produto=int(request.form['form_quantidade_produto']),
                                        categoria_id=int(request.form['form_categoria_id'])
                                        )

            print(form_novo_produto)
            form_novo_produto.save()
            db_session.close()
            flash("Evento criado !!!", "success")

            # dentro do url sempre chamar função
            return redirect(url_for("lista_produto.html"))
    # sempre no render chamar html
    return render_template('novo_produto.html')


@app.route('/nova_categoria', methods=['POST', 'GET'])
def criar_categoria():
    if request.method == "POST":
        if (not request.form['form_nome_classificacao']):
            flash("Preencher todos os campos", "error")
        else:
            form_nova_categoria = Categoria(nome_classificacao=request.form
            ["form_nome_classificacao"])

            print(form_nova_categoria)
            form_nova_categoria.save()
            db_session.close()
            flash("Evento criado !!!", "success")

            # dentro do url sempre chamar função
            return redirect(url_for("categoria"))
            # sempre no render chamar html
    return render_template('nova_categoria.html')


@app.route('/novo_funcinario', methods=['POST', 'GET'])
def criar_funcionario():
    # quando clicar no botao de salva
    if request.method == "POST":

        if (not request.form['form_nome_funcionario']
                or not request.form['form_cpf']
                or not request.form['form_salario']):
            flash("Preencher todos os campos", "error")
        else:
            form_novo_funcionario = Funcionario(nome=request.form["form_nome_funcionario"],
                                                cpf=request.form["form_cpf"],
                                                salario=float(request.form['form_salario']),

                                                )
            print(form_novo_funcionario)
            form_novo_funcionario.save()
            db_session.close()
            flash("Evento criado !!!", "success")

            # dentro do url sempre chamar função
            return redirect(url_for("funcionario"))
    # sempre no render chamar html
    return render_template('novo_funcionario.html')

# ---------------------------------------------------------------------------
@app.route('/atualizar_produto/<int:produto_id>', methods=['POST', 'GET'])
def atualizar_produto(produto_id):
    produto = db_session.query(Produto).get(produto_id)

    if request.method == "POST":
        if (not request.form['form_nome']
                or not request.form['form_descricao']
                or not request.form['form_quantidade_produto']
                or not request.form['form_categoria_id']):
            flash("Preencher todos os campos", "error")
        else:
            produto.nome = request.form["form_nome"]
            produto.descricao = request.form['form_descricao']
            produto.quantidade_produto = int(request.form['form_quantidade_produto'])
            produto.categoria_id = int(request.form['form_categoria_id'])

            db_session.commit()
            flash("Produto atualizado com sucesso!", "success")
            return redirect(url_for("lista_produto"))

    return render_template('atualizar_produto.html', produto=produto)


@app.route('/atualizar_funcionario/<int:funcionario_id>', methods=['POST', 'GET'])
def atualizar_funcionario(funcionario_id):
    funcionario = db_session.query(Funcionario).get(funcionario_id)

    if request.method == "POST":
        if (not request.form['form_nome_funcionario']
                or not request.form['form_cpf']
                or not request.form['form_salario']):
            flash("Preencher todos os campos", "error")
        else:
            funcionario.nome = request.form["form_nome_funcionario"]
            funcionario.cpf = request.form["form_cpf"]
            funcionario.salario = float(request.form['form_salario'])

            db_session.commit()
            flash("Funcionário atualizado com sucesso!", "success")
            return redirect(url_for("funcionario"))

    return render_template('atualizar_funcionario.html', funcionario=funcionario)


@app.route('/atualizar_categoria/<int:categoria_id>', methods=['POST', 'GET'])
def atualizar_categoria(categoria_id):
    categoria = db_session.query(Categoria).get(categoria_id)

    if request.method == "POST":
        if not request.form['form_nome_classificacao']:
            flash("Preencher todos os campos", "error")
        else:
            categoria.nome_classificacao = request.form["form_nome_classificacao"]

            db_session.commit()
            flash("Categoria atualizada com sucesso!", "success")
            return redirect(url_for("categoria"))

    return render_template('atualizar_categoria.html', categoria=categoria)










if __name__ == '__main__':
    app.run(debug=True)
