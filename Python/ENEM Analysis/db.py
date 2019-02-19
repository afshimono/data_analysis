import os
import sys
import configparser
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()

class Local(Base):
	__tablename__ = 'local'
	id = Column(Integer, primary_key=True)
	municipio = Column(String(250),nullable=False)
	estado = Column(String(5),nullable=False)

class Racial(Base):
	__tablename__ = 'racial'
	id = Column(Integer, primary_key=True)
	racial_id = Column(String(20),nullable=False)

class Nacionalidade(Base):
	__tablename__ = 'nacionalidade'
	id = Column(Integer, primary_key=True)
	nacionalidade = Column(String(50),nullable=False)

class EstadoCivil(Base):
	__tablename__ = 'estadocivil'
	id = Column(Integer, primary_key=True)
	estado_civil = Column(String(50),nullable=False)

class Exame(Base):
	__tablename__ = 'exame'
	candidato_id = Column(BigInteger, primary_key=True)
	exame_local_id = Column(Integer,ForeignKey('local.id'))
	exame_local = relationship(Local,
		primaryjoin=exame_local_id==Local.id,
                                post_update=True)       
	local_nasc_id = Column(Integer,ForeignKey('local.id'))
	local_nasc = relationship(Local,
		primaryjoin=local_nasc_id==Local.id,
                                post_update=True) 
	residencia_id = Column(Integer,ForeignKey('local.id'))
	residencia = relationship(Local,
		primaryjoin=residencia_id==Local.id,
                                post_update=True) 
	ano = Column(Integer,nullable=False)
	idade = Column(Integer,nullable=True)
	racial_id = Column(Integer,ForeignKey('racial.id'))
	racial = relationship(Racial,
		primaryjoin=racial_id==Racial.id,
                                post_update=True) 
	nacional_id = Column(Integer,ForeignKey('nacionalidade.id'))
	nacional = relationship(Nacionalidade,
		primaryjoin=nacional_id==Nacionalidade.id,
                                post_update=True) 
	casado_id = Column(Integer,ForeignKey('estadocivil.id'))
	casado = relationship(EstadoCivil,
		primaryjoin=casado_id==EstadoCivil.id,
                                post_update=True) 
	sexo = Column(String(1),nullable=True)

	nota_cn = Column(Float,nullable=False)
	nota_ch = Column(Float,nullable=False)
	nota_lc = Column(Float,nullable=False)
	nota_mt = Column(Float,nullable=False)
	nota_red = Column(Float,nullable=False)



def populate_basic_tables(engine):
	Session = sessionmaker(bind=engine)
	session = Session()
	session.add_all([
		EstadoCivil(id=0,estado_civil='Solteiro(a)'),
		EstadoCivil(id=1,estado_civil='Casado(a)/Mora com companheiro(a)'),
		EstadoCivil(id=2,estado_civil='Divorciado(a)/Desquitado(a)/Separado(a)'),
		EstadoCivil(id=3,estado_civil='Viúvo(a)'),
		Nacionalidade(id=0,nacionalidade='Não informado'),
		Nacionalidade(id=1,nacionalidade='Brasileiro(a)'),
		Nacionalidade(id=2,nacionalidade='Brasileiro(a) Naturalizado(a)'),
		Nacionalidade(id=3,nacionalidade='Estrangeiro(a)'),
		Nacionalidade(id=4,nacionalidade='Brasileiro(a) Nato(a), nascido(a) no exterior'),
		Racial(id=0,racial_id='Não declarado'),
		Racial(id=1,racial_id='Branca'),
		Racial(id=2,racial_id='Preta'),
		Racial(id=3,racial_id='Parda'),
		Racial(id=4,racial_id='Amarela'),
		Racial(id=5,racial_id='Indigena')])
	session.commit()
	session.close()

#Will return a connector to a DB
def get_db_engine(create_schema=False):
	#Reads DB info from config file
	config = configparser.ConfigParser()
	config.read('database.cfg')
	username = config['DEFAULT']['user']
	password = config['DEFAULT']['password']
	url = config['DEFAULT']['url']
	dbname = config['DEFAULT']['dbname']

	engine = create_engine('postgresql://'+username+':'+password+'@'+url+'/'+dbname)
	engine.connect()
	if create_schema:
		Base.metadata.drop_all(engine)
		Base.metadata.create_all(engine)
		populate_basic_tables(engine)
	return engine

#Returns the Session element with the database. Must not
#be used along with get_db_engine, you must choose between them
def get_db_session(create_schema=False):
	Session = sessionmaker(bind=get_db_engine(create_schema=create_schema))
	return Session()





