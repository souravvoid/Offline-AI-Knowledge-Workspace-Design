# Phase 11-12: Markdown Design & Mermaid Diagrams

## Markdown Output Template (AI-Generated)

When a document is processed, the system produces the following Markdown structure:

```markdown
---
title: "Quantum Mechanics: An Introduction"
source: "quantum_mechanics_textbook.pdf"
author: "Griffiths, David J."
pages: 24
processed: "2026-07-03"
tags: [physics, quantum, wave-mechanics]
difficulty: advanced
language: english
model: llama-3.2-1b
license: CC-BY-SA
---

# Quantum Mechanics: An Introduction

> **TL;DR:** A comprehensive introduction to quantum mechanics covering
> wave-particle duality, the Schrödinger equation, quantum operators,
> and the uncertainty principle. The document explains how quantum
> mechanics describes nature at atomic scales through mathematical
> formalisms and experimental evidence.

---

## Overview

Quantum mechanics is the fundamental theory describing the physical
properties of nature at the scale of atoms and subatomic particles.
It introduces concepts that challenge classical intuition, including:

- **Wave-particle duality**: Particles exhibit both wave-like and
  particle-like behavior
- **Quantization**: Physical quantities take discrete values
- **Superposition**: Systems exist in multiple states simultaneously
- **Uncertainty**: Precision limits on complementary measurements

---

## Key Definitions

### Wave Function (Ψ)
A mathematical description of the quantum state of a system. The
probability of finding a particle in a given location is |Ψ|².

### Hamiltonian (Ĥ)
The operator representing the total energy of the system.

### Eigenstate
A state that yields a definite value (eigenvalue) when measured
for a particular observable.

---

## Important Formulas

### Schrödinger Equation (Time-Dependent)
$$
i\hbar\frac{\partial}{\partial t}|\Psi(t)\rangle = \hat{H}|\Psi(t)\rangle
$$

### Schrödinger Equation (Time-Independent)
$$
\hat{H}|\Psi\rangle = E|\Psi\rangle
$$

### de Broglie Wavelength
$$
\lambda = \frac{h}{p}
$$

### Heisenberg Uncertainty Principle
$$
\Delta x \Delta p \geq \frac{\hbar}{2}
$$

---

## Diagrams

### Wave-Particle Duality Overview

```mermaid
flowchart TD
    A[Light / Matter] --> B{Wave or Particle?}
    B -->|Interference| C[Wave behavior]
    B -->|Photoelectric effect| D[Particle behavior]
    C --> E[Double-slit experiment]
    D --> F[Compton scattering]
    E --> G[Conclusion: Wave-Particle Duality]
    F --> G
    G --> H[Described by Wave Function Ψ]
```

### The Schrödinger Equation

```mermaid
flowchart LR
    A[Classical Wave Eq] --> B[Hamiltonian Analogy]
    B --> C[Schrödinger Eq]
    C --> D[Time-Dependent]
    C --> E[Time-Independent]
    D --> F[Evolution of States]
    E --> G[Energy Eigenvalues]
    F --> H[Quantum Dynamics]
    G --> I[Allowed Energy Levels]
```

### Quantum Measurement Process

```mermaid
sequenceDiagram
    participant System as Quantum System
    participant Observer as Measurement Device
    participant Classic as Classical World

    System->>System: Evolves via Schrödinger Eq
    System->>Observer: Wave function collapses
    Observer->>Classic: Reports eigenvalue
    Note over System,Classic: |Ψ⟩ → |λᵢ⟩ with probability |⟨λᵢ|Ψ⟩|²
```

### Timeline: Development of Quantum Mechanics

```mermaid
timeline
    title Evolution of Quantum Theory
    1900 : Planck's Blackbody Radiation
    1905 : Photoelectric Effect (Einstein)
    1913 : Bohr Model of Atom
    1924 : de Broglie Wave Hypothesis
    1925 : Heisenberg Matrix Mechanics
    1926 : Schrödinger Wave Equation
    1927 : Uncertainty Principle
    1935 : EPR Paradox
    1950s : Quantum Field Theory
    1980s : Quantum Computing Begins
```

### Entity Relationship: Quantum Concepts

```mermaid
erDiagram
    QUANTUM_STATE ||--o{ WAVE_FUNCTION : described_by
    WAVE_FUNCTION ||--|| SCHRODINGER_EQ : evolves_by
    HAMILTONIAN ||--|| SCHRODINGER_EQ : appears_in
    OBSERVABLE ||--|| OPERATOR : represented_by
    OPERATOR ||--o{ EIGENVALUE : has
    MEASUREMENT ||--|| WAVE_FUNCTION : collapses
    MEASUREMENT }o--|| EIGENVALUE : yields
    UNCERTAINTY ||--|| OBSERVABLE : relates
    COMPLEMENTARITY ||--|| UNCERTAINTY : causes
```

### Decision Tree: Quantum vs Classical Regime

```mermaid
flowchart TD
    Start{System Size?}
    Start -->|Atomic scale| Q1
    Start -->|Macroscopic| C1[Use Classical Physics]
    Q1{Action ~ ℏ?}
    Q1 -->|Yes| QM[Quantum Mechanics Required]
    Q1 -->|No| C1
    QM --> Q2{Measurement?}
    Q2 -->|Before| QS[Superposition]
    Q2 -->|After| CE[Collapse to Eigenstate]
```

---

## Examples

### Example 1: Particle in a Box

A particle of mass m is confined to a 1D box of length L.

**Solution:**
The wave function is:
$$
\psi_n(x) = \sqrt{\frac{2}{L}} \sin\left(\frac{n\pi x}{L}\right)
$$

**Energy levels:**
$$
E_n = \frac{n^2\pi^2\hbar^2}{2mL^2}
$$

### Example 2: Tunneling Effect

A particle with energy E encounters a barrier of height V₀ > E.

The particle can tunnel through with probability:
$$
T \approx e^{-2\kappa a}
$$
where $\kappa = \sqrt{2m(V_0-E)}/\hbar$

---

## Important Questions

1. Explain the physical interpretation of the wave function.
2. Derive the time-independent Schrödinger equation from the
   time-dependent form.
3. What is the significance of the Heisenberg Uncertainty Principle?
4. Compare and contrast the Copenhagen and Many-Worlds interpretations.
5. How does quantum tunneling enable technologies like scanning
   tunneling microscopy?

---

## Quiz

### Question 1
Which equation describes the time evolution of a quantum state?

A. Newton's Second Law
B. Maxwell's Equations
C. Schrödinger Equation ✓
D. Einstein's Field Equations

### Question 2
The de Broglie wavelength of a particle is inversely proportional to:

A. Its mass
B. Its momentum ✓
C. Its energy
D. Its charge

...

---

## Flashcards

### Card 1
**Front:** What is the Schrödinger equation?
**Back:** The fundamental equation of quantum mechanics describing how
the quantum state of a system evolves over time.
$$i\hbar\frac{\partial}{\partial t}|\Psi\rangle = \hat{H}|\Psi\rangle$$
**Tags:** #quantum #core-equation #schrodinger

### Card 2
**Front:** State the Heisenberg Uncertainty Principle.
**Back:** It is impossible to simultaneously know both the exact
position and exact momentum of a particle.
$$\Delta x \Delta p \geq \frac{\hbar}{2}$$
**Tags:** #quantum #uncertainty #heisenberg

---

## Learning Progress

- [x] Wave-Particle Duality
- [x] Wave Function
- [x] Schrödinger Equation
- [ ] Quantum Operators
- [ ] Measurement Theory
- [ ] Applications

---

## References

- Chapter 1, "The Wave Function" (p. 1-24)
- Chapter 2, "Time-Independent Schrödinger Equation" (p. 25-67)
- Feynman Lectures, Vol. 3, Chapter 1

---

## Tags

`#quantum-mechanics` `#physics` `#wave-function` `#schrodinger`
`#heisenberg` `#wave-particle-duality` `#advanced`
```

---

## Additional Mermaid Diagram Types

### Knowledge Graph

```mermaid
graph TD
    QM[Quantum Mechanics] --> WP[Wave-Particle Duality]
    QM --> SE[Schrödinger Equation]
    QM --> UP[Uncertainty Principle]
    WP --> DE[Double-slit Experiment]
    WP --> PE[Photoelectric Effect]
    SE --> TD[Time-Dependent]
    SE --> TI[Time-Independent]
    SE --> WE[Wave Function]
    UP --> HP[Heisenberg's Principle]
    UP --> CP[Complementarity]
    WE --> PD[Probability Density]
    WE --> NO[Normalization]
    TD --> QD[Quantum Dynamics]
    TI --> EE[Energy Eigenvalues]
```

### Architecture Flow

```mermaid
flowchart LR
    A[PDF Input] --> B[OCR & Layout]
    B --> C[Text Extraction]
    C --> D[Chunking]
    D --> E[Embeddings]
    E --> F[(Vector DB)]
    D --> G[LLM Pipeline]
    F --> H[Semantic Search]
    G --> I[Markdown Notes]
    G --> J[Flashcards]
    G --> K[Quiz]
    G --> L[Mermaid Diagrams]
    G --> M[Mind Maps]
```

### State Diagram: Document Processing States

```mermaid
stateDiagram-v2
    [*] --> Uploaded
    Uploaded --> Queued
    Queued --> Processing
    Processing --> OCR_Stage
    OCR_Stage --> Chunking
    Chunking --> Embedding
    Embedding --> LLM_Processing
    LLM_Processing --> Notes_Generated
    LLM_Processing --> Flashcards_Generated
    LLM_Processing --> Quiz_Generated
    Notes_Generated --> Complete
    Flashcards_Generated --> Complete
    Quiz_Generated --> Complete
    Complete --> [*]
    Processing --> Failed
    Failed --> Queued
    Failed --> [*]
```

### Gantt: Typical Processing Timeline

```mermaid
gantt
    title Document Processing (100-page PDF)
    dateFormat  X
    axisFormat %s
    section Preprocessing
    OCR & Layout         : 0, 15s
    Text Extraction      : 5s, 10s
    section AI Pipeline
    Chunking             : 10s, 12s
    Embeddings           : 12s, 25s
    LLM Summary          : 25s, 50s
    section Generation
    Notes                : 50s, 60s
    Flashcards           : 55s, 65s
    Quiz                 : 60s, 70s
    Mind Map            : 60s, 68s
```

### Class Diagram: Knowledge Structure

```mermaid
classDiagram
    class Document {
        +String title
        +String source
        +String raw_text
        +process()
        +getNotes()
        +getFlashcards()
    }
    class Note {
        +String content
        +String[] tags
        +export()
    }
    class Flashcard {
        +String front
        +String back
        +String[] tags
        +scheduleReview()
    }
    class Quiz {
        +Question[] questions
        +generate()
        +grade()
    }
    class MindMap {
        +Node root
        +render()
        +exportMermaid()
    }
    class Embedding {
        +float[] vector
        +String text
        +search(query)
    }
    Document "1" --> "*" Note
    Document "1" --> "*" Flashcard
    Document "1" --> "1" Quiz
    Document "1" --> "1" MindMap
    Document "1" --> "*" Embedding
```
