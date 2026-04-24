import os
import json
from datetime import datetime
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Config — env vars required: SPREADSHEET_ID, GOOGLE_CREDENTIALS_JSON
# ---------------------------------------------------------------------------
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
CREDS_JSON = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

app = FastAPI(title="Prospecção Vilas API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Google Sheets client (cached)
# ---------------------------------------------------------------------------
_gc = None


def get_gc():
    global _gc
    if _gc is None:
        creds = Credentials.from_service_account_info(CREDS_JSON, scopes=SCOPES)
        _gc = gspread.authorize(creds)
    return _gc


def get_spreadsheet():
    return get_gc().open_by_key(SPREADSHEET_ID)


# ---------------------------------------------------------------------------
# Seed data (42 leads)
# ---------------------------------------------------------------------------
SEED_LEADS = [
    # RESTAURANTES
    {"id":1,"nicho":"restaurante","name":"Restaurante Donana","phone":"(71) 3379-4364","rating":4.6,"reviews":3033,"addr":"Av. Praia de Itapuã, QD04 LT06 - Vilas","priority":"P1","website":False,"obs":"3K+ reviews. Sem site. Oportunidade enorme de tráfego pago.","status":"nao-contatado","instagram":"https://instagram.com/donanarestaurante","maps":"https://maps.google.com/?cid=2179164227317637632"},
    {"id":2,"nicho":"restaurante","name":"Ki-Mukeka","phone":"(71) 3369-5381","rating":4.6,"reviews":1453,"addr":"R. Praia do Tubarão, 70 - Vilas","priority":"P1","website":False,"obs":"Especialidade em moqueca. Grande volume de avaliações. Rede com 34K seguidores no IG.","status":"nao-contatado","instagram":"https://instagram.com/kimukeka","maps":"https://maps.google.com/?cid=2402224636865959270"},
    {"id":3,"nicho":"restaurante","name":"Mariposa - Vilas do Atlântico","phone":"(71) 3018-4690","rating":4.4,"reviews":2813,"addr":"Av. Praia de Itapuã, s/n - Vilas","priority":"P1","website":True,"obs":"Bar + música ao vivo. 38K seguidores no Instagram. Tem site mariposa.com.br.","status":"nao-contatado","instagram":"https://instagram.com/mariposavilas","site":"https://www.mariposa.com.br","maps":"https://maps.google.com/?cid=6016212904337810409"},
    {"id":4,"nicho":"restaurante","name":"Camarão Vilas","phone":"(71) 4009-4949","rating":4.5,"reviews":1597,"addr":"Av. Praia de Itapuã, 805 - Vilas","priority":"P1","website":False,"obs":"1.6K reviews. Tem Linktree com Instagram e Facebook linkados.","status":"nao-contatado","site":"https://linktr.ee/camaraovilas","maps":"https://maps.google.com/?cid=4300696539975391504"},
    {"id":5,"nicho":"restaurante","name":"Oscarito Restaurant","phone":"(71) 4113-1306","rating":4.5,"reviews":1097,"addr":"Al. Praia do Tubarão, QA12 - Vilas","priority":"P2","website":False,"obs":"Churrasco e buffet. Bom volume.","status":"nao-contatado","maps":"https://maps.google.com/?cid=2732622065490968672"},
    # ESTÉTICA
    {"id":6,"nicho":"estetica","name":"BellaClin Vilas","phone":"(71) 3508-5704","rating":4.8,"reviews":29,"addr":"R. Itagi, 599 Ed. Mediterrâneo - Pitangueiras","priority":"P1","website":True,"obs":"Medicina estética. Nicho de ticket alto. Ativo digitalmente.","status":"nao-contatado","site":"https://dietadetox1000.blogspot.com","maps":"https://maps.google.com/?cid=8820280970661337207"},
    {"id":7,"nicho":"estetica","name":"Royal Face Clínica","phone":"(71) 98433-2665","rating":4.7,"reviews":40,"addr":"Av. Praia de Itapuã, 805 - Vilas","priority":"P1","website":True,"obs":"Franquia com site próprio. Potencial de escalar campanhas.","status":"nao-contatado","site":"https://royalface.com.br/unidade/lauro-de-freitas-ba/","maps":"https://maps.google.com/?cid=5118448392387256726"},
    {"id":8,"nicho":"estetica","name":"Prime S Clinic","phone":"(71) 99169-0380","rating":5.0,"reviews":11,"addr":"Av. Luiz Tarquínio Pontes, 2580 - Buraquinho","priority":"P2","website":False,"obs":"5 estrelas. Pequena mas qualidade alta.","status":"nao-contatado","maps":"https://maps.google.com/?cid=15909270210003247780"},
    {"id":9,"nicho":"estetica","name":"Clínica Angellis","phone":"(71) 99988-5464","rating":5.0,"reviews":5,"addr":"Estação Villas Shopping - Av. Priscila Dutra, 389","priority":"P2","website":False,"obs":"Nova, 5 estrelas, boa localização no shopping.","status":"nao-contatado","maps":"https://maps.google.com/?cid=7448861896042751287"},
    {"id":10,"nicho":"estetica","name":"Revitalle Clinic","phone":"(71) 3024-3935","rating":4.3,"reviews":29,"addr":"Av. Praia de Itapuã, 381 - Vilas","priority":"P3","website":False,"obs":"Reviews mistas. Precisam melhorar presença online.","status":"nao-contatado","maps":"https://maps.google.com/?cid=2402224636865959270"},
    # SAÚDE
    {"id":11,"nicho":"saude","name":"Bem Sorriso Implantes","phone":"(71) 3015-5484","rating":5.0,"reviews":309,"addr":"Av. Praia de Itapuã, 319 - Vilas","priority":"P1","website":True,"obs":"309 reviews, 5 estrelas! Tem site clinicabemsorriso.com.br e Instagram @bemsorrisovilas.","status":"nao-contatado","instagram":"https://instagram.com/bemsorrisovilas","site":"https://clinicabemsorriso.com.br/vilas-do-atlantico/","maps":"https://maps.google.com/?cid=5571092489970760103"},
    {"id":12,"nicho":"saude","name":"Dentare Clínica Odontológica","phone":"(71) 99212-0622","rating":5.0,"reviews":167,"addr":"Av. Praia de Itapuã, 1670 - Vilas","priority":"P1","website":True,"obs":"Implantes + aparelhos. 5 estrelas. Tem Facebook e site.","status":"nao-contatado","site":"https://www.facebook.com/dentareodonto/","maps":"https://maps.google.com/?cid=14430778771240994664"},
    {"id":13,"nicho":"saude","name":"Villas Dental Clinic","phone":"(71) 3369-0414","rating":4.9,"reviews":123,"addr":"Av. Praia de Itapuã, 408 - Vilas","priority":"P1","website":True,"obs":"Tem site próprio villasdental.com.br com tour 360°. Alta tecnologia.","status":"nao-contatado","site":"https://villasdental.com.br/","maps":"https://maps.google.com/?cid=5118448392387256726"},
    {"id":14,"nicho":"saude","name":"Jeice Lima Nutricionista","phone":"(71) 98403-0485","rating":5.0,"reviews":182,"addr":"Av. Luiz Tarquínio Pontes, 2580 - Buraquinho","priority":"P1","website":False,"obs":"182 reviews! Forte presença no Instagram com desafios e conteúdo. Excelente para escalar.","status":"nao-contatado","instagram":"https://instagram.com/nutrijeicelima","maps":"https://maps.google.com/?cid=8820280970661337207"},
    {"id":15,"nicho":"saude","name":"Michelle Guerra Nutricionista","phone":"(71) 98159-8999","rating":5.0,"reviews":15,"addr":"R. Praia de Ondina, 50 - Vilas","priority":"P2","website":False,"obs":"Excelentes avaliações. Boa para campanhas de captação de pacientes.","status":"nao-contatado","maps":"https://maps.google.com/?cid=5571092489970760103"},
    {"id":16,"nicho":"saude","name":"Infinity Odonto Vilas","phone":"(71) 98882-3474","rating":4.9,"reviews":29,"addr":"Av. Luiz Tarquínio Pontes, 2580 - Vilas","priority":"P2","website":False,"obs":"Clareamento dental em destaque nas avaliações.","status":"nao-contatado","maps":"https://maps.google.com/?cid=2179164227317637632"},
    {"id":17,"nicho":"saude","name":"Nutricionista Cyntia Câmara","phone":"(71) 99919-4915","rating":5.0,"reviews":5,"addr":"Av. Praia de Itapuã, 1686 - Vilas","priority":"P2","website":False,"obs":"Nutrição integrativa + acupuntura. Ticket diferenciado.","status":"nao-contatado","maps":"https://maps.google.com/?cid=14430778771240994664"},
    # ACADEMIA
    {"id":18,"nicho":"academia","name":"Studio Kore - Funcional","phone":"(71) 99152-5662","rating":4.8,"reviews":47,"addr":"Av. Praia de Itapuã, 1808 - Vilas","priority":"P1","website":True,"obs":"Studio premium. Franquia com 87K seguidores no IG nacional. Unidade local @kore.bahia.vilasdoatlantico.","status":"nao-contatado","instagram":"https://instagram.com/kore.bahia.vilasdoatlantico","site":"https://studiokore.com.br/","maps":"https://maps.google.com/?cid=14430778771240994664"},
    {"id":19,"nicho":"academia","name":"Academia Vilas Fitness","phone":"(71) 99907-7895","rating":4.7,"reviews":180,"addr":"R. Praia de Ondina, 50 - Vilas","priority":"P1","website":True,"obs":"Academia grande. 180 reviews. Instagram @academiavilasfitness_. Espaço kids = diferencial.","status":"nao-contatado","instagram":"https://instagram.com/academiavilasfitness_","site":"https://www.academiavilasfitness.com/home/","maps":"https://maps.google.com/?cid=5571092489970760103"},
    {"id":20,"nicho":"academia","name":"Rede Fluir - Vilas","phone":"(71) 3024-3021","rating":4.8,"reviews":82,"addr":"Av. Priscila Dutra, S/N - Buraquinho","priority":"P2","website":False,"obs":"Fisioterapia + fitness. Ticket recorrente alto.","status":"nao-contatado","maps":"https://maps.google.com/?cid=15909270210003247780"},
    # SALÃO
    {"id":21,"nicho":"salao","name":"Villas Coiffeur","phone":"(71) 3508-0796","rating":4.7,"reviews":107,"addr":"Av. Priscila Dutra, 389 - Buraquinho","priority":"P1","website":False,"obs":"107 reviews. Público feminino premium. Presença no Instagram.","status":"nao-contatado","instagram":"https://instagram.com/villascoiffeurcentrodebeleza","maps":"https://maps.google.com/?cid=6316088598018556811"},
    {"id":22,"nicho":"salao","name":"Estação de Beleza Vilas","phone":"(71) 3289-4070","rating":4.7,"reviews":85,"addr":"R. Praia de Pajussara, 348 - Vilas","priority":"P1","website":False,"obs":"85 reviews. Tem Instagram ativo @estacaodebelezavilas. Salão completo.","status":"nao-contatado","instagram":"https://instagram.com/estacaodebelezavilas","maps":"https://maps.google.com/?cid=10381152542829611920"},
    {"id":23,"nicho":"salao","name":"Palazzo Spazio di Belleza","phone":"(71) 3287-1357","rating":4.5,"reviews":141,"addr":"Av. Praia de Itapuã, 571 - Vilas","priority":"P2","website":False,"obs":"141 reviews. Atendimento VIP conforme avaliações.","status":"nao-contatado","maps":"https://maps.google.com/?cid=18005118390911426139"},
    {"id":24,"nicho":"salao","name":"Rosenildes Mendes Cabeleireira","phone":"(71) 3251-9153","rating":4.6,"reviews":105,"addr":"Av. Praia de Itapuã, 1861 - Vilas","priority":"P2","website":False,"obs":"Especialista em loiras. Clientela fiel.","status":"nao-contatado","maps":"https://maps.google.com/?cid=6016212904337810409"},
    {"id":25,"nicho":"salao","name":"Lu Castro Studio de Beleza","phone":"(71) 99317-3415","rating":4.7,"reviews":48,"addr":"Av. Luiz Tarquínio Pontes, 2318 - Vilas","priority":"P2","website":False,"obs":"Avaliações mistas. Potencial de melhora com tráfego + reputação.","status":"nao-contatado","maps":"https://maps.google.com/?cid=15909270210003247780"},
    # PET
    {"id":26,"nicho":"pet","name":"Veterinary Clinic Vilas do Atlântico","phone":"(71) 3379-0092","rating":4.8,"reviews":170,"addr":"R. Praia do Mucuripe, 26 - Vilas","priority":"P1","website":False,"obs":"170 reviews, 4.8. Nicho pet com ticket recorrente alto.","status":"nao-contatado","maps":"https://maps.google.com/?cid=14430778771240994664"},
    {"id":27,"nicho":"pet","name":"Pettep","phone":"(71) 99695-7413","rating":4.8,"reviews":50,"addr":"Av. Praia de Itapuã, 374 - Vilas","priority":"P1","website":False,"obs":"Pet shop + clínica. 4.8 estrelas. 11K seguidores no IG @pettepbahia. Muito ativo.","status":"nao-contatado","instagram":"https://instagram.com/pettepbahia","maps":"https://maps.google.com/?cid=5571092489970760103"},
    {"id":28,"nicho":"pet","name":"Pet Vilas","phone":"(71) 99295-0648","rating":4.6,"reviews":233,"addr":"R. Ana C. B. Dias - Miragem","priority":"P2","website":False,"obs":"233 reviews. Volume alto. Reviews mistas — oportunidade de posicionamento.","status":"nao-contatado","maps":"https://maps.google.com/?cid=2402224636865959270"},
    {"id":29,"nicho":"pet","name":"Dr. Zoo & Cia Veterinária 24h","phone":"(71) 98796-5529","rating":4.3,"reviews":267,"addr":"R. Praia de Pajussara, 106 - Vilas","priority":"P2","website":False,"obs":"24h. Alto volume mas avaliações variadas.","status":"nao-contatado","maps":"https://maps.google.com/?cid=6016212904337810409"},
    # IMÓVEIS
    {"id":30,"nicho":"imoveis","name":"Silvia Porto Imóveis","phone":"(71) 99675-8989","rating":4.8,"reviews":24,"addr":"Av. Praia de Itapuã, 48 - Vilas","priority":"P1","website":False,"obs":"Corretora individual. Tráfego pago para captação de leads imob.","status":"nao-contatado","maps":"https://maps.google.com/?cid=14430778771240994664"},
    {"id":31,"nicho":"imoveis","name":"Linnda Imobiliária","phone":"(71) 99969-3434","rating":4.3,"reviews":15,"addr":"Av. Praia de Itapuã, 1067 - Vilas","priority":"P2","website":False,"obs":"Imobiliária local. Ticket alto por transação.","status":"nao-contatado","maps":"https://maps.google.com/?cid=5571092489970760103"},
    {"id":32,"nicho":"imoveis","name":"Tadeu Carvalho Corretor","phone":"(71) 99185-1348","rating":4.0,"reviews":4,"addr":"R. Praia de Itapema - Vilas","priority":"P2","website":False,"obs":"Corretor individual. Pode investir em leads qualificados.","status":"nao-contatado","maps":"https://maps.google.com/?cid=6016212904337810409"},
    # EDUCAÇÃO
    {"id":33,"nicho":"educacao","name":"Badermann Escola de Música","phone":"(71) 99272-9658","rating":5.0,"reviews":202,"addr":"Shopping Villas Boulevard - Av. Praia de Itapuã, 1137","priority":"P1","website":False,"obs":"5 estrelas, 202 reviews! Forte Instagram @badermann.musica.","status":"nao-contatado","instagram":"https://instagram.com/badermann.musica","maps":"https://maps.google.com/?cid=7448861896042751287"},
    {"id":34,"nicho":"educacao","name":"Kidsland Creche Escola","phone":"(71) 99608-1136","rating":5.0,"reviews":64,"addr":"R. Maria dos Réis Silva, 312 - Miragem","priority":"P1","website":False,"obs":"5 estrelas. Escola infantil premium. 5.3K seguidores @kidslandvilas. Público de alta renda.","status":"nao-contatado","instagram":"https://instagram.com/kidslandvilas","maps":"https://maps.google.com/?cid=14430778771240994664"},
    {"id":35,"nicho":"educacao","name":"Vilas Cursos (Number One)","phone":"—","rating":4.8,"reviews":31,"addr":"Av. Praia de Pajussara, 294 - Vilas","priority":"P2","website":False,"obs":"Franquia de inglês. Anúncios para matrículas.","status":"nao-contatado","maps":"https://maps.google.com/?cid=5571092489970760103"},
    {"id":36,"nicho":"educacao","name":"Escola Lápis Vilas","phone":"(71) 98430-6639","rating":4.8,"reviews":19,"addr":"R. Maria dos Réis Silva, 152 - Miragem","priority":"P2","website":False,"obs":"Berçário e Fundamental. Boa estrutura pedagógica.","status":"nao-contatado","maps":"https://maps.google.com/?cid=6316088598018556811"},
    # MODA
    {"id":37,"nicho":"moda","name":"MSTORE BA","phone":"(71) 99607-1116","rating":5.0,"reviews":15,"addr":"Av. Praia de Itapuã, 7 - Vilas","priority":"P1","website":False,"obs":"Moda masculina premium. 5 estrelas. Instagram ativo.","status":"nao-contatado","maps":"https://maps.google.com/?cid=2179164227317637632"},
    {"id":38,"nicho":"moda","name":"Loja Oyá Let'sGo","phone":"(71) 99677-9492","rating":4.9,"reviews":11,"addr":"Av. Praia de Itapuã, 935 - Vilas","priority":"P1","website":False,"obs":"Moda feminina. 4.9 estrelas. Peças exclusivas.","status":"nao-contatado","maps":"https://maps.google.com/?cid=6016212904337810409"},
    {"id":39,"nicho":"moda","name":"Vivi Moda Íntima","phone":"(71) 98349-6325","rating":4.8,"reviews":13,"addr":"Av. Praia de Itapuã, 248 - Vilas","priority":"P2","website":False,"obs":"Lingerie. Cliente fiel conforme reviews.","status":"nao-contatado","maps":"https://maps.google.com/?cid=18005118390911426139"},
    # JURÍDICO
    {"id":40,"nicho":"juridico","name":"Alvarez & Borba Advocacia","phone":"(71) 99333-7181","rating":5.0,"reviews":39,"addr":"Empresarial Atlântico - R. Itagi - Vilas","priority":"P1","website":False,"obs":"Especialidade digital: recuperação de contas Instagram/TikTok. Público nichado.","status":"nao-contatado","maps":"https://maps.google.com/?cid=5118448392387256726"},
    {"id":41,"nicho":"juridico","name":"Tatiane Costa Advocacia","phone":"(71) 99621-4242","rating":5.0,"reviews":51,"addr":"R. Praia de Pajussara, 294 - Vilas","priority":"P1","website":False,"obs":"51 reviews, 5 estrelas. Advocacia consumerista. Tráfego para captação.","status":"nao-contatado","maps":"https://maps.google.com/?cid=14430778771240994664"},
    {"id":42,"nicho":"juridico","name":"Carvalho Advocacia","phone":"(71) 99184-7649","rating":5.0,"reviews":11,"addr":"Estr. Min. Antônio Carlos Magalhães, 447 - Buraquinho","priority":"P2","website":False,"obs":"Família e patrimonial. Bom ticket médio.","status":"nao-contatado","maps":"https://maps.google.com/?cid=6316088598018556811"},
]

LEADS_HEADERS = [
    "id", "nicho", "name", "phone", "addr", "rating", "reviews",
    "priority", "status", "obs", "website", "instagram", "site", "maps",
    "customStatus", "customPriority", "customObs", "updated_at",
]

HISTORY_HEADERS = [
    "id", "lead_id", "lead_name", "field", "old_value", "new_value", "changed_at",
]


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------
@app.on_event("startup")
def startup():
    ss = get_spreadsheet()
    ws_leads = ss.worksheet("Leads")
    ws_history = ss.worksheet("Histórico")

    # Write headers if sheets are empty
    if not ws_leads.row_values(1):
        ws_leads.append_row(LEADS_HEADERS)
    if not ws_history.row_values(1):
        ws_history.append_row(HISTORY_HEADERS)

    # Seed leads if only the header row exists
    all_rows = ws_leads.get_all_values()
    if len(all_rows) <= 1:
        now = datetime.utcnow().isoformat()
        rows = []
        for l in SEED_LEADS:
            rows.append([
                l["id"], l["nicho"], l["name"], l.get("phone", ""),
                l.get("addr", ""), l.get("rating", 0), l.get("reviews", 0),
                l["priority"], l["status"], l.get("obs", ""),
                1 if l.get("website") else 0,
                l.get("instagram", ""), l.get("site", ""), l.get("maps", ""),
                l["status"],    # customStatus
                l["priority"],  # customPriority
                "",             # customObs
                now,
            ])
        ws_leads.append_rows(rows, value_input_option="RAW")


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class LeadUpdate(BaseModel):
    customStatus: Optional[str] = None
    customPriority: Optional[str] = None
    customObs: Optional[str] = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def row_to_lead(rec: dict) -> dict:
    return {
        "id": int(rec["id"]),
        "nicho": rec.get("nicho", ""),
        "name": rec.get("name", ""),
        "phone": rec.get("phone", ""),
        "addr": rec.get("addr", ""),
        "rating": float(rec["rating"]) if rec.get("rating") else 0.0,
        "reviews": int(rec["reviews"]) if rec.get("reviews") else 0,
        "priority": rec.get("priority", "P3"),
        "status": rec.get("status", "nao-contatado"),
        "obs": rec.get("obs", ""),
        "website": bool(int(rec["website"])) if rec.get("website") else False,
        "instagram": rec.get("instagram") or None,
        "site": rec.get("site") or None,
        "maps": rec.get("maps") or None,
        "customStatus": rec.get("customStatus") or rec.get("status", "nao-contatado"),
        "customPriority": rec.get("customPriority") or rec.get("priority", "P3"),
        "customObs": rec.get("customObs", ""),
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/leads")
def list_leads():
    ws = get_spreadsheet().worksheet("Leads")
    return [row_to_lead(r) for r in ws.get_all_records()]


@app.patch("/leads/{lead_id}")
def update_lead(lead_id: int, body: LeadUpdate):
    ss = get_spreadsheet()
    ws_leads = ss.worksheet("Leads")
    ws_history = ss.worksheet("Histórico")

    records = ws_leads.get_all_records()
    row_idx = None
    rec = None
    for i, r in enumerate(records):
        if int(r["id"]) == lead_id:
            row_idx = i + 2  # row 1 is headers, data starts at row 2
            rec = r
            break

    if row_idx is None:
        raise HTTPException(status_code=404, detail="Lead não encontrado")

    headers = ws_leads.row_values(1)
    col_map = {h: i + 1 for i, h in enumerate(headers)}

    now = datetime.utcnow().isoformat()
    field_map = [
        ("customStatus",   body.customStatus,   "status"),
        ("customPriority", body.customPriority, "prioridade"),
        ("customObs",      body.customObs,      "anotação"),
    ]

    # Build history rows for changed fields
    all_history_rows = ws_history.get_all_values()
    next_hist_id = len(all_history_rows)  # len includes header row

    history_rows = []
    updates_by_col = {}

    for col_name, new_val, label in field_map:
        if new_val is None:
            continue
        old_val = str(rec.get(col_name, "") or "")
        if old_val != new_val:
            history_rows.append([
                next_hist_id + len(history_rows),
                lead_id, rec["name"], label, old_val, new_val, now,
            ])
        if col_name in col_map:
            updates_by_col[col_map[col_name]] = new_val

    updates_by_col[col_map["updated_at"]] = now

    # Batch update lead row
    cell_updates = [
        {"range": gspread.utils.rowcol_to_a1(row_idx, col), "values": [[val]]}
        for col, val in updates_by_col.items()
    ]
    ws_leads.batch_update(cell_updates)

    if history_rows:
        ws_history.append_rows(history_rows, value_input_option="RAW")

    return {
        "id": lead_id,
        "customStatus": body.customStatus if body.customStatus is not None else rec.get("customStatus", rec.get("status")),
        "customPriority": body.customPriority if body.customPriority is not None else rec.get("customPriority", rec.get("priority")),
        "customObs": body.customObs if body.customObs is not None else rec.get("customObs", ""),
    }


@app.get("/history")
def get_history(limit: int = 30):
    ws = get_spreadsheet().worksheet("Histórico")
    records = ws.get_all_records()
    records.sort(key=lambda r: r.get("changed_at", ""), reverse=True)
    return records[:limit]


@app.get("/leads/{lead_id}/history")
def get_lead_history(lead_id: int):
    ws = get_spreadsheet().worksheet("Histórico")
    records = ws.get_all_records()
    filtered = [r for r in records if str(r.get("lead_id", "")) == str(lead_id)]
    return sorted(filtered, key=lambda r: r.get("changed_at", ""), reverse=True)


@app.get("/")
def root():
    return {"status": "ok", "message": "Prospecção Vilas API"}
