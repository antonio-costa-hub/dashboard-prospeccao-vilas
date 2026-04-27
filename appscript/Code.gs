// ============================================================
// Dashboard Prospecção Vilas — Google Apps Script Backend
// Cria e gerencia a planilha automaticamente na primeira execução
// ============================================================

var LEADS_HEADERS = ['id','nicho','name','phone','addr','rating','reviews','priority','status','obs','website','instagram','site','maps','customStatus','customPriority','customObs','updated_at'];
var HISTORY_HEADERS = ['id','lead_id','lead_name','field','old_value','new_value','changed_at'];

var SEED_LEADS = [
  {id:1,nicho:'restaurante',name:'Restaurante Donana',phone:'(71) 3379-4364',rating:4.6,reviews:3033,addr:'Av. Praia de Itapuã, QD04 LT06 - Vilas',priority:'P1',website:false,obs:'3K+ reviews. Sem site. Oportunidade enorme de tráfego pago.',status:'nao-contatado',instagram:'https://instagram.com/donanarestaurante',maps:'https://maps.google.com/?cid=2179164227317637632'},
  {id:2,nicho:'restaurante',name:'Ki-Mukeka',phone:'(71) 3369-5381',rating:4.6,reviews:1453,addr:'R. Praia do Tubarão, 70 - Vilas',priority:'P1',website:false,obs:'Especialidade em moqueca. Grande volume de avaliações. Rede com 34K seguidores no IG.',status:'nao-contatado',instagram:'https://instagram.com/kimukeka',maps:'https://maps.google.com/?cid=2402224636865959270'},
  {id:3,nicho:'restaurante',name:'Mariposa - Vilas do Atlântico',phone:'(71) 3018-4690',rating:4.4,reviews:2813,addr:'Av. Praia de Itapuã, s/n - Vilas',priority:'P1',website:true,obs:'Bar + música ao vivo. 38K seguidores no Instagram. Tem site mariposa.com.br.',status:'nao-contatado',instagram:'https://instagram.com/mariposavilas',site:'https://www.mariposa.com.br',maps:'https://maps.google.com/?cid=6016212904337810409'},
  {id:4,nicho:'restaurante',name:'Camarão Vilas',phone:'(71) 4009-4949',rating:4.5,reviews:1597,addr:'Av. Praia de Itapuã, 805 - Vilas',priority:'P1',website:false,obs:'1.6K reviews. Tem Linktree com Instagram e Facebook linkados.',status:'nao-contatado',site:'https://linktr.ee/camaraovilas',maps:'https://maps.google.com/?cid=4300696539975391504'},
  {id:5,nicho:'restaurante',name:'Oscarito Restaurant',phone:'(71) 4113-1306',rating:4.5,reviews:1097,addr:'Al. Praia do Tubarão, QA12 - Vilas',priority:'P2',website:false,obs:'Churrasco e buffet. Bom volume.',status:'nao-contatado',maps:'https://maps.google.com/?cid=2732622065490968672'},
  {id:6,nicho:'estetica',name:'BellaClin Vilas',phone:'(71) 3508-5704',rating:4.8,reviews:29,addr:'R. Itagi, 599 Ed. Mediterrâneo - Pitangueiras',priority:'P1',website:true,obs:'Medicina estética. Nicho de ticket alto. Ativo digitalmente.',status:'nao-contatado',site:'https://dietadetox1000.blogspot.com',maps:'https://maps.google.com/?cid=8820280970661337207'},
  {id:7,nicho:'estetica',name:'Royal Face Clínica',phone:'(71) 98433-2665',rating:4.7,reviews:40,addr:'Av. Praia de Itapuã, 805 - Vilas',priority:'P1',website:true,obs:'Franquia com site próprio. Potencial de escalar campanhas.',status:'nao-contatado',site:'https://royalface.com.br/unidade/lauro-de-freitas-ba/',maps:'https://maps.google.com/?cid=5118448392387256726'},
  {id:8,nicho:'estetica',name:'Prime S Clinic',phone:'(71) 99169-0380',rating:5.0,reviews:11,addr:'Av. Luiz Tarquínio Pontes, 2580 - Buraquinho',priority:'P2',website:false,obs:'5 estrelas. Pequena mas qualidade alta.',status:'nao-contatado',maps:'https://maps.google.com/?cid=15909270210003247780'},
  {id:9,nicho:'estetica',name:'Clínica Angellis',phone:'(71) 99988-5464',rating:5.0,reviews:5,addr:'Estação Villas Shopping - Av. Priscila Dutra, 389',priority:'P2',website:false,obs:'Nova, 5 estrelas, boa localização no shopping.',status:'nao-contatado',maps:'https://maps.google.com/?cid=7448861896042751287'},
  {id:10,nicho:'estetica',name:'Revitalle Clinic',phone:'(71) 3024-3935',rating:4.3,reviews:29,addr:'Av. Praia de Itapuã, 381 - Vilas',priority:'P3',website:false,obs:'Reviews mistas. Precisam melhorar presença online.',status:'nao-contatado',maps:'https://maps.google.com/?cid=2402224636865959270'},
  {id:11,nicho:'saude',name:'Bem Sorriso Implantes',phone:'(71) 3015-5484',rating:5.0,reviews:309,addr:'Av. Praia de Itapuã, 319 - Vilas',priority:'P1',website:true,obs:'309 reviews, 5 estrelas! Tem site clinicabemsorriso.com.br e Instagram @bemsorrisovilas.',status:'nao-contatado',instagram:'https://instagram.com/bemsorrisovilas',site:'https://clinicabemsorriso.com.br/vilas-do-atlantico/',maps:'https://maps.google.com/?cid=5571092489970760103'},
  {id:12,nicho:'saude',name:'Dentare Clínica Odontológica',phone:'(71) 99212-0622',rating:5.0,reviews:167,addr:'Av. Praia de Itapuã, 1670 - Vilas',priority:'P1',website:true,obs:'Implantes + aparelhos. 5 estrelas. Tem Facebook e site.',status:'nao-contatado',site:'https://www.facebook.com/dentareodonto/',maps:'https://maps.google.com/?cid=14430778771240994664'},
  {id:13,nicho:'saude',name:'Villas Dental Clinic',phone:'(71) 3369-0414',rating:4.9,reviews:123,addr:'Av. Praia de Itapuã, 408 - Vilas',priority:'P1',website:true,obs:'Tem site próprio villasdental.com.br com tour 360°. Alta tecnologia.',status:'nao-contatado',site:'https://villasdental.com.br/',maps:'https://maps.google.com/?cid=5118448392387256726'},
  {id:14,nicho:'saude',name:'Jeice Lima Nutricionista',phone:'(71) 98403-0485',rating:5.0,reviews:182,addr:'Av. Luiz Tarquínio Pontes, 2580 - Buraquinho',priority:'P1',website:false,obs:'182 reviews! Forte presença no Instagram com desafios e conteúdo. Excelente para escalar.',status:'nao-contatado',instagram:'https://instagram.com/nutrijeicelima',maps:'https://maps.google.com/?cid=8820280970661337207'},
  {id:15,nicho:'saude',name:'Michelle Guerra Nutricionista',phone:'(71) 98159-8999',rating:5.0,reviews:15,addr:'R. Praia de Ondina, 50 - Vilas',priority:'P2',website:false,obs:'Excelentes avaliações. Boa para campanhas de captação de pacientes.',status:'nao-contatado',maps:'https://maps.google.com/?cid=5571092489970760103'},
  {id:16,nicho:'saude',name:'Infinity Odonto Vilas',phone:'(71) 98882-3474',rating:4.9,reviews:29,addr:'Av. Luiz Tarquínio Pontes, 2580 - Vilas',priority:'P2',website:false,obs:'Clareamento dental em destaque nas avaliações.',status:'nao-contatado',maps:'https://maps.google.com/?cid=2179164227317637632'},
  {id:17,nicho:'saude',name:'Nutricionista Cyntia Câmara',phone:'(71) 99919-4915',rating:5.0,reviews:5,addr:'Av. Praia de Itapuã, 1686 - Vilas',priority:'P2',website:false,obs:'Nutrição integrativa + acupuntura. Ticket diferenciado.',status:'nao-contatado',maps:'https://maps.google.com/?cid=14430778771240994664'},
  {id:18,nicho:'academia',name:'Studio Kore - Funcional',phone:'(71) 99152-5662',rating:4.8,reviews:47,addr:'Av. Praia de Itapuã, 1808 - Vilas',priority:'P1',website:true,obs:'Studio premium. Franquia com 87K seguidores no IG nacional.',status:'nao-contatado',instagram:'https://instagram.com/kore.bahia.vilasdoatlantico',site:'https://studiokore.com.br/',maps:'https://maps.google.com/?cid=14430778771240994664'},
  {id:19,nicho:'academia',name:'Academia Vilas Fitness',phone:'(71) 99907-7895',rating:4.7,reviews:180,addr:'R. Praia de Ondina, 50 - Vilas',priority:'P1',website:true,obs:'Academia grande. 180 reviews. Instagram @academiavilasfitness_. Espaço kids = diferencial.',status:'nao-contatado',instagram:'https://instagram.com/academiavilasfitness_',site:'https://www.academiavilasfitness.com/home/',maps:'https://maps.google.com/?cid=5571092489970760103'},
  {id:20,nicho:'academia',name:'Rede Fluir - Vilas',phone:'(71) 3024-3021',rating:4.8,reviews:82,addr:'Av. Priscila Dutra, S/N - Buraquinho',priority:'P2',website:false,obs:'Fisioterapia + fitness. Ticket recorrente alto.',status:'nao-contatado',maps:'https://maps.google.com/?cid=15909270210003247780'},
  {id:21,nicho:'salao',name:'Villas Coiffeur',phone:'(71) 3508-0796',rating:4.7,reviews:107,addr:'Av. Priscila Dutra, 389 - Buraquinho',priority:'P1',website:false,obs:'107 reviews. Público feminino premium. Presença no Instagram.',status:'nao-contatado',instagram:'https://instagram.com/villascoiffeurcentrodebeleza',maps:'https://maps.google.com/?cid=6316088598018556811'},
  {id:22,nicho:'salao',name:'Estação de Beleza Vilas',phone:'(71) 3289-4070',rating:4.7,reviews:85,addr:'R. Praia de Pajussara, 348 - Vilas',priority:'P1',website:false,obs:'85 reviews. Tem Instagram ativo @estacaodebelezavilas. Salão completo.',status:'nao-contatado',instagram:'https://instagram.com/estacaodebelezavilas',maps:'https://maps.google.com/?cid=10381152542829611920'},
  {id:23,nicho:'salao',name:'Palazzo Spazio di Belleza',phone:'(71) 3287-1357',rating:4.5,reviews:141,addr:'Av. Praia de Itapuã, 571 - Vilas',priority:'P2',website:false,obs:'141 reviews. Atendimento VIP conforme avaliações.',status:'nao-contatado',maps:'https://maps.google.com/?cid=18005118390911426139'},
  {id:24,nicho:'salao',name:'Rosenildes Mendes Cabeleireira',phone:'(71) 3251-9153',rating:4.6,reviews:105,addr:'Av. Praia de Itapuã, 1861 - Vilas',priority:'P2',website:false,obs:'Especialista em loiras. Clientela fiel.',status:'nao-contatado',maps:'https://maps.google.com/?cid=6016212904337810409'},
  {id:25,nicho:'salao',name:'Lu Castro Studio de Beleza',phone:'(71) 99317-3415',rating:4.7,reviews:48,addr:'Av. Luiz Tarquínio Pontes, 2318 - Vilas',priority:'P2',website:false,obs:'Avaliações mistas. Potencial de melhora com tráfego + reputação.',status:'nao-contatado',maps:'https://maps.google.com/?cid=15909270210003247780'},
  {id:26,nicho:'pet',name:'Veterinary Clinic Vilas do Atlântico',phone:'(71) 3379-0092',rating:4.8,reviews:170,addr:'R. Praia do Mucuripe, 26 - Vilas',priority:'P1',website:false,obs:'170 reviews, 4.8. Nicho pet com ticket recorrente alto.',status:'nao-contatado',maps:'https://maps.google.com/?cid=14430778771240994664'},
  {id:27,nicho:'pet',name:'Pettep',phone:'(71) 99695-7413',rating:4.8,reviews:50,addr:'Av. Praia de Itapuã, 374 - Vilas',priority:'P1',website:false,obs:'Pet shop + clínica. 4.8 estrelas. 11K seguidores no IG @pettepbahia.',status:'nao-contatado',instagram:'https://instagram.com/pettepbahia',maps:'https://maps.google.com/?cid=5571092489970760103'},
  {id:28,nicho:'pet',name:'Pet Vilas',phone:'(71) 99295-0648',rating:4.6,reviews:233,addr:'R. Ana C. B. Dias - Miragem',priority:'P2',website:false,obs:'233 reviews. Volume alto. Reviews mistas — oportunidade de posicionamento.',status:'nao-contatado',maps:'https://maps.google.com/?cid=2402224636865959270'},
  {id:29,nicho:'pet',name:'Dr. Zoo & Cia Veterinária 24h',phone:'(71) 98796-5529',rating:4.3,reviews:267,addr:'R. Praia de Pajussara, 106 - Vilas',priority:'P2',website:false,obs:'24h. Alto volume mas avaliações variadas.',status:'nao-contatado',maps:'https://maps.google.com/?cid=6016212904337810409'},
  {id:30,nicho:'imoveis',name:'Silvia Porto Imóveis',phone:'(71) 99675-8989',rating:4.8,reviews:24,addr:'Av. Praia de Itapuã, 48 - Vilas',priority:'P1',website:false,obs:'Corretora individual. Tráfego pago para captação de leads imob.',status:'nao-contatado',maps:'https://maps.google.com/?cid=14430778771240994664'},
  {id:31,nicho:'imoveis',name:'Linnda Imobiliária',phone:'(71) 99969-3434',rating:4.3,reviews:15,addr:'Av. Praia de Itapuã, 1067 - Vilas',priority:'P2',website:false,obs:'Imobiliária local. Ticket alto por transação.',status:'nao-contatado',maps:'https://maps.google.com/?cid=5571092489970760103'},
  {id:32,nicho:'imoveis',name:'Tadeu Carvalho Corretor',phone:'(71) 99185-1348',rating:4.0,reviews:4,addr:'R. Praia de Itapema - Vilas',priority:'P2',website:false,obs:'Corretor individual. Pode investir em leads qualificados.',status:'nao-contatado',maps:'https://maps.google.com/?cid=6016212904337810409'},
  {id:33,nicho:'educacao',name:'Badermann Escola de Música',phone:'(71) 99272-9658',rating:5.0,reviews:202,addr:'Shopping Villas Boulevard - Av. Praia de Itapuã, 1137',priority:'P1',website:false,obs:'5 estrelas, 202 reviews! Forte Instagram @badermann.musica.',status:'nao-contatado',instagram:'https://instagram.com/badermann.musica',maps:'https://maps.google.com/?cid=7448861896042751287'},
  {id:34,nicho:'educacao',name:'Kidsland Creche Escola',phone:'(71) 99608-1136',rating:5.0,reviews:64,addr:'R. Maria dos Réis Silva, 312 - Miragem',priority:'P1',website:false,obs:'5 estrelas. Escola infantil premium. 5.3K seguidores @kidslandvilas.',status:'nao-contatado',instagram:'https://instagram.com/kidslandvilas',maps:'https://maps.google.com/?cid=14430778771240994664'},
  {id:35,nicho:'educacao',name:'Vilas Cursos (Number One)',phone:'—',rating:4.8,reviews:31,addr:'Av. Praia de Pajussara, 294 - Vilas',priority:'P2',website:false,obs:'Franquia de inglês. Anúncios para matrículas.',status:'nao-contatado',maps:'https://maps.google.com/?cid=5571092489970760103'},
  {id:36,nicho:'educacao',name:'Escola Lápis Vilas',phone:'(71) 98430-6639',rating:4.8,reviews:19,addr:'R. Maria dos Réis Silva, 152 - Miragem',priority:'P2',website:false,obs:'Berçário e Fundamental. Boa estrutura pedagógica.',status:'nao-contatado',maps:'https://maps.google.com/?cid=6316088598018556811'},
  {id:37,nicho:'moda',name:'MSTORE BA',phone:'(71) 99607-1116',rating:5.0,reviews:15,addr:'Av. Praia de Itapuã, 7 - Vilas',priority:'P1',website:false,obs:'Moda masculina premium. 5 estrelas. Instagram ativo.',status:'nao-contatado',maps:'https://maps.google.com/?cid=2179164227317637632'},
  {id:38,nicho:'moda',name:"Loja Oyá Let'sGo",phone:'(71) 99677-9492',rating:4.9,reviews:11,addr:'Av. Praia de Itapuã, 935 - Vilas',priority:'P1',website:false,obs:'Moda feminina. 4.9 estrelas. Peças exclusivas.',status:'nao-contatado',maps:'https://maps.google.com/?cid=6016212904337810409'},
  {id:39,nicho:'moda',name:'Vivi Moda Íntima',phone:'(71) 98349-6325',rating:4.8,reviews:13,addr:'Av. Praia de Itapuã, 248 - Vilas',priority:'P2',website:false,obs:'Lingerie. Cliente fiel conforme reviews.',status:'nao-contatado',maps:'https://maps.google.com/?cid=18005118390911426139'},
  {id:40,nicho:'juridico',name:'Alvarez & Borba Advocacia',phone:'(71) 99333-7181',rating:5.0,reviews:39,addr:'Empresarial Atlântico - R. Itagi - Vilas',priority:'P1',website:false,obs:'Especialidade digital: recuperação de contas Instagram/TikTok. Público nichado.',status:'nao-contatado',maps:'https://maps.google.com/?cid=5118448392387256726'},
  {id:41,nicho:'juridico',name:'Tatiane Costa Advocacia',phone:'(71) 99621-4242',rating:5.0,reviews:51,addr:'R. Praia de Pajussara, 294 - Vilas',priority:'P1',website:false,obs:'51 reviews, 5 estrelas. Advocacia consumerista. Tráfego para captação.',status:'nao-contatado',maps:'https://maps.google.com/?cid=14430778771240994664'},
  {id:42,nicho:'juridico',name:'Carvalho Advocacia',phone:'(71) 99184-7649',rating:5.0,reviews:11,addr:'Estr. Min. Antônio Carlos Magalhães, 447 - Buraquinho',priority:'P2',website:false,obs:'Família e patrimonial. Bom ticket médio.',status:'nao-contatado',maps:'https://maps.google.com/?cid=6316088598018556811'}
];

// ── Planilha ─────────────────────────────────────────────────

function getOrCreateSpreadsheet() {
  var props = PropertiesService.getScriptProperties();
  var ssId = props.getProperty('SS_ID');
  if (ssId) {
    try { return SpreadsheetApp.openById(ssId); } catch(e) {}
  }
  var ss = SpreadsheetApp.create('Dashboard Prospecção Vilas');
  props.setProperty('SS_ID', ss.getId());
  var leadsSheet = ss.getSheets()[0];
  leadsSheet.setName('Leads');
  leadsSheet.appendRow(LEADS_HEADERS);
  var histSheet = ss.insertSheet('Histórico');
  histSheet.appendRow(HISTORY_HEADERS);
  seedLeads(leadsSheet);
  return ss;
}

function seedLeads(sheet) {
  var now = new Date().toISOString();
  var rows = SEED_LEADS.map(function(l) {
    return [
      l.id, l.nicho, l.name, l.phone||'', l.addr||'',
      l.rating||0, l.reviews||0, l.priority, l.status, l.obs||'',
      l.website ? 1 : 0,
      l.instagram||'', l.site||'', l.maps||'',
      l.status, l.priority, '', now
    ];
  });
  sheet.getRange(2, 1, rows.length, LEADS_HEADERS.length).setValues(rows);
}

// ── Resposta com CORS ────────────────────────────────────────

function jsonResponse(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

// ── GET ──────────────────────────────────────────────────────

function doGet(e) {
  var action = e.parameter.action || 'leads';
  var ss = getOrCreateSpreadsheet();

  if (action === 'leads') {
    return jsonResponse(getLeads(ss));
  }
  if (action === 'history') {
    var limit = parseInt(e.parameter.limit || '30', 10);
    return jsonResponse(getHistory(ss, limit));
  }
  return jsonResponse({error: 'ação desconhecida'});
}

// ── POST ─────────────────────────────────────────────────────

function doPost(e) {
  var body = JSON.parse(e.postData.contents);
  var ss = getOrCreateSpreadsheet();

  if (body.action === 'update') {
    return jsonResponse(updateLead(ss, body));
  }
  return jsonResponse({error: 'ação desconhecida'});
}

// ── Lógica de leads ──────────────────────────────────────────

function getLeads(ss) {
  var sheet = ss.getSheetByName('Leads');
  var data = sheet.getDataRange().getValues();
  var headers = data[0];
  return data.slice(1).map(function(row) {
    var obj = {};
    headers.forEach(function(h, i) { obj[h] = row[i]; });
    return {
      id: Number(obj.id),
      nicho: obj.nicho,
      name: obj.name,
      phone: obj.phone,
      addr: obj.addr,
      rating: Number(obj.rating),
      reviews: Number(obj.reviews),
      priority: obj.priority,
      status: obj.status,
      obs: obj.obs,
      website: obj.website == 1,
      instagram: obj.instagram || null,
      site: obj.site || null,
      maps: obj.maps || null,
      customStatus: obj.customStatus || obj.status,
      customPriority: obj.customPriority || obj.priority,
      customObs: obj.customObs || ''
    };
  });
}

function updateLead(ss, body) {
  var sheet = ss.getSheetByName('Leads');
  var histSheet = ss.getSheetByName('Histórico');
  var data = sheet.getDataRange().getValues();
  var headers = data[0];

  var colMap = {};
  headers.forEach(function(h, i) { colMap[h] = i; });

  var rowIdx = -1;
  for (var i = 1; i < data.length; i++) {
    if (Number(data[i][colMap['id']]) === Number(body.id)) {
      rowIdx = i;
      break;
    }
  }
  if (rowIdx === -1) return {error: 'Lead não encontrado'};

  var row = data[rowIdx];
  var sheetRow = rowIdx + 1; // 1-based
  var now = new Date().toISOString();

  var fieldMap = [
    ['customStatus',   'status'],
    ['customPriority', 'prioridade'],
    ['customObs',      'anotação']
  ];

  var histData = histSheet.getDataRange().getValues();
  var nextHistId = histData.length;

  fieldMap.forEach(function(pair) {
    var field = pair[0], label = pair[1];
    if (body[field] === undefined || body[field] === null) return;
    var oldVal = String(row[colMap[field]] || '');
    var newVal = String(body[field]);
    if (oldVal !== newVal) {
      histSheet.appendRow([nextHistId++, body.id, row[colMap['name']], label, oldVal, newVal, now]);
    }
    sheet.getRange(sheetRow, colMap[field] + 1).setValue(newVal);
  });

  sheet.getRange(sheetRow, colMap['updated_at'] + 1).setValue(now);

  return {
    id: Number(body.id),
    customStatus:   body.customStatus   !== undefined ? body.customStatus   : row[colMap['customStatus']],
    customPriority: body.customPriority !== undefined ? body.customPriority : row[colMap['customPriority']],
    customObs:      body.customObs      !== undefined ? body.customObs      : row[colMap['customObs']]
  };
}

// ── Histórico ────────────────────────────────────────────────

function getHistory(ss, limit) {
  var sheet = ss.getSheetByName('Histórico');
  var data = sheet.getDataRange().getValues();
  if (data.length <= 1) return [];
  var headers = data[0];
  var records = data.slice(1).map(function(row) {
    var obj = {};
    headers.forEach(function(h, i) { obj[h] = row[i]; });
    return obj;
  });
  records.sort(function(a, b) { return b.changed_at > a.changed_at ? 1 : -1; });
  return records.slice(0, limit);
}
