# Testing Strategy

---

## Test Pyramid

```
          ╱╲
         ╱  ╲
        ╱ E2E╲              < 10 tests (critical user flows)
       ╱──────╲
      ╱Integration╲          < 50 tests (API + pipeline)
     ╱────────────╲
    ╱   Unit Tests  ╲        < 200+ tests (components, utils)
   ╱────────────────╲
  ╱   Static Analysis  ╲     TypeScript strict + Clippy + Ruff
 ╱──────────────────────╲
```

---

## 1. Static Analysis

### Frontend (TypeScript/React)
```bash
# Type checking
tsc --strict --noEmit

# Linting
eslint src/ --ext .ts,.tsx --max-warnings 0

# Formatting
prettier --check src/
```

### Backend (Rust)
```bash
# Type checking + lints
cargo clippy -- -D warnings

# Formatting
cargo fmt --check
```

### Thresholds
| Check | Threshold |
|-------|-----------|
| TypeScript strict | No errors |
| ESLint warnings | 0 |
| Clippy warnings | 0 |
| Unsafe code | 0 blocks (no `unsafe` in application code) |

---

## 2. Unit Tests

### Frontend: Component Tests (Vitest + Testing Library)

```typescript
// Example: DocumentCard tests
describe('DocumentCard', () => {
  it('renders document title', () => {
    render(<DocumentCard document={mockDoc} />);
    expect(screen.getByText('Quantum Mechanics')).toBeInTheDocument();
  });
  
  it('shows page count', () => {
    render(<DocumentCard document={mockDoc} />);
    expect(screen.getByText('240 pages')).toBeInTheDocument();
  });
  
  it('shows processing status badge when processing', () => {
    render(<DocumentCard document={{...mockDoc, status: 'processing'}} />);
    expect(screen.getByText('Processing')).toBeInTheDocument();
  });
  
  it('calls onClick when clicked', () => {
    const onClick = vi.fn();
    render(<DocumentCard document={mockDoc} onClick={onClick} />);
    fireEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledOnce();
  });
  
  it('shows star icon when favorited', () => {
    render(<DocumentCard document={{...mockDoc, isFavorite: true}} />);
    expect(screen.getByTestId('star-icon')).toHaveClass('filled');
  });
});
```

### Frontend: Store Tests

```typescript
describe('documentStore', () => {
  it('adds a document to the store', () => {
    const store = useDocumentStore.getState();
    store.addDocument(mockDoc);
    expect(useDocumentStore.getState().documents).toHaveLength(1);
  });
  
  it('sets active document', () => {
    const store = useDocumentStore.getState();
    store.setActiveDocument('doc-1');
    expect(useDocumentStore.getState().activeDocumentId).toBe('doc-1');
  });
  
  it('removes document', () => {
    const store = useDocumentStore.getState();
    store.addDocument(mockDoc);
    store.removeDocument(mockDoc.id);
    expect(useDocumentStore.getState().documents).toHaveLength(0);
  });
});
```

### Backend: Rust Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_chunking_small_text() {
        let text = "Short text under limit.";
        let chunks = chunk_text(text, 100, 0);
        assert_eq!(chunks.len(), 1);
    }
    
    #[test]
    fn test_chunking_with_overlap() {
        let text = "A ".repeat(1000);
        let chunks = chunk_text(&text, 100, 10);
        assert!(chunks.len() > 8);
        // Verify overlap
        assert!(chunks[0].content.ends_with("A ".repeat(10).trim()));
        assert!(chunks[1].content.starts_with("A ".repeat(10).trim()));
    }
    
    #[test]
    fn test_embedding_normalization() {
        let vec = vec![3.0, 4.0];
        let normalized = normalize_vector(&vec);
        assert!((normalized[0] - 0.6).abs() < 0.001);
        assert!((normalized[1] - 0.8).abs() < 0.001);
    }
    
    #[test]
    fn test_cosine_similarity() {
        let a = vec![1.0, 0.0];
        let b = vec![0.0, 1.0];
        let sim = cosine_similarity(&a, &b);
        assert!((sim - 0.0).abs() < 0.001);
    }
    
    #[test]
    fn test_sm2_scheduling() {
        let review = sm2_schedule(3, 2.5, 0, 0);  // Rating: Good, first review
        assert_eq!(review.interval_days, 1.0);
        
        let review = sm2_schedule(3, 2.5, 1, 1.0);  // Second review
        assert_eq!(review.interval_days, 6.0);
    }
    
    #[test]
    fn test_sanitize_path_injection() {
        let result = validate_path("/etc/passwd/../../../etc/passwd");
        assert!(result.is_err());
    }
}
```

### Coverage Targets

| Layer | Target |
|-------|--------|
| UI Components | 80%+ |
| Store/State | 90%+ |
| Utility functions | 95%+ |
| Rust backend core | 85%+ |
| Rust unsafe blocks | 100% (all tested) |

---

## 3. Integration Tests

### API Command Tests

```rust
#[cfg(test)]
mod integration_tests {
    use super::*;
    
    #[tokio::test]
    async fn test_upload_and_process() {
        let app = test_app::setup().await;
        
        // Upload
        let doc = app.upload_document("test_files/sample.pdf").await.unwrap();
        assert_eq!(doc.status, "uploaded");
        
        // Process
        let job = app.process_document(doc.id).await.unwrap();
        assert_eq!(job.status, "queued");
        
        // Wait for completion
        tokio::time::sleep(Duration::from_secs(5)).await;
        let doc = app.get_document(doc.id).await.unwrap();
        assert_eq!(doc.status, "processed");
        assert!(doc.stats.notes_count > 0);
    }
    
    #[tokio::test]
    async fn test_search_returns_results() {
        let app = test_app::setup().await;
        let doc = app.upload_and_process("test_files/sample.pdf").await.unwrap();
        
        let results = app.search("quantum").await.unwrap();
        assert!(!results.is_empty());
        assert_eq!(results[0].document_id, doc.id);
    }
    
    #[tokio::test]
    async fn test_flashcard_review_cycle() {
        let app = test_app::setup().await;
        let doc = app.upload_and_process("test_files/sample.pdf").await.unwrap();
        
        let cards = app.get_flashcards(doc.id).await.unwrap();
        assert!(!cards.is_empty());
        
        // Review all cards
        for card in &cards {
            app.review_flashcard(card.id, 3).await.unwrap();
        }
        
        let stats = app.get_review_stats().await.unwrap();
        assert_eq!(stats.cards_reviewed_today, cards.len());
    }
}
```

### Pipeline Integration Tests

```rust
#[tokio::test]
async fn test_full_pipeline_ocr_to_notes() {
    let pipeline = Pipeline::new(test_config()).await.unwrap();
    let text = pipeline.run_ocr("test_files/scanned_doc.png").await.unwrap();
    let chunks = pipeline.chunk_text(&text);
    let embeddings = pipeline.generate_embeddings(&chunks).await.unwrap();
    let notes = pipeline.generate_notes(&text).await.unwrap();
    
    assert!(!text.is_empty());
    assert!(chunks.len() > 0);
    assert_eq!(embeddings.len(), chunks.len());
    assert!(notes.contains("#"));
}
```

---

## 4. OCR Accuracy Tests

```rust
#[cfg(test)]
mod ocr_tests {
    #[test]
    fn test_ocr_accuracy_clean_text() {
        let result = ocr_test_runner::evaluate("test_files/clean_text.png");
        assert!(result.accuracy > 0.95);
        assert!(result.cer < 0.05);  // Character error rate
    }
    
    #[test]
    fn test_ocr_accuracy_scanned_pdf() {
        let result = ocr_test_runner::evaluate("test_files/scanned_book_page.png");
        assert!(result.accuracy > 0.85);
    }
    
    #[test]
    fn test_ocr_multilingual() {
        let result = ocr_test_runner::evaluate("test_files/hindi_text.png", "hin");
        assert!(result.accuracy > 0.90);
    }
    
    #[test]
    fn test_ocr_empty_image_returns_error() {
        let result = ocr_test_runner::evaluate("test_files/blank.png");
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), OcrError::NoTextFound);
    }
}
```

---

## 5. Markdown Correctness Tests

```typescript
describe('Markdown Generator', () => {
  it('generates valid Markdown with frontmatter', () => {
    const md = generateMarkdown(mockDocument, mockNotes);
    expect(md).toMatch(/^---\n/);  // Starts with frontmatter
    expect(md).toMatch(/\n---\n/); // Ends frontmatter
    expect(md).toContain('title: "Quantum Mechanics"');
  });
  
  it('generates proper heading hierarchy', () => {
    const md = generateMarkdown(mockDocument, mockNotes);
    const headings = md.match(/^#+/gm);
    // No jumps: h1 → h2 → h3, never h1 → h3
    for (let i = 1; i < headings.length; i++) {
      const prev = headings[i-1].length;
      const curr = headings[i].length;
      expect(curr - prev).toBeLessThanOrEqual(1);
    }
  });
  
  it('generates valid Mermaid code blocks', () => {
    const md = generateMarkdown(mockDocument, mockNotes);
    const mermaidBlocks = md.match(/```mermaid\n[\s\S]*?```/g) || [];
    for (const block of mermaidBlocks) {
      expect(isValidMermaid(block)).toBe(true);
    }
  });
  
  it('renders all formulas in LaTeX delimiters', () => {
    const md = generateMarkdown(mockDocument, mockNotes);
    const formulas = md.match(/\$\$[\s\S]*?\$\$/g) || [];
    expect(formulas.length).toBeGreaterThan(0);
  });
  
  it('generates unique flashcard IDs', () => {
    const cards = generateFlashcards(mockDocument);
    const ids = cards.map(c => c.id);
    expect(new Set(ids).size).toBe(ids.length);
  });
});
```

---

## 6. Hallucination Checks

```python
# tests/hallucination_check.py
"""
Compares AI-generated statements against source document.
Flags claims not supported by the original text.
"""

def test_notes_are_grounded_in_source():
    """Every claim in notes should have a corresponding source passage."""
    source_text = load_document("test_files/sample.pdf")
    notes = generate_notes(source_text)
    
    for claim in extract_claims(notes):
        supporting_evidence = find_supporting_passages(claim, source_text)
        assert len(supporting_evidence) > 0, \
            f"Unsupported claim: {claim}"

def test_flashcards_match_document():
    """Flashcard Q&A should be answerable from source."""
    source_text = load_document("test_files/sample.pdf")
    cards = generate_flashcards(source_text)
    
    for card in cards:
        can_answer = can_be_answered(card.back, source_text)
        assert can_answer, f"Card not grounded: {card.front}"
```

---

## 7. Performance Benchmarks

```rust
#[bench]
fn bench_embedding_generation(b: &mut Bencher) {
    let embedder = Embedder::new(test_config()).unwrap();
    let texts = load_test_texts(100);  // 100 chunks
    
    b.iter(|| {
        let results = embedder.embed_batch(&texts).unwrap();
        assert_eq!(results.len(), 100);
    });
}

#[bench]
fn bench_vector_search(b: &mut Bencher) {
    let db = VectorDB::new_test().unwrap();
    db.insert_batch(generate_test_vectors(1000, 384)).unwrap();
    let query = random_vector(384);
    
    b.iter(|| {
        let results = db.search(&query, 10).unwrap();
        assert_eq!(results.len(), 10);
    });
}
```

### Performance Thresholds (CI)

| Test | Threshold | Breaks Build |
|------|-----------|-------------|
| Embedding 100 chunks | <5s (CPU) | Yes |
| Vector search 10k vectors | <50ms | Yes |
| PDF parse 100 pages | <3s | Yes |
| Markov generation 100pg | <1s | Yes |
| Flashcard review flip | <16ms | Warning |
| App startup (cold) | <3s | Yes |
| App startup (warm) | <1s | Yes |
| Memory (idle) | <200MB | Yes |
| Memory (processing) | <1.5GB | Warning |

---

## 8. Memory Profiling

```rust
#[test]
fn test_no_memory_leaks_in_pipeline() {
    let mut app = test_app::setup();
    
    let before = memory_usage();
    
    for _ in 0..10 {
        let doc = app.upload_and_process("test_files/sample.pdf").unwrap();
        app.delete_document(doc.id).unwrap();
    }
    
    let after = memory_usage();
    let leaked = after - before;
    
    // Allow 5MB tolerance for caches
    assert!(leaked < 5_000_000, "Memory leak detected: {} bytes", leaked);
}

#[test]
fn test_model_unloads_after_timeout() {
    let mut app = test_app::setup();
    app.process_document("test_files/sample.pdf").await;
    
    // Model should be loaded
    assert!(app.is_model_loaded("llama"));
    
    // Wait for idle timeout (5 minutes in production, 10s in test)
    tokio::time::sleep(Duration::from_secs(10)).await;
    
    // Model should be unloaded
    assert!(!app.is_model_loaded("llama"));
    assert!(memory_usage() < 300_000_000);  // Under 300MB after unload
}
```

---

## 9. Test Fixtures

```
tests/fixtures/
├── documents/
│   ├── sample.pdf                 # 10-page clean PDF
│   ├── scanned_book.pdf           # 50-page scanned book
│   ├── scanned_book_300dpi.pdf    # High quality scan
│   ├── scanned_book_72dpi.pdf     # Low quality scan
│   ├── with_tables.pdf            # PDF with complex tables
│   ├── with_formulas.pdf          # PDF with LaTeX formulas
│   ├── with_diagrams.pdf          # PDF with figures/diagrams
│   ├── malicious_bomb.pdf         # PDF bomb (for security tests)
│   ├── empty.pdf                  # Empty document
│   ├── corrupted.pdf              # Corrupted file
│   ├── sample.pptx                # PowerPoint file
│   ├── sample.docx                # Word file
│   └── sample.epub                # EPUB file
├── images/
│   ├── clean_text.png
│   ├── hindi_text.png
│   ├── chinese_text.png
│   └── complex_diagram.png
└── expected_outputs/
    ├── sample_notes.md
    ├── sample_flashcards.json
    └── sample_quiz.json
```

---

## 10. CI/CD Pipeline

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  static-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cargo clippy -- -D warnings
      - run: cargo fmt --check
      - run: npm run lint
      - run: npm run typecheck
  
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cargo test --lib
      - run: npm run test:unit
  
  integration-tests:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    steps:
      - uses: actions/checkout@v4
      - run: cargo test --test integration
  
  ocr-accuracy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python tests/ocr_benchmark.py
      - run: python tests/hallucination_check.py
  
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cargo bench
      - run: python tests/validate_performance.py
```
