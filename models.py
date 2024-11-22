# importar bibliotecas
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, select
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base

engine = create_engine('sqlite:///nome.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


# projeto pessoas que tem atividades
class Produto(Base):
    __tablename__ = 'produto'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False, index=True)
    descricao = Column(String(80), nullable=False, index=True, )
    quantidade_produto = Column(Integer, nullable=False, )
    preco = Column(Float, nullable=False, index=True)
    categoria_id = Column(String, ForeignKey('categoria.id'))

    # representação classe
    def verificar_volume(self, volume_movimentacao):
        # o self serve para puxar dele mesmo
        if self.quantidade_produto >= volume_movimentacao:
            return True
        else:
            return False


    def __repr__(self):
        return ('<Produto: nome: {} descricao: {}  preço: {}'
                ' categoria_id:{} quantidade_produto: {}>'.format(self.nome, self.descricao,
                                                                  self.preco,
                                                                  self.categoria_id, self.quantidade_produto))
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
    salario = Column(String, nullable=False, index=False)

    # Senha Login
    # passaword = Column(String, nullable=False, inde=True)
    # username = Column(String, nullable=False, inde=True)

    def __repr__(self):
        return ('<Funcionario: nome: {}  cpf: {}  salario: {}>'.
                format(self.nome, self.cpf, self.salario
                       ))

        # função para salvar no banco

    def save(self):
        db_session.add(self)
        db_session.commit()

        # função para deletar

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_funcionario(self):
        dados_funcionario = {
            "id_funcionario": self.id,
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
    atividade = Column(String(10), nullable=False, index=True)  # 'entrada' ou 'saida'
    produto_movimentado = Column(Integer, ForeignKey('produto.id'), nullable=False)
    funcionario_movimentado = Column(Integer, ForeignKey('funcionario.id'), nullable=False)

    movimentacao_produto = relationship(Produto, backref='movimentacoes')
    movimentacao_funcionario = relationship(Funcionario, backref='movimentacoes')

    def __repr__(self):
        return '<Movimentacao: id: {} atividade: {} volume_movimentacao: {} produto: {} funcionário: {}>'.format(
            self.id,
            self.atividade,
            self.volume_movimentacao,
            self.produto_movimentado,
            self.funcionario_movimentado
        )

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_movimentacao(self):
        return {
            "id": self.id,
            "volume_movimentacao": self.volume_movimentacao,
            "atividade": self.atividade,
            "produto_movimentado": self.produto_movimentado,  # Exibindo apenas o ID do produto
            "funcionario_movimentado": self.funcionario_movimentado  # Exibindo apenas o ID do funcionário
        }


class Categoria(Base):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True)
    name_categoria = Column(String(20), nullable=False)

    def __repr__(self):
        return '<Categoria: name_categoria: {} id: {}>'.format(self.name_categoria, self.id)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_Categoria(self):
        dados_Categoria = {
            "id": self.id,
            "name_categoria": self.name_categoria,
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
        return '<Movimentação: {} {} {} {} {}>'.format(self.id, self.produto, self.produtos, self.movimentacao,
                                                       self.movimentacoes)

    def save(self):
        db_session.add(self)
        db_session.commit()

        # função para deletar

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_movimentacao_produto(self):
        dados_movimentacao_produto = {
            #   "id": self.id,
            "id_movimentacao": self.id,
            "id_produto": self.id
        }
        return dados_movimentacao_produto


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
