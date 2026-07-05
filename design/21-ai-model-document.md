# AI Model Document

## Model Architecture Overview

Khoji uses multiple specialized AI models, not one monolithic model. This document details every model, its requirements, and configuration options.

---

## 1. OCR Models

### Primary: Tesseract v5

| Property | Value |
|----------|-------|
| **Type** | OCR engine |
| **Engine** | Tesseract 5.3.3 (via `tesseract-rs` or CLI) |
| **File Size** | 45MB (base) + 15-50MB per language |
| **RAM Usage** | 200-500MB |
| **CPU Usage** | 1-2 cores at 100% |
| **GPU Support** | CPU only |
| **Speed** | ~10 pages/sec (CPU) |
| **Languages** | 100+ (incl. English, Hindi, Chinese, Arabic, French, German) |
| **Accuracy** | 95%+ on clean text, 80%+ on scanned |
| **Quantization** | N/A (C++ native) |
| **Format** | System package / bundled binary |
| **License** | Apache 2.0 |

**Configuration:**
```json
{
  "ocr_engine": "tesseract",
  "language": "eng",
  "psm_mode": 3,        // Page segmentation mode: 3=auto, 6=block, 11=sparse
  "oem_mode": 1,        // 0=legacy, 1=LSTM, 2=both, 3=default
  "dpi": 300,
  "timeout_seconds": 120
}
```

### Alternative: EasyOCR

| Property | Value |
|----------|-------|
| **Type** | Deep learning OCR |
| **Engine** | EasyOCR (PyTorch-based) |
| **File Size** | 120MB (model files) |
| **RAM Usage** | 1-2GB |
| **CPU Usage** | 2-4 cores |
| **GPU Support** | CUDA (3x speedup) |
| **Speed** | ~3 pages/sec (CPU), ~10 pages/sec (GPU) |
| **Languages** | 80+ |
| **Accuracy** | 97%+ on clean, 90%+ on difficult scans |
| **Quantization** | FP16 supported |
| **When to use** | Low-quality scans, handwritten text, complex layouts |

### Fallback: PaddleOCR

| Property | Value |
|----------|-------|
| **Type** | Lightweight deep learning OCR |
| **File Size** | 15MB |
| **RAM Usage** | 300MB |
| **Speed** | ~5 pages/sec (CPU) |
| **Accuracy** | 90%+ |
| **Best for** | Chinese, Japanese, Korean text; low-resource devices |

---

## 2. Layout Analysis Model

### Primary: LayoutLMv3

| Property | Value |
|----------|-------|
| **Type** | Document layout analysis |
| **File Size** | 440MB |
| **RAM Usage** | 1-2GB |
| **GPU Support** | CUDA (2x speedup) |
| **Speed** | ~2 pages/sec (CPU), ~5 pages/sec (GPU) |
| **Output** | Region types: title, paragraph, table, figure, formula, header, footer, page_number |
| **Accuracy** | 92%+ on standard document layouts |
| **Quantization** | ONNX INT8 supported |

### Fallback: Rule-based Heuristic

No model needed. Uses PDF structure, font sizes, and whitespace analysis.
- Speed: ~20 pages/sec
- Accuracy: ~70%
- RAM: 0MB (no model loaded)

---

## 3. Vision Model (Figure Understanding)

### Primary: Florence-2 (base)

| Property | Value |
|----------|-------|
| **Type** | Vision-language model |
| **Parameters** | 0.23B |
| **File Size** | 340MB |
| **RAM Usage** | 1-2GB (when loaded) |
| **GPU Support** | CUDA (preferred) / CPU (slow) |
| **Speed** | ~1 figure/sec (GPU), ~0.2 fig/sec (CPU) |
| **Output** | Text description of figures, diagrams, charts |
| **Capabilities** | Captioning, OCR, object detection, chart reading |
| **Quantization** | ONNX INT8: 170MB, ~1.5GB RAM |

### Alternative: Skip Vision (No vision model)

When disabled, figures are referenced by caption only ("See Figure 1").

---

## 4. Embedding Model

### Primary: all-MiniLM-L6-v2

| Property | Value |
|----------|-------|
| **Type** | Sentence transformer |
| **Parameters** | 22M |
| **File Size** | 80MB (ONNX) |
| **RAM Usage** | 200-400MB |
| **GPU Support** | CUDA (minor speedup), runs well on CPU |
| **Speed** | ~500 texts/sec (CPU) |
| **Dimensions** | 384 |
| **Distance** | Cosine similarity |
| **Max Tokens** | 256 per chunk |
| **Quantization** | INT8: 40MB, minimal accuracy loss |
| **Format** | ONNX |
| **When to use** | Default — best quality/speed tradeoff |

### Alternative: BGE-Large

| Property | Value |
|----------|-------|
| **Parameters** | 335M |
| **File Size** | 670MB |
| **RAM Usage** | 1-2GB |
| **Dimensions** | 1024 |
| **Accuracy** | Higher for specialized domains |
| **When to use** | Research, medical, legal documents requiring higher accuracy |

### Alternative: BGE-Small

| Property | Value |
|----------|-------|
| **File Size** | 33MB |
| **RAM Usage** | 100MB |
| **Dimensions** | 384 |
| **When to use** | 4GB RAM devices |

---

## 5. Small Language Model (SLM/LLM)

### Primary: Llama 3.2 1B

| Property | Value |
|----------|-------|
| **Type** | Decoder-only transformer |
| **Parameters** | 1.24B |
| **File Size** | 620MB (Q4_K_M GGUF) |
| **RAM Usage** | 1-2GB (varies by context length) |
| **GPU Support** | Metal (macOS), CUDA, Vulkan |
| **CPU Speed** | ~10 tokens/sec (4 cores) |
| **GPU Speed** | ~30 tokens/sec (M1), ~50 tok/sec (RTX 3060) |
| **Context Length** | 8,192 tokens (configurable to 2,048 for memory saving) |
| **Quantization** | Q4_K_M (default), Q5_K_M, Q8_0, F16 |
| **Format** | GGUF |
| **License** | Llama 3.2 Community License |
| **Use Cases** | Knowledge extraction, summary, flashcard gen, quiz gen, chat |
| **Fallback** | Phi-3 Mini 3.8B (if RAM available) |

### Alternative: Phi-3 Mini 3.8B

| Property | Value |
|----------|-------|
| **Parameters** | 3.8B |
| **File Size** | 2.2GB (Q4_K_M) |
| **RAM Usage** | 3-4GB |
| **CPU Speed** | ~5 tokens/sec |
| **GPU Speed** | ~20 tokens/sec |
| **When to use** | 8GB+ RAM devices, need higher quality |

### Alternative: Gemma 2 2B

| Property | Value |
|----------|-------|
| **Parameters** | 2.6B |
| **File Size** | 1.5GB (Q4_K_M) |
| **RAM Usage** | 2-3GB |
| **When to use** | Mid-range devices |

### Alternative: Mistral 7B

| Property | Value |
|----------|-------|
| **Parameters** | 7.3B |
| **File Size** | 4.1GB (Q4_K_M) |
| **RAM Usage** | 6-8GB |
| **When to use** | High-end devices (16GB+ RAM) |

### Minimal Fallback: Llama 3.2 0.5B (Experimental)

| Property | Value |
|----------|-------|
| **Parameters** | 0.5B |
| **File Size** | 300MB (Q4_K_M) |
| **RAM Usage** | 500MB |
| **CPU Speed** | ~25 tokens/sec |
| **When to use** | Ultra-low-resource devices / emergency fallback |

---

## 6. Quantization Guide

| Quantization | Size Reduction | Quality Loss | Use Case |
|-------------|---------------|--------------|----------|
| **F16** | 1x (baseline) | None | Reference / GPU |
| **Q8_0** | 2x | Minimal | High quality, moderate RAM |
| **Q5_K_M** | 3x | Very low | Recommended for quality |
| **Q4_K_M** | 4x | Low | Default — best tradeoff |
| **Q4_0** | 4x | Moderate | Low RAM devices |
| **Q3_K_M** | 5x | Noticeable | Aggressive memory saving |
| **Q2_K** | 6x | Significant | Emergency only |

---

## 7. Token Limits & Chunking

| Model | Max Tokens | Recommended Chunk Size | Overlap |
|-------|-----------|----------------------|---------|
| all-MiniLM-L6-v2 | 256 | 200 tokens | 10% |
| Llama 3.2 1B | 8192 | 2048 tokens | 10% |
| Phi-3 Mini | 4096 | 2048 tokens | 10% |

### Chunking Strategy

```
Document Text
│
├── Paragraph 1
├── Paragraph 2              ┌──────────────────┐
├── Paragraph 3    ────────▶ │ Chunk 1 (200 tok)│
├── Paragraph 4              │ Overlap: 20 tok  │
├── Paragraph 5              └────────┬─────────┘
├── Paragraph 6                       │
├── Paragraph 7              ┌────────▼─────────┐
├── Paragraph 8    ────────▶ │ Chunk 2 (200 tok)│
└── ...                        └──────────────────┘
```

---

## 8. Memory Usage Profile by Scenario

### Scenario A: 4GB RAM Laptop (CPU Only)

| Component | Model | Memory |
|-----------|-------|--------|
| OCR | Tesseract v5 | 200MB |
| Layout | Rule-based (no model) | 0MB |
| Vision | Disabled | 0MB |
| Embedding | BGE-Small (INT8) | 100MB |
| LLM | Llama 3.2 1B (Q4_K_M) | 1GB |
| Vector DB | SQLite-vec | 50MB |
| App + Cache | — | 200MB |
| **Total** | | **~1.55GB** ✅ |

### Scenario B: 8GB RAM Laptop (CPU)

| Component | Model | Memory |
|-----------|-------|--------|
| OCR | EasyOCR | 1.5GB |
| Layout | LayoutLMv3 (INT8) | 800MB |
| Vision | Florence-2 (INT8) | 1GB |
| Embedding | all-MiniLM-L6-v2 | 300MB |
| LLM | Phi-3 Mini (Q4_K_M) | 3GB |
| Vector DB | SQLite-vec | 100MB |
| App + Cache | — | 300MB |
| **Total** | | **~7GB** ✅ |

### Scenario C: 16GB+ RAM Workstation (GPU)

| Component | Model | Memory |
|-----------|-------|--------|
| OCR | Surya OCR (GPU) | 2GB |
| Layout | LayoutLMv3 (FP16) | 1.5GB |
| Vision | Florence-2 (FP16) | 2GB |
| Embedding | BGE-Large (FP16) | 1.5GB |
| LLM | Mistral 7B (Q5_K_M) | 5GB |
| Vector DB | SQLite-vec | 200MB |
| App + Cache | — | 500MB |
| **Total** | | **~12.7GB** ✅ |

---

## 9. Model Download Manager

```
Model Storage: ~/.khoji/models/
│
├── ocr/
│   ├── tesseract-v5/         (45MB)
│   │   ├── eng.traineddata
│   │   └── hin.traineddata
│   └── easyocr/              (120MB)
│       └── model.pt
│
├── layout/
│   └── layoutlm-v3/          (440MB)
│       └── model.onnx
│
├── vision/
│   └── florence-2-base/      (340MB)
│       └── model.onnx
│
├── embeddings/
│   ├── all-minilm-l6-v2/     (80MB)
│   │   └── model.onnx
│   └── bge-small/            (33MB)
│       └── model.onnx
│
└── llm/
    ├── llama-3.2-1b/         (620MB)
    │   └── llama-3.2-1b.Q4_K_M.gguf
    ├── phi-3-mini/            (2.2GB)
    │   └── phi-3-mini.Q4_K_M.gguf
    └── gemma-2-2b/            (1.5GB)
        └── gemma-2-2b.Q4_K_M.gguf
```

---

## 10. ONNX Runtime Configuration

```json
{
  "onnx": {
    "execution_providers": ["cpu"],
    "cpu": {
      "arena_strategy": "workspace",
      "enable_cpu_mem_arena": true
    },
    "cuda": {
      "device_id": 0,
      "enable_cuda_graph": false
    },
    "session": {
      "graph_optimization_level": "all",
      "enable_mem_pattern": true,
      "enable_cpu_mem_arena": true,
      "intra_op_num_threads": 4
    }
  }
}
```

---

## 11. llama.cpp Configuration

```json
{
  "llama": {
    "model_path": "~/.khoji/models/llm/llama-3.2-1b/llama-3.2-1b.Q4_K_M.gguf",
    "context_size": 2048,
    "batch_size": 512,
    "threads": 4,
    "gpu_layers": 0,
    "temperature": 0.3,
    "top_p": 0.9,
    "repeat_penalty": 1.1,
    "max_tokens": 1024,
    "seed": 42
  }
}
```
