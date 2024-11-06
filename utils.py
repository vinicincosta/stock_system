from models import Produto, Categoria, Movimentacao, Funcionario, Movimentacao_Produto, db_session
from sqlalchemy import select


# inserir dados na tabela
def inserir_produto():
    produto = Produto(nome=str(input('Nome:')),
                      descricao=str(input('descricao:')),
                      quantidade_produto=int(input('quantidade_produto:')),
                      codigo_barras=str(input('codigo_barras:')),
                      categoria_id=int(input('categoria_id:'))
                      )

    print(produto)
    produto.save()


def consultar_produto():
    var_produto = select(Produto)
    var_produto = db_session.execute(var_produto).all()
    print(var_produto)


def atualizar_produto():
    # Seleciona o item a ser alterado
    var_produto = select(Produto).where(str(input('Nome: ')) == Produto.nome)
    var_produto = db_session.execute(var_produto).scalar()
    # Nova informação
    var_produto.nome = str(input('Novo Nome:'))
    var_produto.save()


# remove pessoas
def deletar_produto():
    produto_delete = input('Quem você deseja deletar?:')
    var_produto = select(Produto).where(produto_delete == Produto.nome)
    var_produto = db_session.execute(var_produto).scalar()
    var_produto.delete()


def inserir_movimentacao():
    movimentacao = Movimentacao(
        volume_movimentacao=int(input('Quantidade:')),
        atividade=str(input('Atividade:')),
        produto_movimentado=int(input('Produto:'))
    )

    print(movimentacao)
    movimentacao.save()


def consultar_movimentacao():
    var_movimentacao = select(Movimentacao)
    var_movimentacao = db_session.execute(var_movimentacao).all()
    print(var_movimentacao)


def atualizar_movimentacao():
    # Seleciona o item a ser alterado
    var_movimentacao = select(Movimentacao).where(str(input('Atividade: ')) == Movimentacao.nome)
    var_movimentacao = db_session.execute(var_movimentacao).scalar()
    # Nova informação
    var_movimentacao.nome = str(input('Nova Atividade:'))
    var_movimentacao.save()


# remove movimentações
def deletar_movimentacao():
    movimentacao_delete = input('Qual movimentação você deseja deletar?:')
    var_movimentacao = select(Movimentacao).where(movimentacao_delete == Movimentacao.nome)
    var_movimentacao = db_session.execute(var_movimentacao).scalar()
    var_movimentacao.delete()


# inserir dados na tabela
def inserir_categoria():
    categoria = Categoria(nome_classificacao=str(input('nome_classificação'))
                          )
    print(categoria)
    categoria.save()


def consultar_categoria():
    var_categoria = select(Categoria)
    var_categoria = db_session.execute(var_categoria).all()
    print(var_categoria)


def atualizar_categoria():
    # Seleciona o item a ser alterado
    var_categoria = select(Categoria).where(str(input('Nome: ')) == Categoria.nome)
    var_categoria = db_session.execute(var_categoria).scalar()
    # Nova informação
    var_categoria.nome = str(input('Novo Nome:'))
    var_categoria.save()


# remove pessoas

def deletar_categoria():
    categoria_delete = input('Quem você deseja deletar?:')
    var_categoria = select(Categoria).where(categoria_delete == Categoria.nome)
    var_categoria = db_session.execute(var_categoria).scalar()
    var_categoria.delete()


def inserir_funcionario():
    funcionario = Funcionario(
        nome=str(input('Nome:')),
        salario=float(input('Salário:')),
        cpf=str(input('CPF:'))
    )

    print(funcionario)
    funcionario.save()


def consultar_funcionario():
    var_funcionario = select(Funcionario)
    var_funcionario = db_session.execute(var_funcionario).all()
    print(var_funcionario)


def atualizar_funcionario():
    # Seleciona o item a ser alterado
    var_funcionario = select(Funcionario).where(str(input('Nome: ')) == Funcionario.nome)
    var_funcionario = db_session.execute(var_funcionario).scalar()
    # Nova informação
    var_funcionario.nome = str(input('Novo Nome:'))
    var_funcionario.save()


# remove pessoas
def deletar_funcionario():
    funcionario_delete = input('Quem você deseja deletar?:')
    var_funcionario = select(Funcionario).where(funcionario_delete == Funcionario.nome)
    var_funcionario = db_session.execute(var_funcionario).scalar()
    var_funcionario.delete()


# def inserir_movimentacao_produto():
#     movimentacao_produto = Movimentacao_Produto(
#         produto=int(input('produto_id')),
#         movimentacao=int(input('ID')),
#     )
#
#     print(movimentacao_produto)
#     movimentacao_produto.save()
#
#
# def consultar_movimentacao_produto():
#     var_movimentacao_produto = select(Movimentacao_Produto)
#     var_movimentacao_produto = db_session.execute(var_movimentacao_produto).all()
#     print(var_movimentacao_produto)
#
#
# def atualizar_movimentacao_produto():
#     # Seleciona o item a ser alterado
#     var_movimentacao_produto = select(Movimentacao_Produto).where(str(input('Nome: ')) == Movimentacao_Produto.nome)
#     var_movimentacao_produto = db_session.execute(var_movimentacao_produto).scalar()
#     # Nova informação
#     var_movimentacao_produto.nome = str(input('Novo Nome:'))
#     var_movimentacao_produto.save()
#
#
# def deletar_movimentacao_produto():
#     movimentacao_produto_delete = input('Quem você deseja deletar?:')
#     var_movimentacao_produto = select(Funcionario).where(movimentacao_produto_delete == Funcionario.nome)
#     var_movimentacao_produto = db_session.execute(var_movimentacao_produto).scalar()
#     var_movimentacao_produto.delete()


if __name__ == '__main__':

    while True:
        print("Qual tabela você quer editar?")
        print("0 - sair")
        print("1 - produto")
        print("2 - movimentação")
        print("3 - funcionário")
        print("4 - categoria")

        escolha = input("Escolha: ")
        if escolha == "1":
            print("O que você quer fazer na tabela produto?")
            print("0 - sair")
            print("1 - inserir dados")
            print("2 - atualizar dados")
            print("3 - excluir dados")
            print("4 - consultar dados")

            escolha2 = input("Escolha: ")
            if escolha2 == "1":
                inserir_produto()
            elif escolha2 == "2":
                atualizar_produto()
            elif escolha2 == "3":
                deletar_produto()
            elif escolha2 == "4":
                consultar_produto()
            elif escolha == "0":
                break

        elif escolha == "2":
            print("O que você quer fazer na tabela movimentação?")
            print("0 - sair")
            print("1 - inserir dados")
            print("2 - atualizar dados")
            print("3 - excluir dados")
            print("4 - consultar dados")

            escolha2 = input("Escolha: ")
            if escolha2 == "1":
                inserir_movimentacao()
            elif escolha2 == "2":
                atualizar_movimentacao()
            elif escolha2 == "3":
                deletar_movimentacao()
            elif escolha2 == "4":
                consultar_movimentacao()
            elif escolha == "0":
                break

        elif escolha == "3":
            print("O que você quer fazer na tabela funcionário?")
            print("0 - sair")
            print("1 - inserir dados")
            print("2 - atualizar dados")
            print("3 - excluir dados")
            print("4 - consultar dados")

            escolha2 = input("Escolha: ")
            if escolha2 == "1":
                inserir_funcionario()
            elif escolha2 == "2":
                atualizar_funcionario()
            elif escolha2 == "3":
                deletar_funcionario()
            elif escolha2 == "4":
                consultar_funcionario()
            elif escolha == "0":
                break

        elif escolha == "4":
            print("O que você quer fazer na tabela categoria?")
            print("0 - sair")
            print("1 - inserir dados")
            print("2 - atualizar dados")
            print("3 - excluir dados")
            print("4 - consultar dados")

            escolha2 = input("Escolha: ")
            if escolha2 == "1":
                inserir_categoria()
            elif escolha2 == "2":
                atualizar_categoria()
            elif escolha2 == "3":
                deletar_categoria()
            elif escolha2 == "4":
                consultar_categoria()
            elif escolha == "0":
                break

        elif escolha == "0":
            break
