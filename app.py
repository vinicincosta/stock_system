from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.testing.pickleable import User

# import matplotlib.pyplot as plt
from models import *

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
import hashlib

app = Flask(__name__)
ln = LoginManager(app)
ln.login_view = 'login'
app.config['SECRET_KEY'] = "SECRET"
# estrtura login
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()


@ln.user_loader
def user_loader(id):
    usario = db_session.query(Usuario).filter_by(id=id).first()
    return usario


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']

        user = db_session.query(Usuario).filter_by(nome=nome, senha=hash(senha)).first()
        if not user:
            return 'Nome ou senha incorretos'

        login_user(user)
        return redirect(url_for('template'))

    else:
        flash(message=" Verifique se os dados estão inseridos corretamente")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registrar.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']

        novo_usuario = Usuario(nome=nome, senha=hash(senha))
        db_session.add(novo_usuario)
        db_session.commit()

        login_user(novo_usuario)

        return redirect(url_for('template'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# redirecionar login
@app.route('/')
def template():
    return render_template('login.html')


@app.route('/suporte')
def suporte():
    return render_template('suporte.html')


@app.route('/estoque')
def estoque():
    return render_template('estoque.html')


@app.route('/produto', methods=['GET'])
def produto():
    sql_produto = select(Produto, Categoria).join(Categoria, Categoria.id == Produto.categoria_id)
    resultado_produto = db_session.execute(sql_produto).fetchall()  # quando é join fetchall invez de de scalars

    return render_template('produto.html',
                           lista_produto=resultado_produto)


@app.route('/listar_movimentacoes')
def movimentacao():
    sql_mov = (select(Movimentacao, Produto, Funcionario).join(Produto, Movimentacao.produto_movimentado == Produto.id)
               .join(Funcionario, Movimentacao.funcionario_movimentado == Funcionario.id))
    resultado_mov = db_session.execute(sql_mov).fetchall()
    print(resultado_mov)

    return render_template('movimentacao.html', movimentacoes=resultado_mov)


@app.route('/novo_produto', methods=['POST', 'GET'])
def criar_produto():
    sql_categoria = select(Categoria)
    resultado_categoria = db_session.execute(sql_categoria).scalars()
    # quando clicar no botao de salva
    if request.method == "POST":  # Enviar no banco

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

    return render_template('novo_produto.html',
                           categorias=resultado_categoria)


@app.route('/editar_produto/<int:id_produto>', methods=['POST', 'GET'])
def editar_produto(id_produto):
    sql_categoria = select(Categoria)
    resultado_categoria = db_session.execute(sql_categoria).scalars()
    # busca de acordo com o id, usando o db_session
    produto_resultado = db_session.execute(select(Produto).filter_by(id=int(id_produto))).scalar()
    sql_categoria_atual = db_session.execute(select(Categoria).filter_by(id=produto_resultado.categoria_id)).scalar()
    print(produto_resultado)

    # verifica se existe
    if not produto_resultado:
        flash("Produto não encontrado", "error")
        return redirect(url_for('produto'))
    if request.method == 'POST':
        # valida os dados recebidos
        if not request.form.get('form_nome'):
            flash("Preencher campo", "error")
        elif not request.form.get('form_descricao'):
            flash("Preencher campo", "error")
        elif not request.form.get('form_preco'):
            flash("Preencher campo", "error")
        elif not request.form.get('form_categoria_id'):
            flash("Preencher campo", "error")
        else:
            try:
                # o ponto (.) busca a informação
                # atualiza os dados
                produto_resultado.nome = request.form.get('form_nome')
                produto_resultado.descricao = request.form.get('form_descricao')
                produto_resultado.preco = request.form.get('form_preco')
                produto_resultado.categoria_id = request.form.get('form_categoria_id')
                # salva os dados alterados
                produto_resultado.save()
                flash("Produto atualizado com sucesso!", "sucess")
                return redirect(url_for('produto'))
            except Exception:
                flash(f"Erro {Exception}", "error")
    return render_template('editar_produto.html', produto=produto_resultado, categorias=resultado_categoria,
                           categoria_atual=sql_categoria_atual)


@app.route('/editar_funcionario/<int:id_funcionario>', methods=['POST', 'GET'])
def editar_funcionario(id_funcionario):
    # busca de acordo com o id, usando o db_session
    funcionario_resultado = db_session.execute(select(Funcionario).filter_by(id=int(id_funcionario))).scalar()
    print(funcionario_resultado)
    # verifica se existe
    if not funcionario_resultado:
        flash("Funcionario não encontrado", "error")
        return redirect(url_for('funcionario'))
    if request.method == 'POST':
        # valida os dados recebidos
        if not request.form.get('form_nome'):
            flash("Preencher campo", "error")
        elif not request.form.get('form_salario'):
            flash("Preencher campo", "error")

        else:
            try:
                # atualiza os dados
                funcionario_resultado.nome = request.form.get('form_nome')
                funcionario_resultado.salario = request.form.get('form_salario')

                # salva os dados alterados
                funcionario_resultado.save()
                flash("funcionário atualizado com sucesso!", "sucess")
                return redirect(url_for('funcionario'))
            except Exception:
                flash(f"Erro {Exception}", "error")
    return render_template('editar_funcionario.html', funcionario=funcionario_resultado)


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
            flash("Categoria criada!!!", "success")

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
    resultado_produtos = db_session.execute(sql_produto).scalars()

    sql_funcionario = select(Funcionario)
    resultado_funcionarios = db_session.execute(sql_funcionario).scalars()

    if request.method == 'POST':
        volume = int(request.form['volume_movimentacao'])
        atividade = request.form['atividade']
        produto_id = int(request.form['produto_movimentado'])
        funcionario_id = int(request.form['funcionario_movimentado'])

        # select para buscar o produto do id encima
        resultado_produto = db_session.execute(select(Produto).filter_by(id=int(produto_id))).scalar()

        if not resultado_produto:
            return "Produto não encontrado"

        movimentacao = Movimentacao(
            volume_movimentacao=volume,
            atividade=atividade,
            produto_movimentado=produto_id,
            funcionario_movimentado=funcionario_id
        )
        if atividade == 'saida':
            # Checar se há quantidade suficiente no estoque
            if resultado_produto.verificar_volume(volume_movimentacao=volume):
                # Atualizar estoque para saída
                resultado_produto.quantidade_produto -= volume
                movimentacao.save()
                resultado_produto.save()
                return redirect(url_for('movimentacao'))
            else:
                flash(f"Estoque insuficiente. Disponível: {resultado_produto.quantidade_produto} unidades.", "error")

        elif atividade == "entrada":
            # Atualizar estoque para entrada
            resultado_produto.quantidade_produto += volume
            movimentacao.save()
            resultado_produto.save()
            return redirect(url_for('movimentacao'))
        else:
            flash("Atividade inválida. Escolha 'entrada' ou 'saida'.", 'error')
    return render_template('nova_movimentacao.html', produtos=resultado_produtos, funcionarios=resultado_funcionarios)


@app.route('/editar_movimentacao/<int:id_movimentacao>', methods=['POST', 'GET'])
def editar_movimentacao(id_movimentacao):
    # busca de acordo com o id, usando o db_session
    print(id_movimentacao)
    teste = select(Movimentacao)
    movimentacao_resultado = db_session.execute(
        select(Movimentacao).filter_by(id=id_movimentacao)).scalar()
    print('xxxxxxxxxx', movimentacao_resultado)
    # verifica se existe
    if not movimentacao_resultado:
        flash("Movimentação não encontrada", "error")
        return redirect(url_for('movimentacao'))
    if request.method == 'POST':
        # valida os dados recebidos
        if not request.form.get('form_volume_movimentacao'):
            flash("Preencher campo", "error")
        elif not request.form.get('form_atividade'):
            flash("Preencher campo", "error")
        elif not request.form.get('form_produto_movimentado'):
            flash("Preencher campo", "error")
        elif not request.form.get('form_funcionario_movimentado'):
            flash("Preencher campo", "error")
        else:
            try:
                # atualiza os dados
                movimentacao_resultado.volume_movimentacao = request.form.get('form_volume_movimentacao')
                movimentacao_resultado.atividade = request.form.get('form_atividade')
                movimentacao_resultado.produto_movimentado = request.form.get('form_produto_movimentado')
                movimentacao_resultado.funcionario_movimentado = request.form.get('form_funcionario_movimentado')
                # salva os dados alterados
                movimentacao_resultado.save()
                flash("Movimentação atualizada com sucesso!", "sucess")
                return redirect(url_for('movimentacao'))
            except Exception:
                flash(f"Erro {Exception}", "error")
    return render_template('editar_movimentacao.html', movimentacao=movimentacao_resultado)


@app.route('/editar_categoria/<int:id_categoria>', methods=['POST', 'GET'])
def editar_categoria(id_categoria):
    # busca de acordo com o id, usando o db_session
    categoria_resultado = db_session.execute(select(Categoria).filter_by(id=int(id_categoria))).scalar()
    print(categoria_resultado)
    # verifica se existe
    if not categoria_resultado:
        flash("Categoria não encontrado", "error")
        return redirect(url_for('categoria'))
    if request.method == 'POST':
        # valida os dados recebidos
        if not request.form.get('form_name_categoria'):
            flash("Preencher campo", "error")

        else:
            try:
                # atualiza os dados
                categoria_resultado.name_categoria = request.form.get('form_name_categoria')

                # salva os dados alterados
                categoria_resultado.save()
                flash("Categoria atualizado com sucesso!", "sucess")
                return redirect(url_for('categoria'))
            except Exception:
                flash(f"Erro {Exception}", "error")
    return render_template('editar_categoria.html', categoria=categoria_resultado)


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

# @app.route('/cadastrar_movimentacao', methods=['GET', 'POST'])
# def criar_movimentacao():
#     sql_produto = select(Produto)
#     resultado_produto = db_session.execute(sql_produto).scalars()
#     sql_funcionario = select(Funcionario)
#     resultado_funcionario = db_session.execute(sql_funcionario).scalars()
#     if request.method == 'POST':
#         volume = int(request.form['volume_movimentacao'])
#         atividade = request.form['atividade']
#         produto_id = int(request.form['produto_movimentado'])
#         funcionario_id = int(request.form['funcionario_movimentado'])
#
#         movimentacao = Movimentacao(
#             volume_movimentacao=volume,
#             atividade=atividade,
#             produto_movimentado=produto_id,
#             funcionario_movimentado=funcionario_id
#         )
#         movimentacao.aplicar_movimentacao()  # Método que ajusta o estoque e salva a movimentação
#         return redirect(url_for('movimentacao'))
#
#     return render_template('nova_movimentacao.html',
#                            produtos=resultado_produto, funcionarios=resultado_funcionario)

@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
