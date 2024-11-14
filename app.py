from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select
# import matplotlib.pyplot as plt
from models import *

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = "SECRET"


@app.route('/')
def template():
    return render_template('template.html')

@app.route('/suporte')
def suporte():
    return render_template('suporte.html')



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

@app.route('/novo_produto', methods=['POST', 'GET'])
def criar_produto():
    # quando clicar no botao de salva
    if request.method == "POST": # Enviar no banco

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
                                        categoria_name=request.form['form_categoria_id'],
                                        preco=str(request.form['form_preco'])
                                        )

            print(form_novo_produto)
            form_novo_produto.save()
            db_session.close()
            flash("Produto cadastrado com sucesso!!", "success")

            # dentro do url sempre chamar função
            return redirect(url_for("produto"))
            # sempre no render chamar html
    return render_template('novo_produto.html')


@app.route('/editar_produto/<int:id_produto>', methods=['POST','GET'])
def editar_produto(id_produto):
    #busca de acordo com o id, usando o db_session
    produto_resultado = db_session.execute(select(Produto).filter_by(id=int(id_produto))).scalar()
    print(produto_resultado)
    #verifica se existe
    if not produto_resultado:
        flash("Produto não encontrado", "error")
        return redirect(url_for('produto'))
    if request.method == 'POST':
        #valida os dados recebidos
        if not request.form.get('form_nome'):
            flash("Preencher campo", "error")
        elif not request.form.get('form_descricao'):
            flash("Preencher campo", "error")
        elif not request.form.get('form_preco'):
            flash("Preencher campo", "error")
        elif not request.form.get('form_categoria_id'):
            flash("Preencher campo categoria", "error")
        else:
            try:
                #atualiza os da0000000000000000000000000000000,



                # ,0dos
                produto_resultado.nome = request.form.get('form_nome')
                produto_resultado.descricao = request.form.get('form_descricao')
                produto_resultado.preco = request.form.get('form_preco')
                produto_resultado.categoria = request.form.get('form_categoria_id')
                #salva os dados alterados
                produto_resultado.save()
                flash("Produto atualizado com sucesso!", "sucess")
                return redirect(url_for('produto'))
            except Exception:
                flash(f"Erro {Exception}", "error")
    return render_template('editar_produto.html', produto=produto_resultado)



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


@app.route('/nova_categoria', methods=['POST', 'GET'])
def criar_categoria():
    if request.method == "POST":
        if (not request.form['form_name_categoria']):
            flash("Preencher todos os campos", "error")
        else:
            form_nova_categoria = Categoria(name_categoria=request.form
            ["form_name_categoria"])

            print(form_nova_categoria)
            form_nova_categoria.save()
            db_session.close()
            flash("Evento criado !!!", "success")

            # dentro do url sempre chamar função
            return redirect(url_for("categoria"))
            # sempre no render chamar html
    return render_template('nova_categoria.html')








# @app.route('/movimentacao', methods=['GET'])
# def movimentacao():
#     sql_movimentacao = select(Movimentacao)
#     resultado_movimentacao = db_session.execute(sql_movimentacao).scalars()
#     lista_movimentacao = []
#     for n in resultado_movimentacao:
#         lista_movimentacao.append(n.serialize_Categoria())
#         print((lista_movimentacao[-1]))
#     return render_template('categoria.html',
#                            lista_movimentacao=lista_movimentacao)





# @app.route('/nova_movimentacao',  methods=['POST', 'GET'])
# def criar_movimentacao():
#     if request.method == "POST":
#
#         if (not request.form['form_volume_movimentacao']
#                 or not request.form['form_atividade']
#                 or not request.form['form_produto_movimentado']
#         or not request.form['funcionario_movimentado']):
#             flash("Preencher todos os campos", "error")
#         else:
#             form_nova_movimentacao = Movimentacao(volume_movimentacao=int(request.form["form_volume_movimentacao"]),
#                                                 atividade=request.form["form_atividade"],
#                                                 produto_movimentado=int((request.form['form_produto_movimentado'])),
#                                                 funcionario_movimentado=int((request.form['funcionario_movimentado']))
#                                                 )
#             print(form_nova_movimentacao)
#             form_nova_movimentacao.save()
#             db_session.close()
#             flash("Evento criado !!!", "success")
#
#             # dentro do url sempre chamar função
#             return redirect(url_for("movimentacao"))
#     # sempre no render chamar html
#     return render_template('nova_movimentacao.html')


@app.route('/cadastrar_movimentacao', methods=['GET', 'POST'])
def criar_movimentacao():
    sql_produto = select(Produto)
    resultado_produto = db_session.execute(sql_produto).scalars()
    sql_funcionario = select(Funcionario)
    resultado_funcionario = db_session.execute(sql_funcionario).scalars()
    if request.method == 'POST':
        volume = int(request.form['volume_movimentacao'])
        atividade = request.form['atividade']
        produto_id = int(request.form['produto_movimentado'])
        funcionario_id = int(request.form['funcionario_movimentado'])

        movimentacao = Movimentacao(
            volume_movimentacao=volume,
            atividade=atividade,
            produto_movimentado=produto_id,
            funcionario_movimentado=funcionario_id
        )
        movimentacao.aplicar_movimentacao()  # Método que ajusta o estoque e salva a movimentação
        return redirect(url_for('movimentacao'))

    return render_template('nova_movimentacao.html',
                           produtos=resultado_produto, funcionarios=resultado_funcionario)


@app.route('/listar_movimentacoes')
def movimentacao():
    movimentacoes = Movimentacao.query.all()
    # {'': hxhgjv}

    return render_template('movimentacao.html', movimentacoes=movimentacoes)

# @app.route('/dashboard_estoque')
# def dashboard_estoque():
#     sql_produto = select(Produto)
#     resultado_produto = db_session.execute(sql_produto).scalars()
#
#     produtos = []
#     quantidades = []
#     for produto in resultado_produto:
#         produtos.append(produto.nome)
#         quantidades.append(produto.quantidade_produto)
#
#     return render_template('dashboard.html', produtos=produtos, quantidades=quantidades)

if __name__ == '__main__':
    app.run(debug=True)
