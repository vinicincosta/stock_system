from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select

from models import *

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

app.config['SECRET_KEY'] = "SECRET"


@app.route('/')
def template():
    return render_template('template.html')



@app.route('/produto', methods=['GET'])
def produto():
    sql_produto = select(Produto)
    resultado_produto = db_session.execute(sql_produto).scalars()
    lista_produto = []
    for n in resultado_produto:
        lista_produto.append(n.serialize_produto())
        print(lista_produto[-1])
    return render_template('produto.html',
                           lista_produto=lista_produto)

@app.route('/funcionario', methods=['GET'])
def funcionario():
    sql_funcionario = select(Funcionario)
    resultado_funcionario = db_session.execute(sql_funcionario).scalars()
    lista_funcionario = []
    for n in resultado_funcionario:
        lista_funcionario.append(n.serialize_funcionario())
        print(lista_funcionario[-1])
    return render_template('funcionario.html',
                           lista_funcionario=lista_funcionario)
@app.route('/movimentacao', methods=['GET'])
def movimentacao():
    sql_movimentacao = select(Movimentacao)
    resultado_movimentacao = db_session.execute(sql_movimentacao).scalars()
    lista_movimentacao = []
    for n in resultado_movimentacao:
        lista_movimentacao.append(n.serialize_Categoria())
        print((lista_movimentacao[-1]))
    return render_template('categoria.html',
                           lista_movimentacao=lista_movimentacao)

@app.route('/categoria', methods=['GET'])
def categoria():
    sql_categoria = select(Categoria)
    resultado_categoria = db_session.execute(sql_categoria).scalars()
    lista_categoria = []
    for n in resultado_categoria:
        lista_categoria.append(n.serialize_Categoria())
        print((lista_categoria[-1]))
    return render_template('categoria.html',
                           lista_categoria=lista_categoria)


@app.route('/novo_produto', methods=['POST', 'GET'])
def criar_produto():
    # quando clicar no botao de salva
    if request.method == "POST":

        if (not request.form['form_nome']
                or not request.form['form_descricao']
                or not request.form['form_quantidade_produto']
                or not request.form['form_categoria_id']
                or not request.form['form_preco']):
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
        if (not request.form['form_nome_classificação']):
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

        if (not request.form['form_nome']
                or not request.form['form_cpf']
                or not request.form['form_salario']):
            flash("Preencher todos os campos", "error")
        else:
            form_novo_funcionario = Funcionario(nome=request.form["form_nome"],
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

@app.route('/nova_movimentacao',  methods=['POST', 'GET'])
def criar_movimentacao():
    if request.method == "POST":

        if (not request.form['form_volume_movimentacao']
                or not request.form['form_atividade']
                or not request.form['form_produto_movimentado']
        or not request.form['funcionario_movimentado']):
            flash("Preencher todos os campos", "error")
        else:
            form_nova_movimentacao = Movimentacao(volume_movimentacao=int(request.form["form_volume_movimentacao"]),
                                                atividade=request.form["form_atividade"],
                                                produto_movimentado=int((request.form['form_produto_movimentado'])),
                                                funcionario_movimentado=int((request.form['funcionario_movimentado']))
                                                )
            print(form_nova_movimentacao)
            form_nova_movimentacao.save()
            db_session.close()
            flash("Evento criado !!!", "success")

            # dentro do url sempre chamar função
            return redirect(url_for("movimentacao"))
    # sempre no render chamar html
    return render_template('nova_movimentacao.html')



if __name__ == '__main__':
    app.run(debug=True)
