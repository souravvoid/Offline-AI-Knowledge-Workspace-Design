# Security Document

## Security Model

Khoji is a **local-first, offline application**. The security model prioritizes:
1. **Data sovereignty** — All data stays on the user's device
2. **Safe parsing** — Document parsers are sandboxed against malicious files
3. **Plugin isolation** — Third-party plugins run in restricted environments
4. **No telemetry** — No data is sent anywhere without explicit user consent
5. **Defense in depth** — Multiple layers of protection at every level

---

## 1. Data Storage Security

### Encryption at Rest

| Data Type | Encryption | Mechanism |
|-----------|-----------|-----------|
| Document files | Optional AES-256-GCM | User-provided passphrase |
| SQLite database | Optional (SQLite Encryption Extension) | Same passphrase |
| AI models | No encryption (public models) | N/A |
| User settings | No encryption (local-only assumption) | File permissions |

### File Permissions

```
~/.khoji/          rwx------ (0700)
~/.khoji/db/       rwx------ (0700)
~/.khoji/documents/ rwx------ (0700)
~/.khoji/models/   rwx------ (0700)
```

---

## 2. Document Parsing Security

### Parser Isolation

| Parser | Sandbox | Strategy |
|--------|---------|----------|
| PDF (pdf-extract) | OS process | Fork + seccomp filter |
| PDF (pdf.js) | WASM sandbox | Memory-safe |
| Image (image-rs) | Rust memory safety | No unsafe code |
| PPT/DOCX/EPUB | OS process | Timeout + memory limit |

### PDF Bomb Protection

```
MAX_FILE_SIZE:    200MB
MAX_PAGES:        1000
MAX_OBJECTS:      100000
PARSE_TIMEOUT:    30s
```

### Path Traversal Protection

All file paths are canonicalized and validated against an allowlist before any read/write operation.

---

## 3. Plugin Security

### WASM Plugin Sandbox (wasmtime)
- No filesystem access (unless explicitly granted)
- No network access
- No process spawning
- Memory limit: 256MB
- CPU limit: 2 cores
- Timeout: 30s per operation

### Native Plugin Sandbox (OS-level)
- Seccomp (Linux) / Seatbelt (macOS) / AppContainer (Windows)
- No direct filesystem (uses host-provided API)
- No network unless permission granted

### Permission System

Each plugin declares capabilities in its manifest. User must approve:

```
filesystem:read               Low risk    Default: Grant
filesystem:write              Medium      Default: Ask
network:connect               High        Default: Ask
process:spawn                 Critical    Default: Deny
clipboard:read                Medium      Default: Ask
document:read_full_text       Medium      Default: Ask
```

---

## 4. AI Model Security

- All models downloaded from official Hugging Face repositories
- SHA256 checksums are hardcoded and verified before loading
- Models are data files loaded by safe runtimes — never executed as code

### Prompt Injection Defense

```
1. Strip system prompt escape sequences from user input
2. Separate system, context, and user message sections
3. Truncate user input to 4000 chars max
4. Never concatenate user input into system prompt directly
```

---

## 5. Network Security

Khoji is **offline by default**. Network access is limited to:

| Operation | Network Required | User Control |
|-----------|-----------------|--------------|
| Model download | Yes | Explicit action |
| Plugin download | Yes | Explicit action |
| Updates check | Optional | Configurable |
| Core AI features | No | Always offline |
| Telemetry | No | Always disabled |

---

## 6. Privacy Model

| Data Type | Collected | Purpose |
|-----------|-----------|---------|
| Usage statistics | Never | — |
| Document content | Never | — |
| AI model usage | Never | — |
| Error reports | Opt-in only | Crash debugging (no personal data) |
| Analytics | Never | — |
| User identity | Never | — |

---

## 7. Security Checklist

| Check | Status |
|-------|--------|
| No hardcoded secrets | ✅ |
| Input sanitization | ✅ |
| Path traversal protection | ✅ |
| PDF bomb protection | ✅ |
| Plugin sandboxing | ✅ |
| Permission system | ✅ |
| Model verification (SHA256) | ✅ |
| No eval() or dynamic code | ✅ |
| Memory safety (Rust) | ✅ |
| Safe defaults | ✅ |
| Prompt injection defense | ✅ |
