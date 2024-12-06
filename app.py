from sqlite3 import IntegrityError
from sqlalchemy import select, func, desc
from sqlalchemy.testing.pickleable import User
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
from models import *
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
import hashlib
from argon2 import PasswordHasher
from functools import wraps


app = Flask(__name__)
ln = LoginManager(app)
ln.login_view = 'login'
app.config['SECRET_KEY'] = "SECRET"
# estrtura login
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


@app.route('/home')
def home():
    sql_salario = select(Funcionario)
    resultado_funcionario = db_session.execute(sql_salario).scalars()
    lista_funcionario = []
    for n in resultado_funcionario:
        lista_funcionario.append(n.serialize_funcionario())
        print(lista_funcionario[-1])

    sql_categoria = select(Categoria)
    resultado_categoria = db_session.execute(sql_categoria).scalars()
    lista_categoria = []
    for n in resultado_categoria:
        lista_categoria.append(n.serialize_Categoria())
        print(lista_categoria[-1])
    return render_template('home.html',
                           lista_funcionario=lista_funcionario, lista_categoria=lista_categoria
                           )


@ln.user_loader
def user_loader(id):
    usuario = db_session.query(Usuario).filter_by(id=id).first()
    return usuario


ln.login_view = 'login'


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.admin:  # Verifica se o usuÃ¡rio NÃƒO Ã© admin
            flash('Acesso negado, necessita ser admin', 'error')
            return redirect(url_for('dashboard'))  # Redireciona para uma pÃ¡gina apropriada
        return f(*args, **kwargs)  # Executa a funÃ§Ã£o original

    return decorated_function


def usuario_ativo(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.status:
            flash('Acesso negado, Usuario desativado', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def redirecionar():
    return redirect(url_for('login'))


#   U          S           U           A            R              I             O          S         login
# cadastro de usuarios

def verificar_email_cnpj(email, cnpj, telefone):
    usuario = db_session.query(Usuario).filter_by(email=email).first()
    if usuario:
        return True
    usuario = db_session.query(Usuario).filter_by(CNPJ=cnpj).first()
    if usuario:
        return True
    usuario = db_session.query(Usuario).filter_by(telefone=telefone).first()
    if usuario:
        return True
    return False


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        telefone = request.form['telefone']
        CNPJ = request.form['CNPJ']

        if verificar_email_cnpj(email, CNPJ, telefone):
            flash('Email ou CNPJ ja existente', 'error')
            return redirect(url_for('login'), )
        else:
            try:
                if not nome or not email or not senha:
                    flash('preecher todos os campos', 'error')
                else:
                    usuario = Usuario(nome=nome, email=email, senha=senha,
                                      telefone=telefone, CNPJ=CNPJ, admin=False, status=False)
                    db_session.add(usuario)
                    db_session.commit()
                    flash('Usuario cadastrado com sucesso', 'error')
                    return redirect(url_for('login'))
            except IntegrityError:

                flash('erro')

    return render_template("registrar.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if not email:
            flash('preecher todos os campos', 'error')
        elif not senha:
            flash('preecher todos os campos', 'error')
        else:
            usuario = db_session.query(Usuario).filter_by(email=email).first()

            if usuario:
                if not usuario.status:
                    flash('')
                    redirect(url_for('login'))
                print(senha)
                if usuario.admin and usuario.verificar_senha(senha):
                    flash('Olá admin, login realizado com sucesso!', 'success')
                    login_user(usuario)

                    return redirect(url_for('dashboard'))
                else:
                    flash('login deu errado, certifique-se de que os dados estão coreretos', 'error')
            else:
                flash('usuario não encontrado', 'error')
    db_session.close()
    return render_template("login.html")


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@app.route('/logout', methods=['GET', 'POST'])
@login_required
@usuario_ativo
def logout():
    logout_user()
    return redirect(url_for('dashboard'))

# redirecionar login
# @app.route('/')
# def template():
#     return render_template('template.html')


@app.route('/suporte')
def suporte():
    return render_template('suporte.html')


@app.route('/estoque')
def estoque():
    return render_template('estoque.html')


@app.route('/produto', methods=['GET'])
def produto():
    sql_produto = select(Produto, Categoria).join(Categoria, Categoria.id == Produto.categoria_id)
    resultado_produto = db_session.execute(sql_produto).fetchall()  # quando Ã© join fetchall invez de de scalars

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
                or not request.form['form_categoria_id']
                or not request.form['form_preco']):
            flash("Preencher todos os campos", "error")
        else:
            form_novo_produto = Produto(nome=request.form["form_nome"],
                                        descricao=request.form['form_descricao'],
                                        quantidade_produto=0,
                                        categoria_id=request.form['form_categoria_id'],
                                        preco=float(request.form['form_preco'])
                                        )

            print(form_novo_produto)
            form_novo_produto.save()
            db_session.close()
            flash("Produto cadastrado com sucesso!!", "success")

            # dentro do url sempre chamar funÃ§Ã£o
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
        flash("Produto nÃ£o encontrado", "error")
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
                # o ponto (.) busca a informaÃ§Ã£o
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
        flash("Funcionario nÃ£o encontrado", "error")
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
                flash("funcionÃ¡rio atualizado com sucesso!", "sucess")
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


@app.route('/novo_funcionario', methods=['POST', 'GET'])
def criar_funcionario():
    if request.method == "POST":
        nome = request.form.get('form_nome', '').strip()
        cpf = request.form.get('form_cpf', '').strip()
        salario = request.form.get('form_salario', '').strip()

        # Verifica se todos os campos estão preenchidos
        if not nome or not cpf or not salario:
            flash("Preencher todos os campos", "error")
        # Verifica se o CPF tem exatamente 11 caracteres
        elif len(cpf) != 11 or not cpf.isdigit():
            flash("O CPF deve conter exatamente 11 números.", "error")
        else:
            try:
                form_novo_funcionario = Funcionario(
                    nome=nome,
                    cpf=cpf,
                    salario=float(salario),
                )
                form_novo_funcionario.save()
                db_session.close()
                flash("Funcionário criado com sucesso!", "success")
                return redirect(url_for("funcionario"))
            except Exception as e:
                flash(f"Erro ao salvar funcionário: {e}", "error")

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

            # dentro do url sempre chamar funÃ§Ã£o
            return redirect(url_for("categoria"))
            # sempre no render chamar html
    return render_template('nova_categoria.html')


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
            return "Produto nÃ£o encontrado"

        movimentacao = Movimentacao(
            volume_movimentacao=volume,
            atividade=atividade,
            produto_movimentado=produto_id,
            funcionario_movimentado=funcionario_id
        )
        if atividade == 'saida':
            # Checar se hÃ¡ quantidade suficiente no estoque
            if resultado_produto.verificar_volume(volume_movimentacao=volume):
                # Atualizar estoque para saÃ­da
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
        flash("MovimentaÃ§Ã£o nÃ£o encontrada", "error")
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
                flash("MovimentaÃ§Ã£o atualizada com sucesso!", "sucess")
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
        flash("Categoria nÃ£o encontrado", "error")
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


@app.route('/dashboard')
def dashboard():
    # Buscar os 3 funcionÃ¡rios com os maiores salÃ¡rios no departamento "estoque"
    funcionarios_estoque = (
        Funcionario.query
        .order_by(Funcionario.salario.desc())
        .limit(3)
        .all()
    )
    produtos_movimentados = produtos_mais_movimentados()

    return render_template("dashboard.html", lista_funcionario=funcionarios_estoque,
                           produtos_movimentados=produtos_movimentados)


def produtos_mais_movimentados():
    # Consulta para contar as movimentaÃ§Ãµes por produto
    produtos_movimentados = (
        db_session.query(
            Produto.nome,
            func.sum(Movimentacao.volume_movimentacao).label('total_movimentacoes')
        )
        .join(Movimentacao, Produto.id == Movimentacao.produto_movimentado)
        .where(Movimentacao.atividade == 'saida')
        .group_by(Movimentacao.produto_movimentado)
        .order_by(desc('total_movimentacoes'))
        .limit(3)
        .all()
    )

    # Verificando se os dados estÃ£o sendo retornados
    print(produtos_movimentados)

    # Renderizar os resultados no dashboard
    return produtos_movimentados


@app.route('/dashboard_gf', methods=['GET', 'POST'])
def dashboard_func():
    resultados = (
        db_session.query(
            Funcionario.id.label("funcionario_id"),
            Funcionario.nome.label('funcionario_nome'),
            func.count(Movimentacao.id).label('total_movimentacoes')
        )
        .join(Movimentacao, Funcionario.id == Movimentacao.funcionario_movimentado)
        .group_by(Funcionario.id, Funcionario.nome)
        .order_by(desc('total_movimentacoes'))
        .limit(6)
        .all()
    )
    print(resultados)
    labels = []
    dados = []
    for id_, nome, num in resultados:
        print(id_, nome, num)
        labels.append(nome)
        dados.append(num)
    data = {
        'Funcionários': labels,
        'Nº de movimentações': dados
    }
    print(data)
    # criando grÃ¡fico com plotly express

    fig = px.histogram(data, x='Funcionários', y='Nº de movimentações', color='Funcionários', template='plotly_dark')
    # convertendo grafico em html
    fig.layout.update().legend.visible = False
    fig.layout.update(
        {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
         'paper_bgcolor': 'rgba(0, 0, 0, 0)' }
    )
    graph_html = pio.to_html(fig, full_html=False)
    return render_template('dashboard_gf.html', home_=False, graph_html=graph_html)


if __name__ == '__main__':
    app.run(debug=True)
