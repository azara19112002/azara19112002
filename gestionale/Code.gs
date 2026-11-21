/**
 * Li Fòli – Gestionale
 * Backend Google Apps Script. I dati vivono in un Google Sheet nel vostro Drive,
 * gli allegati in una cartella Drive. Vedi ISTRUZIONI.md per l'installazione.
 */

var APP_NAME = 'Li Fòli · Gestionale';
var ROOT_FOLDER_NAME = 'Li Fòli – Gestionale';

// Permessi per ruolo: 'rw' = lettura e scrittura, 'r' = sola lettura. Moduli assenti = nessun accesso.
var PERMS = {
  admin: {
    prenotazioni: 'rw', camere: 'rw', stagioni: 'rw', pulizie: 'rw', movimenti: 'rw', fatture: 'rw',
    finanziamenti: 'rw', scadenze: 'rw', documenti: 'rw', impostazioni: 'rw', utenti: 'rw', log: 'r'
  },
  socio: {
    prenotazioni: 'rw', camere: 'rw', stagioni: 'rw', pulizie: 'rw', movimenti: 'rw', fatture: 'rw',
    finanziamenti: 'rw', scadenze: 'rw', documenti: 'rw', impostazioni: 'rw', log: 'r'
  },
  collaboratore: {
    prenotazioni: 'r', camere: 'r', stagioni: 'r', pulizie: 'rw', impostazioni: 'r'
  },
  contabile: {
    movimenti: 'r', fatture: 'r', finanziamenti: 'r', scadenze: 'r', documenti: 'r', impostazioni: 'r',
    prenotazioni: 'r', camere: 'r', stagioni: 'r'
  }
};

// Ruoli che ricevono l'accesso in modifica al foglio dati (necessario per salvare)
var EDITOR_ROLES = ['admin', 'socio', 'collaboratore'];

/* ------------------------------------------------------------------ */
/*  Web app                                                            */
/* ------------------------------------------------------------------ */

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle(APP_NAME)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/* ------------------------------------------------------------------ */
/*  Installazione (eseguire UNA volta dall'editor: funzione "setup")   */
/* ------------------------------------------------------------------ */

function setup() {
  var props = PropertiesService.getScriptProperties();
  var me = Session.getEffectiveUser().getEmail();

  var root;
  if (props.getProperty('FOLDER_ID')) {
    root = DriveApp.getFolderById(props.getProperty('FOLDER_ID'));
  } else {
    root = DriveApp.createFolder(ROOT_FOLDER_NAME);
    root.createFolder('Allegati');
    props.setProperty('FOLDER_ID', root.getId());
  }

  var ss;
  if (props.getProperty('SHEET_ID')) {
    ss = SpreadsheetApp.openById(props.getProperty('SHEET_ID'));
  } else {
    ss = SpreadsheetApp.create('Li Fòli – Dati gestionale');
    DriveApp.getFileById(ss.getId()).moveTo(root);
    props.setProperty('SHEET_ID', ss.getId());
  }

  var users = readAll_(ss, 'utenti');
  if (!users.some(function (u) { return lc_(u.email) === lc_(me); })) {
    writeRecord_(ss, 'utenti', { id: newId_(), email: me, nome: 'Amministratore', ruolo: 'admin', attivo: 'si' }, me);
  }

  // Promemoria giornaliero alle 8 (scadenze, fatture, arrivi, pulizie)
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'sendReminders') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('sendReminders').timeBased().everyDays(1).atHour(8).inTimezone('Europe/Rome').create();

  Logger.log('Installazione completata.\nFoglio dati: ' + ss.getUrl() + '\nCartella: ' + root.getUrl());
}

/* ------------------------------------------------------------------ */
/*  API chiamate dalla pagina                                          */
/* ------------------------------------------------------------------ */

function bootstrap() {
  var ctx = ctx_();
  var data = {};
  Object.keys(ctx.perms).forEach(function (m) {
    data[m] = readAll_(ctx.ss, m);
    if (m === 'log') data[m] = data[m].slice(-300);
  });
  var team = readAll_(ctx.ss, 'utenti')
    .filter(function (u) { return u.attivo !== 'no'; })
    .map(function (u) { return { email: u.email, nome: u.nome, ruolo: u.ruolo }; });
  return {
    user: { email: ctx.user.email, nome: ctx.user.nome, ruolo: ctx.user.ruolo },
    perms: ctx.perms,
    data: data,
    team: team,
    sheetUrl: ctx.user.ruolo === 'admin' ? ctx.ss.getUrl() : ''
  };
}

function saveRecord(module, record) {
  var ctx = ctx_();
  need_(ctx, module, 'rw');
  if (!record || typeof record !== 'object') throw new Error('Dati non validi');
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var isNew = !record.id;
    if (isNew) { record.id = newId_(); record.creato_il = nowIso_(); record.creato_da = ctx.user.email; }
    record.modificato_il = nowIso_();
    record.modificato_da = ctx.user.email;
    if (module === 'utenti') prepareUser_(ctx, record);
    writeRecord_(ctx.ss, module, record, ctx.user.email);
    log_(ctx, isNew ? 'crea' : 'modifica', module, record);
    return record;
  } finally {
    lock.releaseLock();
  }
}

function deleteRecord(module, id) {
  var ctx = ctx_();
  need_(ctx, module, 'rw');
  if (module === 'utenti' && id === ctx.user.id) throw new Error('Non puoi eliminare il tuo stesso utente');
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var sh = ctx.ss.getSheetByName(module);
    if (!sh) return false;
    var values = sh.getDataRange().getValues();
    var idCol = values[0].indexOf('id');
    for (var i = 1; i < values.length; i++) {
      if (String(values[i][idCol]) === String(id)) {
        var rec = rowToObj_(values[0], values[i]);
        sh.deleteRow(i + 1);
        log_(ctx, 'elimina', module, rec);
        return true;
      }
    }
    return false;
  } finally {
    lock.releaseLock();
  }
}

/** Carica un allegato nella cartella Drive del modulo. Restituisce {n: nome, u: url}. */
function uploadFile(module, fileName, mimeType, base64) {
  var ctx = ctx_();
  need_(ctx, module, 'rw');
  var root = DriveApp.getFolderById(prop_('FOLDER_ID'));
  var allegati = sub_(root, 'Allegati');
  var folder = sub_(allegati, module);
  var blob = Utilities.newBlob(Utilities.base64Decode(base64), mimeType || 'application/octet-stream', fileName);
  var file = folder.createFile(blob);
  log_(ctx, 'allegato', module, { id: file.getId(), titolo: fileName });
  return { n: fileName, u: file.getUrl() };
}

/* ------------------------------------------------------------------ */
/*  Promemoria email giornalieri                                       */
/* ------------------------------------------------------------------ */

function sendReminders() {
  var ss = SpreadsheetApp.openById(prop_('SHEET_ID'));
  var today = isoDate_(new Date());
  var items = [];

  readAll_(ss, 'scadenze').forEach(function (s) {
    if (s.stato === 'Fatto' || !s.data) return;
    var d = daysBetween_(today, s.data);
    var pre = Number(s.preavviso_giorni || 15);
    if (d < 0) items.push('🔴 SCADUTA da ' + (-d) + ' gg: ' + s.titolo + ' (' + fmtDate_(s.data) + ')' + money_(s.importo));
    else if (d <= pre) items.push('🟠 tra ' + d + ' gg: ' + s.titolo + ' (' + fmtDate_(s.data) + ')' + money_(s.importo));
  });
  readAll_(ss, 'fatture').forEach(function (f) {
    if (f.tipo !== 'Ricevuta' || f.stato === 'Pagata' || !f.scadenza_pagamento) return;
    var d = daysBetween_(today, f.scadenza_pagamento);
    if (d <= 7) items.push('🧾 Fattura ' + (f.numero || '') + ' ' + (f.controparte || '') + ' da pagare ' + (d < 0 ? '(scaduta)' : 'entro ' + fmtDate_(f.scadenza_pagamento)) + money_(f.totale));
  });
  var tomorrow = isoDate_(new Date(Date.now() + 864e5));
  readAll_(ss, 'prenotazioni').forEach(function (p) {
    if (p.stato === 'Cancellata') return;
    if (p.arrivo === today || p.arrivo === tomorrow) items.push('🛎️ Arrivo ' + (p.arrivo === today ? 'oggi' : 'domani') + ': ' + p.ospite + ' – ' + (p.camera || ''));
  });
  readAll_(ss, 'pulizie').forEach(function (p) {
    if (p.stato !== 'Fatto' && (p.data === today || p.data === tomorrow)) items.push('🧹 ' + p.tipo + ' ' + (p.camera || '') + ' – ' + (p.data === today ? 'oggi' : 'domani') + (p.assegnato_a ? ' (' + p.assegnato_a + ')' : ''));
  });

  if (!items.length) return;
  var to = readAll_(ss, 'utenti')
    .filter(function (u) { return u.attivo !== 'no' && (u.ruolo === 'admin' || u.ruolo === 'socio'); })
    .map(function (u) { return u.email; }).join(',');
  if (!to) return;
  MailApp.sendEmail({
    to: to,
    subject: 'Li Fòli – promemoria del ' + fmtDate_(today) + ' (' + items.length + ')',
    body: 'Buongiorno!\n\n' + items.join('\n') + '\n\nApri il gestionale: ' + ScriptApp.getService().getUrl()
  });
}

/* ------------------------------------------------------------------ */
/*  Interni                                                            */
/* ------------------------------------------------------------------ */

function ctx_() {
  var email = lc_(Session.getActiveUser().getEmail());
  if (!email) throw new Error('Accesso non riconosciuto: entra con l\'account Google autorizzato.');
  var ss = SpreadsheetApp.openById(prop_('SHEET_ID'));
  var user = readAll_(ss, 'utenti').filter(function (u) { return lc_(u.email) === email && u.attivo !== 'no'; })[0];
  if (!user) throw new Error('L\'account ' + email + ' non è abilitato. Chiedi all\'amministratore di aggiungerti.');
  var perms = PERMS[user.ruolo];
  if (!perms) throw new Error('Ruolo non valido: ' + user.ruolo);
  return { ss: ss, user: user, perms: perms };
}

function need_(ctx, module, level) {
  var p = ctx.perms[module];
  if (!p || (level === 'rw' && p !== 'rw')) throw new Error('Permesso negato per "' + module + '"');
}

function prepareUser_(ctx, rec) {
  rec.email = lc_(rec.email);
  if (!rec.email) throw new Error('Email obbligatoria');
  if (!PERMS[rec.ruolo]) throw new Error('Ruolo non valido');
  // Condivide automaticamente foglio dati e cartella allegati con il nuovo utente
  var file = DriveApp.getFileById(ctx.ss.getId());
  var folder = DriveApp.getFolderById(prop_('FOLDER_ID'));
  try {
    if (EDITOR_ROLES.indexOf(rec.ruolo) > -1) { file.addEditor(rec.email); folder.addEditor(rec.email); }
    else { file.addViewer(rec.email); folder.addViewer(rec.email); }
  } catch (e) {
    rec.note = (rec.note ? rec.note + ' · ' : '') + 'Condivisione non riuscita: ' + e.message;
  }
}

function sheet_(ss, name) {
  var sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    sh.getRange('A1').setValue('id');
    sh.getRange('A:ZZ').setNumberFormat('@'); // tutto come testo: niente conversioni automatiche di date
    sh.setFrozenRows(1);
  }
  return sh;
}

function readAll_(ss, name) {
  var sh = ss.getSheetByName(name);
  if (!sh || sh.getLastRow() < 2) return [];
  var values = sh.getDataRange().getValues();
  var head = values[0];
  var out = [];
  for (var i = 1; i < values.length; i++) {
    if (values[i].join('') === '') continue;
    out.push(rowToObj_(head, values[i]));
  }
  return out;
}

function rowToObj_(head, row) {
  var o = {};
  head.forEach(function (h, j) {
    if (!h) return;
    var v = row[j];
    if (v instanceof Date) v = isoDate_(v);
    o[h] = v === null || v === undefined ? '' : String(v);
  });
  return o;
}

function writeRecord_(ss, name, rec, who) {
  var sh = sheet_(ss, name);
  var lastCol = Math.max(sh.getLastColumn(), 1);
  var head = sh.getRange(1, 1, 1, lastCol).getValues()[0].map(String);
  var keys = Object.keys(rec);
  keys.forEach(function (k) {
    if (head.indexOf(k) === -1) { head.push(k); sh.getRange(1, head.length).setValue(k); }
  });
  var row = head.map(function (h) {
    var v = rec[h];
    if (v === null || v === undefined) return '';
    if (typeof v === 'object') return JSON.stringify(v);
    return String(v);
  });
  var idCol = head.indexOf('id');
  var n = sh.getLastRow();
  if (n >= 2) {
    var ids = sh.getRange(2, idCol + 1, n - 1, 1).getValues();
    for (var i = 0; i < ids.length; i++) {
      if (String(ids[i][0]) === String(rec.id)) {
        sh.getRange(i + 2, 1, 1, row.length).setValues([row]);
        return;
      }
    }
  }
  sh.getRange(n + 1, 1, 1, row.length).setValues([row]);
}

function log_(ctx, azione, module, rec) {
  var label = rec.titolo || rec.descrizione || rec.ospite || rec.nome || rec.numero || rec.email || rec.tipo || '';
  writeRecord_(ctx.ss, 'log', {
    id: newId_(), quando: nowIso_(), utente: ctx.user.email, azione: azione, modulo: module,
    record_id: rec.id || '', dettaglio: String(label).slice(0, 120)
  });
}

function sub_(parent, name) {
  var it = parent.getFoldersByName(name);
  return it.hasNext() ? it.next() : parent.createFolder(name);
}

function prop_(k) {
  var v = PropertiesService.getScriptProperties().getProperty(k);
  if (!v) throw new Error('Gestionale non installato: esegui la funzione "setup" dall\'editor.');
  return v;
}

function newId_() { return Utilities.getUuid().replace(/-/g, '').slice(0, 12); }
function lc_(s) { return String(s || '').trim().toLowerCase(); }
function nowIso_() { return Utilities.formatDate(new Date(), 'Europe/Rome', "yyyy-MM-dd'T'HH:mm:ss"); }
function isoDate_(d) { return Utilities.formatDate(d, 'Europe/Rome', 'yyyy-MM-dd'); }
function fmtDate_(iso) { var p = String(iso).split('-'); return p.length === 3 ? p[2] + '/' + p[1] + '/' + p[0] : iso; }
function daysBetween_(a, b) { return Math.round((Date.parse(b + 'T12:00:00Z') - Date.parse(a + 'T12:00:00Z')) / 864e5); }
function money_(v) { return v ? ' – € ' + Number(v).toFixed(2).replace('.', ',') : ''; }
