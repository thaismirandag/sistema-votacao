from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.participante import Participante
from app.core.config import get_settings


settings = get_settings()
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()


participante1 = Participante(nome='Participante 1', foto_url='http://example.com/foto1.jpg')
participante2 = Participante(nome='Participante 2', foto_url='http://example.com/foto2.jpg')


session.add(participante1)
session.add(participante2)


session.commit()

session.close()

print("Participantes criados com sucesso!")