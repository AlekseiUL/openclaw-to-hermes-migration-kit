# Базы данных, память и хранилища при миграции OpenClaw → Hermes

## Главное правило

Базы и память нельзя “просто скопировать в Hermes”. Надо сначала понять тип хранилища, назначение и риск.

Правильный порядок:

```text
inventory → backup → read-only validation → mapping → import/rebuild/archive → smoke test → rollback plan
```

## Какие хранилища бывают

### 1. Config/state databases

Это внутреннее состояние OpenClaw: настройки, registry, статусы, dashboard/gateway state.

Решение:

- не переносить как активную базу в Hermes;
- извлечь только нужные настройки;
- сохранить оригинал как архив;
- создать Hermes config/profile заново.

### 2. Sessions / conversation history

Обычно JSONL, SQLite или набор файлов.

Решение:

- не заливать всё в активную память;
- сохранить как `legacy-openclaw-sessions/`;
- сделать короткий summary для будущего агента;
- приватные/финансовые/психологические sessions не индексировать без отдельного согласия.

### 3. Memory databases

Это долговременная память, embedding/vector storage, sqlite-vec, Chroma, FAISS, LanceDB, Qdrant и похожие штуки.

Решение:

- сначала inventory: формат, размер, коллекции/таблицы, embedding provider, metadata;
- документы лучше импортировать как readable notes/references;
- embeddings лучше **перестроить** в Hermes, а не копировать бинарный vector index вслепую;
- если source memory содержит raw private data - только private/profile-local import.

### 4. Tool/application databases

Например локальная база финучёта, CRM export, research cache, Notion/Airtable mirror, SQLite приложения.

Решение:

- не считать это “памятью агента” автоматически;
- описать владельца и назначение;
- перенести connector/tool config;
- перенести данные только если агент реально должен их читать;
- для внешних баз PostgreSQL/MySQL/Supabase лучше переносить connection instructions, а не dump.

### 5. Flat files

CSV, JSON, JSONL, Parquet, Markdown, PDF, media.

Решение:

- классифицировать: active knowledge / archive / private / ignore;
- проверить encoding;
- убрать секреты;
- создать index/references уже в Hermes.

## Что делает kit

Скрипт:

```bash
python3 scripts/database_inventory.py --source ~/.openclaw --out ./database-inventory.json
```

Он работает read-only и собирает:

- путь;
- тип;
- размер;
- SQLite quick_check и список таблиц без чтения строк;
- количество JSONL lines без чтения содержания;
- признаки vector/index directories;
- рекомендации по migration action.

Он не печатает содержимое строк, сообщений, документов и ключей.

## Decision matrix

### Copy as archive

Использовать для:

- raw sessions;
- старых DB, нужных только для rollback/reference;
- неизвестных бинарных индексов.

### Import as knowledge

Использовать для:

- чистых Markdown/reference docs;
- публичных или разрешённых заметок;
- agent role knowledge.

### Rebuild in Hermes

Использовать для:

- vector indexes;
- memory embeddings;
- search indexes;
- generated caches.

### Reconnect, not copy

Использовать для:

- PostgreSQL;
- MySQL;
- Supabase;
- Notion;
- Airtable;
- Google Sheets;
- external APIs.

### Skip/quarantine

Использовать для:

- секретных DB;
- повреждённых DB;
- неизвестных бинарных форматов;
- приватных sessions без согласия;
- старых cache/index files, которые можно пересобрать.

## Проверки перед переносом

Для SQLite:

```bash
sqlite3 <file.db> 'PRAGMA quick_check;'
sqlite3 <file.db> '.tables'
```

Для больших JSONL:

```bash
wc -l <file.jsonl>
```

Для vector DB:

- определить engine;
- найти original documents, если есть;
- проверить embedding model/provider;
- решить: rebuild, not copy.

## Что должно попасть в финальный отчёт

```text
Storage: sessions.sqlite
Type: sqlite
Size: 124 MB
Purpose: OpenClaw sessions
Action: archive + summarize, not direct import
Private risk: medium
Verification: quick_check ok
Rollback: original file preserved
```

## Что нельзя делать

- Нельзя писать прямо в Hermes internal DB без documented import path.
- Нельзя копировать vector index и считать, что память “перешла”.
- Нельзя индексировать raw private sessions по умолчанию.
- Нельзя переносить external DB credentials в отчёт.
- Нельзя удалять source DB после миграции. Сначала период наблюдения.

## Безопасная формула

```text
Raw DB stays archived.
Readable knowledge gets converted to files/notes.
Embeddings/search indexes get rebuilt.
External databases get reconnected.
Private data stays private.
```
