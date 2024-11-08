# importar bibliotecas
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('sqlite:///nome.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


# projeto pessoas que tem atividades
class Produto(Base):
    __tablename__ = 'produto'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False, index=True)
    descricao = Column(String(80), nullable=False, index=True,)
    quantidade_produto = Column(Integer, nullable=False,)
    preco = Column(Float, nullable=False, unique=True)
    categoria_id = Column(Integer, ForeignKey('categoria.id'))



    # representação classe
    def __repr__(self):
        return '<Produto: nome: {} descricao: {}  quantidade_produto: {} preço: {} categoria id: {}'.format(self.nome, self.descricao, self.quantidade_produto, self.preco, self.categoria_id)

    # função para salvar no banco

    def save(self):
        db_session.add(self)
        db_session.commit()

    # função para deletar
    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_produto(self):
        dados_produto = {
            "id_produto": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "quantidade_produto": self.quantidade_produto,
            "preco": self.preco,
            "categoria_id": self.categoria_id
        }
        return dados_produto

# class funcionários
class Funcionario(Base):
    __tablename__ = 'funcionario'
    nome = Column(String(40), nullable=False, index=True)
    id = Column(Integer, primary_key=True, unique=True)
    cpf = Column(String(11), nullable=False, index=True, unique=True)
    salario = Column(Float, nullable=False, index=False)

    # Senha Login
    # passaword = Column(String, nullable=False, inde=True)
    # username = Column(String, nullable=False, inde=True)


    def __repr__(self):
        return '<Funcionario: nome: {}  cpf: {}  salario: {}  id:{}>' .format(self.nome, self.cpf, self.salario, self.id)

    # função para salvar no banco
    def save(self):
        db_session.add(self)
        db_session.commit()

    #função para deletar
    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_funcionario(self):
        dados_funcionario = {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "salario": self.salario,
        }
        return dados_funcionario




# class movimentação
class Movimentacao(Base):
    __tablename__ = 'movimentacao'
    id = Column(Integer, primary_key=True)
    volume_movimentacao = Column(Integer, nullable=False)
    atividade = Column(String(10), nullable=False, index=True)
    produto_movimentado = Column(Integer,ForeignKey('produto.id'), nullable=False)
    funcionario_movimentado = Column(Integer,ForeignKey('funcionario.id'), nullable=False)

    movimentacao_produto = relationship(Produto)
    movimentacao_funcionario = relationship(Funcionario)


    def __repr__(self):
        return '<Movimentação: id: {} atividade: {} volume_movimentacao: {} movimentacao_funcionario: {} movimentacao_produto: {} >' .format(self.id, self.atividade, self.volume_movimentacao, self.movimentacao_funcionario, self.movimentacao_produto)

    # função para salvar no banco
    def save(self):
        db_session.add(self)
        db_session.commit()

    #função para deletar
    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_movimentacao(self):
        dados_movimentacao = {
            "id": self.id,
            "volume": self.volume_movimentacao,
            "tipo de movimentação": self.atividade,
            "funconário responsável": self.movimentacao_funcionario,
            "produto": self.movimentacao_produto
        }
        return dados_movimentacao


class Categoria(Base):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True)
    nome_classificacao = Column(String(20), nullable=False)

    def __repr__(self):
        return '<Categoria: nome_classificacao: {} id: {}>' .format(self.nome_classificacao, self.id)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_Categoria(self):
        dados_Categoria = {
            "id_Categoria": self.id,
            "nome_classificacao": self .nome_classificacao,
        }
        return dados_Categoria


class Movimentacao_Produto(Base):
    __tablename__ = 'movimentacao_produto'
    id = Column(Integer, primary_key=True)
    produto = Column(Integer, ForeignKey('produto.id'), nullable=False)
    produtos = relationship(Produto)

    movimentacao = Column(Integer, ForeignKey('movimentacao.id'), nullable=False)
    movimentacoes = relationship(Movimentacao)

    def __repr__(self):
        return '<Movimentação: {} {} {} {} {}>' .format(self.id, self.produto, self.produtos, self.movimentacao, self.movimentacoes)

    def save(self):
        db_session.add(self)
        db_session.commit()

        # função para deletar
    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_movimentacao_produto(self):
        dados_movimentacao_produto = {
            "id": self.id,
            "id_movimentacao": self.id,
            "id_produto": self.id
        }
        return dados_movimentacao_produto

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()