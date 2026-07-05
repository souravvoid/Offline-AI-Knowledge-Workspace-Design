# Phase 7-8: Wireframes & High-Fidelity UI

## Screen 1: Splash / First Launch

```
┌──────────────────────────────────────────────┐
│                                              │
│                                              │
│                   🔍                         │
│              KHOJI v1.0                      │
│         Offline AI Knowledge Workspace       │
│                                              │
│          ┌──────────────────────┐            │
│          │   Get Started        │            │
│          └──────────────────────┘            │
│                                              │
│     ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐               │
│     │✓ │ │✓ │ │  │ │  │ │  │               │
│     └──┘ └──┘ └──┘ └──┘ └──┘               │
│    Setup  Model  Doc   AI   Ready            │
│           Downl  Upload     to Go            │
│                                              │
│         [Skip Setup]                         │
│                                              │
└──────────────────────────────────────────────┘
```

## Screen 2: Library (Empty State)

```
┌─────────────────────────────────────────────────────────────┐
│ 🔍 Khoji          [Search all... ⌘K]            ☰ Settings │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                                                             │
│                    ┌─────────────────┐                      │
│                    │    📂            │                     │
│                    │   No documents   │                     │
│                    │  yet. Drop your  │                     │
│                    │  first PDF, PPT, │                     │
│                    │  DOCX, or image  │                     │
│                    │  to get started. │                     │
│                    │                  │                     │
│                    │ [Upload Document]│                     │
│                    │  or drag and drop│                     │
│                    └─────────────────┘                      │
│                                                             │
│  Supported: PDF, PNG, JPG, PPT, DOCX, EPUB                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Screen 3: Library (With Documents)

```
┌─────────────────────────────────────────────────────────────┐
│ 🔍 Khoji   [Search... ⌘K]   ⌂ Upload   ⋮                  │
├─────────────────────────────────────────────────────────────┤
│ Collections │ All    │ Recent │ Favorites                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ 📄            │  │ 📄            │  │ 📄            │     │
│  │ Quantum      │  │ Machine      │  │ Organic      │     │
│  │ Mechanics    │  │ Learning     │  │ Chemistry    │     │
│  │              │  │              │  │              │     │
│  │ 24 pages     │  │ 150 pages    │  │ 89 pages     │     │
│  │ 45 notes     │  │ 120 notes    │  │ 67 notes     │     │
│  │ 12 flashcard │  │ 35 flashcards│  │ 21 flashcards │    │
│  │ ⭐           │  │              │  │ ⭐           │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ 🖼️            │  │ 📄            │                         │
│  │ Cell Biology │  │ Algorithms   │                         │
│  │ Diagrams     │  │ & Data       │                         │
│  │              │  │ Structures   │                         │
│  │ 12 images    │  │ 200 pages    │                         │
│  │ 8 notes      │  │ 89 notes     │                         │
│  └──────────────┘  └──────────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Screen 4: Upload & Processing

```
┌─────────────────────────────────────────────────────────────┐
│ ← Library    Upload Document                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────────────────────────────────────┐      │
│  │                                                   │      │
│  │            Drop files here or click to browse      │      │
│  │                                                   │      │
│  │    📄 PDF  🖼️ Image  📊 PPT  📝 DOCX  📚 EPUB     │     │
│  │                                                   │      │
│  └───────────────────────────────────────────────────┘      │
│                                                             │
│  ┌─── Quantum_Mechanics_Textbook.pdf ──── 24MB ── [✕] ──┐  │
│  │  ┌────────────────────────────────────────────────────┐  │
│  │  │                                                    │  │
│  │  │  📄 OCR & Layout Analysis     ✓ Complete           │  │
│  │  │  🔤 Text Extraction           ✓ Complete           │  │
│  │  │  📝 Markdown Generation       ◌ Processing...      │  │
│  │  │     ████████████░░░░░░░░░░░░  65%                 │  │
│  │  │  🧠 Embeddings                ○ Pending           │  │
│  │  │  🤖 LLM Processing            ○ Pending           │  │
│  │  │  🃏 Flashcard Generation      ○ Pending           │  │
│  │  │  ❓ Quiz Generation           ○ Pending           │  │
│  │  │  🧠 Mind Map Generation       ○ Pending           │  │
│  │  │                                                    │  │
│  │  └────────────────────────────────────────────────────┘  │
│  │  ⏱ Estimated time remaining: 45 seconds               │  │
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  [Background]  [Cancel]                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Screen 5: Document Workspace (Desktop)

```
┌─────────────────────────────────────────────────────────────────────┐
│ ← Library  │  ⚛️ Quantum Mechanics  │ ⭐ ★ │ ⋮ │ [Export]          │
├────────────┬────────────────────────────────────────────────────┬──┤
│            │                                                    │  │
│ Outline    │  ┌─── Notes ──┬─ Flashcards ─┬─ Quiz ─┬─ Mind Map┐ │  │
│            │  │                                                    │ │
│ ├ Chapter 1│  │ # Quantum Mechanics                                 │ │
│ ├ Chapter 2│  │                                                    │ │
│ ├ Chapter 3│  │ ## Chapter 1: Wave-Particle Duality                │ │
│ │ Section A│  │                                                    │ │
│ │ Section B│  │ ### Definition                                      │ │
│ ├ Chapter 4│  │ Wave-particle duality is the concept in quantum    │ │
│            │  │ mechanics that every particle exhibits both wave   │ │
│            │  │ and particle properties.                           │ │
│            │  │                                                    │ │
│            │  │ ### Key Formula                                     │ │
│            │  │ > λ = h / p                                        │ │
│            │  │ > de Broglie wavelength                            │ │
│            │  │                                                    │ │
│            │  │ ### Mermaid Diagram                                 │ │
│            │  │ ┌────────────────────────────────────────────┐    │ │
│            │  │ │         Wave-Particle Duality               │    │ │
│            │  │ │    ┌──────┐         ┌────────┐            │    │ │
│            │  │ │    │ Wave │ ←───→   │Particle│            │    │ │
│            │  │ │    └──────┘         └────────┘            │    │ │
│            │  │ └────────────────────────────────────────────┘    │ │
│            │  │                                                    │ │
│            │  └────────────────────────────────────────────────────┘ │
│            │                                                    │  │
├────────────┴────────────────────────────────────────────────────┴──┤
│ Model: Llama 3.2 (1B)  │ 45 notes  │ 20 cards  │ Quiz: 10 Qs       │
└─────────────────────────────────────────────────────────────────────┘
```

## Screen 6: Flashcard Review Mode

```
┌────────────────────────────────────────────────────────────┐
│ ← Back to Workspace    Review: Quantum Mechanics    🎯 12│
├────────────────────────────────────────────────────────────┤
│                                                            │
│              ┌──────────────────────────────┐              │
│              │                              │              │
│              │   What is the de Broglie     │              │
│              │   wavelength equation?       │              │
│              │                              │              │
│              │                              │              │
│              │      [Show Answer]           │              │
│              │                              │              │
│              └──────────────────────────────┘              │
│                                                            │
│         ────  Card 5 of 20  ────                          │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Again (1min) │ Hard (5min) │ Good (1d) │ Easy (3d) │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Screen 7: Quiz Mode

```
┌────────────────────────────────────────────────────────────┐
│ ← Back to Workspace    Quiz: Quantum Mechanics     ⏱ 12:34│
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Question 3 of 10                                          │
│  ────────────────────────────────────────────────────      │
│                                                            │
│  Which of the following best describes the                  │
│  Heisenberg Uncertainty Principle?                         │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ A) Particles always have definite position and        │  │
│  │    momentum                                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ B) The more precisely position is known, the less    │  │
│  │    precisely momentum can be known                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ C) Energy is always quantized                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ D) Light behaves only as a wave                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  [Skip]                           [Submit Answer]          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Screen 8: AI Chat Panel

```
┌────────────────────────────────────────────────────────┐
│ 💬 AI Chat       📄 Context: Quantum Mechanics    ⋮   │
├────────────────────────────────────────────────────────┤
│                                                        │
│  User:  Explain the double-slit experiment             │
│         in simple terms.                               │
│                                                        │
│  ┌────────────────────────────────────────────────┐    │
│  │ 🤖 Imagine throwing tennis balls through two   │    │
│  │ holes in a wall. You'd expect two piles behind  │    │
│  │ each hole. But with electrons, you get an       │    │
│  │ interference pattern — like waves in water.     │    │
│  │ [Source: Chapter 1, Page 12]                    │    │
│  └────────────────────────────────────────────────┘    │
│                                                        │
│  User:  Generate 3 more quiz questions on this.        │
│                                                        │
│  ┌────────────────────────────────────────────────┐    │
│  │ 🤖 1. What is the role of the observer in the  │    │
│  │ double-slit experiment?                        │    │
│  │ 2. How does the pattern change when one slit   │    │
│  │ is closed?                                     │    │
│  │ 3. What does the double-slit experiment prove  │    │
│  │ about wave-particle duality?                    │    │
│  └────────────────────────────────────────────────┘    │
│                                                        │
├────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────┐ [Send] [✨]  │
│ │ Ask anything about this document...   │              │
│ └──────────────────────────────────────┘              │
└────────────────────────────────────────────────────────┘
```

## Screen 9: Semantic Search

```
┌───────────────────────────────────────────────────────────────┐
│ 🔍 Search                                    [Esc to close]   │
├───────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐   │
│ │ └> neural networks backpropagation              [⌘ ↵]   │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                               │
│  Results (12)                               Filter: All Docs  │
│  ─────────────────────────────────────────────────────────    │
│                                                               │
│  ┌─── 📄 Machine Learning Basics ──────────────────────────┐  │
│  │  ...backpropagation computes the gradient of the        │  │
│  │  loss function with respect to the weights of the       │  │
│  │  **neural network**...                                  │  │
│  │                                        Page 42 | Score 95% │
│  └─────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌─── 📄 Deep Learning with Python ─────────────────────────┐ │
│  │  The chain rule is essential for understanding           │  │
│  │  **backpropagation** in **neural networks**...           │  │
│  │                                        Page 89 | Score 88% │
│  └─────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌─── 📄 Neural Networks: A Visual Guide ───────────────────┐ │
│  │  ┌──┐    ┌──┐    ┌──┐                                    │  │
│  │  │x1│───▶│h1│───▶│y1│  Backpropagation visually:         │  │
│  │  └──┘    └──┘    └──┘  error flows backwards...          │  │
│  │                                        Page 15 | Score 82% │
│  └─────────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Screen 10: Settings

```
┌────────────────────────────────────────────────────────────┐
│ ← Back    Settings                                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  General          ────────────────────────────────────     │
│  Models                                                     │
│  Storage         Theme               ○ Light  ● Dark ○ Sys │
│  Export                                                     │
│  Shortcuts       Language           English ▼              │
│  Accessibility                                              │
│  About           Font Size          ○ Sm  ● Md  ○ Lg ○ XL │
│                                                            │
│                  Reading Mode       ○ Serif  ● Sans        │
│                                                            │
│                  Startup            □ Open last document   │
│                                     □ Auto-load library    │
│                                                            │
│  ───────────────────────────────────────────────────────    │
│                                                            │
│  Models                                                     │
│  ────────────────────────────────────────────────────────   │
│                                                            │
│  OCR Engine                                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Tesseract v5 (Recommended)          [●] Download 45MB│   │
│  │ EasyOCR                              ○               │   │
│  │ Document AI (Experimental)           ○               │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                            │
│  LLM Model                                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Llama 3.2 1B (Fast)             [●] Downloaded       │   │
│  │ Phi-3 Mini 3.8B                  ○ Download 2.2GB   │   │
│  │ Mistral 7B                        ○ Download 4.1GB   │   │
│  │ Gemma 2 2B                        ○ Download 1.5GB   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                            │
│  Embedding Model                                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ All-MiniLM-L6-v2              [●] Downloaded         │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                            │
│  Storage Used: 1.2 GB / 10 GB                               │
│  ───────────────────────────────────── ████░░ 12% ────    │
│  [Clear Cache]                         [Reset All Data]    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Screen 11: Mobile Layout

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 🔍 Khoji    ⌂  │     │ ← Quantum       │     │         Card 5/20│
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│                 │     │ 📝 ✏ 🃏 ❓ 🧠   │     │                 │
│  ┌───────────┐  │     ├─────────────────┤     │  What is the    │
│  │ 📄         │  │     │                 │     │  Heisenberg     │
│  │ Quantum   │  │     │ # Quantum        │     │  Uncertainty   │
│  │ Mechanics │  │     │ Mechanics        │     │  Principle?    │
│  │            │  │     │                  │     │                 │
│  │ 24p | 45n  │  │     │ ## Chapter 1     │     │                 │
│  └───────────┘  │     │                  │     │   [Show]       │
│                 │     │ Wave-particle     │     │                 │
│  ┌───────────┐  │     │ duality is...     │     │ ──[≡]──[≡]──  │
│  │ 📄         │  │     │                  │     │ A H G E        │
│  │ Machine   │  │     │ > λ = h/p        │     │                 │
│  │ Learning  │  │     │                  │     │                 │
│  └───────────┘  │     │                  │     │                 │
│                 │     │                  │     │                 │
│                 │     │                  │     │                 │
│                 │     │                  │     │                 │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ 📚 🃏 💬 🔍 ⚙️ │     │ 📚 🃏 💬 🔍 ⚙️   │     │ 📚 🃏 💬 🔍 ⚙️ │
└─────────────────┘     └─────────────────┘     └─────────────────┘
   Library Screen         Document Screen         Flashcards Screen
   (Mobile)               (Mobile)               (Mobile)
```

## Screen 12: Mind Map View

```
┌──────────────────────────────────────────────────────────────┐
│ ← Back    Mind Map: Neural Networks              [Export]     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                      ┌──────────────────┐                    │
│                      │  Neural Networks  │                    │
│                      └────────┬─────────┘                    │
│                               │                              │
│           ┌───────────────────┼───────────────────┐          │
│           │                   │                   │          │
│    ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐    │
│    │  Architecture│    │  Training   │    │  Applications│   │
│    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    │
│           │                  │                  │           │
│     ┌─────┼─────┐      ┌────┼────┐       ┌─────┼─────┐     │
│     │     │     │      │    │    │       │     │     │     │
│  ┌──▼┐ ┌──▼┐ ┌──▼┐ ┌──▼┐ ┌──▼┐ ┌──▼┐ ┌──▼┐ ┌──▼┐ ┌──▼┐  │
│  │FF │ │CNN│ │RNN│ │BP │ │SGD│ │Reg│ │CV │ │NLP│ │Gen│  │
│  └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘  │
│                                                              │
│  [Zoom: 100%] [Fit] [+][-] [⟲ Reset]                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Screen 13: Export Dialog

```
┌────────────────────────────────────────────────────────┐
│  Export: Quantum Mechanics                    [✕]     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Select Format                                         │
│                                                        │
│  ┌────────────────────────────────────────────────┐    │
│  │ ○ Markdown (Notes + Flashcards + Quiz)  ✅(Rec)  │    │
│  │ ● Anki (.apkg)                           2.4MB   │    │
│  │ ○ PDF                                    4.1MB   │    │
│  │ ○ LaTeX                                  1.8MB   │    │
│  │ ○ JSON (Structured Data)                  890KB   │    │
│  │ ○ Text (.txt)                             340KB   │    │
│  └────────────────────────────────────────────────┘    │
│                                                        │
│  Include:                                              │
│  ☑ Notes                                              │
│  ☑ Flashcards                                         │
│  ☑ Quiz Questions                                      │
│  ☑ Mind Map (Mermaid + SVG)                           │
│  ☐ Images from document                                │
│                                                        │
│  [Cancel]                       [Export → Downloads]    │
│                                                        │
└────────────────────────────────────────────────────────┘
```
