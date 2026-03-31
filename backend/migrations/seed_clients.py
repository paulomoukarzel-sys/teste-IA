"""Migra os 65 clientes do array JS do dashboard para o SQLite."""

import asyncio
import re
from pathlib import Path
from sqlalchemy import select
from backend.database import async_session, init_db
from backend.models import Client
from backend.services.client_service import _find_client_folder

# Dados extraidos do dashboard_clientes.html
CLIENTS_DATA = [
    {"nome":"Alexandre Westphal - ind. Stella","status":"Ativa","peticoes":4,"tipos":4,"sintese":"Peticao Inicial (cumprimento de sentenca); Pedido de Citacao; Pedido de Penhora (SISBAJUD e RENAJUD); Reiteracao SISBAJUD"},
    {"nome":"Ana Paula Medeiros","status":"Ativa","peticoes":8,"tipos":7,"sintese":"Pedido de Acesso aos Autos; Resposta a Acusacao; Substituicao e Intimacao de Testemunhas; Reiteracao de Endereco de Testemunhas; Desistencia da Oitiva de Testemunhas; Pedido de Descadastramento de Advogado; Pedido de Indeferimento de Assistencia da Acusacao"},
    {"nome":"Anna Clara Carvalho (Fitosil)","status":"Ativa","peticoes":4,"tipos":3,"sintese":"Agravo Interno; Memoriais; Objecao ao Julgamento Virtual"},
    {"nome":"Ariel Ramos Rosa","status":"Ativa","peticoes":7,"tipos":6,"sintese":"REsp; RE; Embargos de Declaracao; Memoriais; Juntada de Ata Notarial; Pedido de Retirada de Pauta"},
    {"nome":"Augusto Pereira da Silva","status":"Ativa","peticoes":6,"tipos":5,"sintese":"Resposta a Acusacao; Pedido de Extincao da Punibilidade; Intimacao Pessoal; Pedido de Suspensao de Execucao Fiscal; Pedido de Expedicao de Alvara e Liberacao de Bloqueio SISBAJUD"},
    {"nome":"Banco Real (Bradesco) - Bruno Gastao","status":"Ativa","peticoes":1,"tipos":1,"sintese":"Peticao avulsa"},
    {"nome":"Bi Tax - Lobo e Vaz Advogados","status":"Ativa","peticoes":3,"tipos":2,"sintese":"Contestacao com Reconvencao; Manifestacao a Contestacao; Requerimento de Julgamento Antecipado"},
    {"nome":"Brunao Andrade","status":"Ativa","peticoes":1,"tipos":1,"sintese":"Recurso JARI"},
    {"nome":"Carlos Munaretto","status":"Ativa","peticoes":12,"tipos":6,"sintese":"AREsp; RE; REsp; Agravo Interno (AgRg e AgInt); Embargos de Declaracao; Peticao de Nulidade e Prosseguimento do Feito"},
    {"nome":"Cris Damim (amigo Rui)","status":"Ativa","peticoes":5,"tipos":4,"sintese":"Replica; Especificacao de Provas; Embargos de Declaracao; Contrarrazoes"},
    {"nome":"Cristian Vieira (marinheiro Edenir)","status":"Ativa","peticoes":2,"tipos":2,"sintese":"Defesa Previa (recusa bafometro); Recurso JARI"},
    {"nome":"Daniel de Sena Pletikos","status":"Ativa","peticoes":17,"tipos":10,"sintese":"Resposta a Acusacao; RESE; Apelacao Criminal; Memoriais; Objecao ao Julgamento Virtual; Embargos de Declaracao; REsp; AREsp; Habeas Corpus; Termo de Acordo (pensao)"},
    {"nome":"Eduarda de Sa Gesser","status":"Ativa","peticoes":1,"tipos":1,"sintese":"Habeas Corpus"},
    {"nome":"Elena Oriana de Benedictis","status":"Ativa","peticoes":41,"tipos":16,"sintese":"Peticao Inicial; Contestacao; Contrarrazoes; Replica; Alegacoes Finais; Memoriais; Embargos de Declaracao; Apelacao; REsp; Objecao ao Julgamento Virtual; Manifestacoes diversas; Pedido de Suspensao; Juntada de documentos; Cumprimento de Sentenca; Pedido de Expedicao de Alvara; Desistencia"},
    {"nome":"Elierri Medeiros","status":"Ativa","peticoes":8,"tipos":6,"sintese":"Contestacao; Alegacoes Finais; Manifestacoes; Juntada de documentos; Preparacao para AIJ; Peticoes diversas"},
    {"nome":"Emerson Trevisol","status":"Ativa","peticoes":2,"tipos":2,"sintese":"Defesa Previa (recusa bafometro); Recurso JARI"},
    {"nome":"Fernanda Moukarzel","status":"Ativa","peticoes":2,"tipos":2,"sintese":"Defesa Previa (recusa bafometro); Recurso JARI"},
    {"nome":"Fernando Soares da Luz","status":"Ativa","peticoes":22,"tipos":13,"sintese":"Alegacoes Finais; Apelacao; Embargos de Declaracao; Memoriais; REsp; AREsp; AgRg no AREsp; Agravo Interno; Habeas Corpus; Juntada de documentos; Objecao ao Julgamento Virtual; Pedido de Retirada de Pauta; Peticoes diversas"},
    {"nome":"Gastao da Rosa e Moukarzel Adv. Associados","status":"Ativa","peticoes":9,"tipos":6,"sintese":"Peticao Inicial (cumprimento de sentenca); Contrarrazoes; Embargos de Declaracao; Manifestacoes; Pedido de Penhora; Peticoes diversas"},
    {"nome":"Gean Alessandro Silveira Byler","status":"Ativa","peticoes":17,"tipos":11,"sintese":"Contestacao; Apelacao; Memoriais; AREsp; REsp; Agravo Interno; Agravo; Juntada de documentos; Objecao ao Julgamento Virtual; Pedido de Acesso aos Autos; Peticoes diversas"},
    {"nome":"Geraldo Otto Weber","status":"Ativa","peticoes":20,"tipos":12,"sintese":"Alegacoes Finais; RESE; Habeas Corpus; Contrarrazoes; Memoriais; Agravo; Embargos de Declaracao; REsp; Juntada de documentos; Objecao ao Julgamento Virtual; Peticoes diversas"},
    {"nome":"Gilson dos Santos","status":"Ativa","peticoes":15,"tipos":11,"sintese":"Peticao Inicial; Replica; Especificacao de Provas; Apelacao; Contrarrazoes; Embargos de Declaracao; Memoriais; Objecao ao Julgamento Virtual; Pedido de Suspensao; REsp; AREsp"},
    {"nome":"Heitor Koerich da Silveira","status":"Ativa","peticoes":1,"tipos":1,"sintese":"Juntada de documentos"},
    {"nome":"Ivanir Alves Dias Parizotto","status":"Ativa","peticoes":14,"tipos":12,"sintese":"Pedido de Acesso; Recurso Inominado; Replica; Especificacao de Provas; Alegacoes Finais; Apelacao; Contrarrazoes; Memoriais; Embargos de Declaracao; REsp; Objecao ao Julgamento Virtual; Juntada de documentos"},
    {"nome":"Luciano Nivaldo","status":"Ativa","peticoes":11,"tipos":6,"sintese":"Peticao Inicial; Replica; Apelacao; Embargos de Declaracao; Juntada de documentos; Peticoes diversas"},
    {"nome":"Luiz Antonio - Toni EuroQuadros","status":"Ativa","peticoes":1,"tipos":1,"sintese":"Pedido de Suspensao"},
    {"nome":"Manuel Ribeiro","status":"Ativa","peticoes":1,"tipos":1,"sintese":"Recurso"},
    {"nome":"Margarete Fukushima (Espolio de Rioitsu)","status":"Ativa","peticoes":3,"tipos":3,"sintese":"Contestacao; Especificacao de Provas; Juntada de documentos"},
    {"nome":"Maria Ap. Gastao - Espolio de Claudio","status":"Ativa","peticoes":18,"tipos":10,"sintese":"Cumprimento de Sentenca (multiplos); Contrarrazoes; Memoriais; Embargos de Declaracao; Manifestacoes; Juntada de documentos; Pedido de Citacao; Pedido de Expedicao de Alvara; Concordancia; Comprovacao de Pagamento"},
    {"nome":"Mayck Torres Mates","status":"Ativa","peticoes":18,"tipos":11,"sintese":"Habeas Corpus; Memoriais; AREsp; REsp; Agravo Interno; Contrarrazoes; Embargos de Declaracao; Juntada de documentos; Objecao ao Julgamento Virtual; Pedido de Retirada de Pauta; Peticoes diversas"},
    {"nome":"Murilo Bongiolo","status":"Ativa","peticoes":2,"tipos":2,"sintese":"Defesa Previa (recusa bafometro); Recurso JARI"},
    {"nome":"Parcerias com o Delegado Ilson","status":"Ativa","peticoes":10,"tipos":4,"sintese":"Defesa Previa; Recurso; Memoriais; Peticoes diversas"},
    {"nome":"Paulo Moukarzel Jr","status":"Ativa","peticoes":1,"tipos":1,"sintese":"Defesa Previa"},
    {"nome":"Rafael de Melo","status":"Ativa","peticoes":1,"tipos":1,"sintese":"Peticao avulsa"},
    {"nome":"Revail Pires de Lima","status":"Ativa","peticoes":3,"tipos":3,"sintese":"Peticao Inicial; Embargos de Declaracao; Juntada de documentos"},
    {"nome":"Rodrigo Bertoldi","status":"Ativa","peticoes":3,"tipos":2,"sintese":"Defesa Previa; Recurso"},
    {"nome":"Stella Maris Seixas","status":"Ativa","peticoes":4,"tipos":3,"sintese":"Cumprimento de Sentenca; Reiteracao; Peticoes diversas"},
    {"nome":"Vagner Silva de Borba","status":"Ativa","peticoes":2,"tipos":2,"sintese":"Juntada de documentos; Manifestacao"},
    {"nome":"Vera Moukarzel","status":"Ativa","peticoes":11,"tipos":9,"sintese":"Peticao Inicial; Apelacao; Memoriais; Embargos de Declaracao; Cumprimento de Sentenca; Concordancia; Juntada de documentos; Manifestacao; Peticoes diversas"},
    {"nome":"Wellington Rodrigues Ferreira (Wellmix)","status":"Ativa","peticoes":10,"tipos":7,"sintese":"RESE; REsp; Contrarrazoes; Memoriais; Juntada de documentos; Peticoes diversas; Habeas Corpus"},
    {"nome":"Adilson Gomes","status":"Encerrada","peticoes":5,"tipos":2,"sintese":"AREsp; AgRg no AREsp; RE; Embargos de Declaracao (2x)"},
    {"nome":"Alex Jose Goncalves","status":"Encerrada","peticoes":0,"tipos":0,"sintese":"Apenas procuracao"},
    {"nome":"Ana Claudia Thober","status":"Encerrada","peticoes":2,"tipos":2,"sintese":"Recurso; Juntada de atestado no IP"},
    {"nome":"Fabiola Gomes (Esposa Paulinho)","status":"Encerrada","peticoes":2,"tipos":2,"sintese":"Alegacoes Finais; Preparacao para AIJ"},
    {"nome":"Felipe Vasconcelos","status":"Encerrada","peticoes":0,"tipos":0,"sintese":"Minuta de contrato"},
    {"nome":"Felipe Vieira","status":"Encerrada","peticoes":1,"tipos":1,"sintese":"Pedido de TAC"},
    {"nome":"Heitor Roecker Vieira","status":"Encerrada","peticoes":0,"tipos":0,"sintese":"Documentos locaticios (entrega de chaves, recibo, rescisao)"},
    {"nome":"Laura Toscan Mitterer","status":"Encerrada","peticoes":0,"tipos":0,"sintese":"Apenas procuracao"},
    {"nome":"Leonardo Henriques Maciel","status":"Encerrada","peticoes":2,"tipos":2,"sintese":"Contestacao; Pedido de Homologacao de Renuncia"},
    {"nome":"Lincoln Zaghi Jr","status":"Encerrada","peticoes":8,"tipos":6,"sintese":"Habeas Corpus; RHC (STJ); RESE contra pronuncia; Pedido de Revogacao de Prisao Preventiva; Memoriais; Nota a imprensa"},
    {"nome":"Luciano Petry","status":"Encerrada","peticoes":2,"tipos":2,"sintese":"Agravo; Pedido de Detracao"},
    {"nome":"Maria Aparecida Co","status":"Encerrada","peticoes":7,"tipos":5,"sintese":"Contrarrazoes (AI e AgInt); Embargos de Declaracao; Manifestacoes (ITCMD e evento 337); Concordancia dos Herdeiros com Plano de Partilha; Juntada de documentos"},
    {"nome":"Maria Fernanda Dias","status":"Encerrada","peticoes":1,"tipos":1,"sintese":"Inicial de Dissolucao de Uniao Estavel"},
    {"nome":"Osvaldo Peixer Neto","status":"Encerrada","peticoes":1,"tipos":1,"sintese":"Inicial de Dissolucao de Uniao Estavel (consensual)"},
    {"nome":"Pablo Espindola Dal Maso","status":"Encerrada","peticoes":2,"tipos":2,"sintese":"Defesa Previa (recusa bafometro); Recurso"},
    {"nome":"Renato Hercilio Bertoldi","status":"Encerrada","peticoes":11,"tipos":10,"sintese":"Alegacoes Finais; Contrarrazoes (EDs); Embargos de Declaracao; Apelacao; Juntada de certidao de arquivamento; Defesa Previa (multa); Recurso JARI; Peticoes diversas; Pedido de Prosseguimento; Acordo (reintegracao de posse)"},
    {"nome":"Ricobert Bach","status":"Encerrada","peticoes":3,"tipos":3,"sintese":"Contestacao; Embargos de Declaracao; Comprovacao de Pagamento (cumprimento de sentenca)"},
    {"nome":"Rivael Pires de Lima","status":"Encerrada","peticoes":1,"tipos":1,"sintese":"Recurso administrativo (DETRAN)"},
    {"nome":"Rodrigo Bruggemann","status":"Encerrada","peticoes":1,"tipos":1,"sintese":"Pedido de Acesso ao IP"},
    {"nome":"Silvio Cristovao (Wellmix)","status":"Encerrada","peticoes":2,"tipos":2,"sintese":"Memoriais; Juntada de memoriais"},
    {"nome":"Thays Oliveira","status":"Encerrada","peticoes":2,"tipos":2,"sintese":"Medida Protetiva; Pedido de Acesso e Copia dos Autos"},
    {"nome":"Tiago Civa","status":"Encerrada","peticoes":0,"tipos":0,"sintese":"Apenas procuracao"},
    {"nome":"Tomaz Agenor Aguiar","status":"Encerrada","peticoes":2,"tipos":2,"sintese":"Defesa (execucao); Renuncia"},
    {"nome":"Vitor de Farias","status":"Encerrada","peticoes":4,"tipos":3,"sintese":"Juntada de Procuracao; Pedido de Acesso aos Autos; Renuncia"},
    {"nome":"Volnei Muniz Lima","status":"Encerrada","peticoes":0,"tipos":0,"sintese":"Apenas procuracao"},
    {"nome":"Yxpia","status":"Encerrada","peticoes":1,"tipos":1,"sintese":"Carta para entrega de produtos (FEMSA)"},
]


async def seed():
    """Insere os 65 clientes no banco se estiver vazio."""
    await init_db()

    async with async_session() as session:
        result = await session.execute(select(Client))
        existing = result.scalars().all()

        if existing:
            print(f"Banco ja possui {len(existing)} clientes. Seed ignorado.")
            return

        for data in CLIENTS_DATA:
            folder = _find_client_folder(data["nome"])
            client = Client(
                nome=data["nome"],
                status=data["status"],
                peticoes=data["peticoes"],
                tipos=data["tipos"],
                sintese=data["sintese"],
                folder_path=folder,
            )
            session.add(client)

        await session.commit()
        print(f"Seed concluido: {len(CLIENTS_DATA)} clientes inseridos.")


if __name__ == "__main__":
    asyncio.run(seed())
