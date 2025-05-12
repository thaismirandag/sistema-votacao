import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.database import async_session
from app.models.participante import Participante

async def inserir_participantes():
    async with async_session() as session:
        participante1 = Participante(nome="Participante 1", foto_url='http://example.com/foto1.jpg')
        participante2 = Participante(nome="Participante 2", foto_url='http://example.com/foto2.jpg')

        session.add_all([participante1, participante2])
        await session.commit()

        print("Participantes inseridos com sucesso!")

if __name__ == "__main__":
    asyncio.run(inserir_participantes())
