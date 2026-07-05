# UI Component Library

Every reusable UI component in Khoji, organized by layer.

---

## Layer 1: Design Primitives

### `Button`
```tsx
<Button variant="primary|secondary|ghost|danger" size="sm|md|lg|xl" icon={...} loading disabled>
  Label
</Button>
```
**Props:** variant, size, icon, loading, disabled, onClick, type, fullWidth, tooltip

### `IconButton`
```tsx
<IconButton icon={Search} label="Search" onClick={...} />
```
**Props:** icon, label (aria-label), size, variant, onClick, disabled

### `Input`
```tsx
<Input value={...} onChange={...} placeholder="..." icon={...} error="..." clearable />
```
**Props:** value, onChange, placeholder, icon, error, clearable, type, disabled, autoFocus

### `Textarea`
```tsx
<Textarea value={...} onChange={...} rows={5} maxLength={5000} />
```

### `Select`
```tsx
<Select options={[{value, label}]} value={...} onChange={...} />
```

### `Checkbox`
```tsx
<Checkbox checked={...} onChange={...} label="..." indeterminate />
```

### `Toggle`
```tsx
<Toggle checked={...} onChange={...} label="Dark Mode" />
```

### `Radio`
```tsx
<Radio name="theme" options={[{value, label}]} value={...} onChange={...} />
```

### `Badge`
```tsx
<Badge variant="primary|secondary|success|warning|error|neutral" size="sm|md">
  Label
</Badge>
```

---

## Layer 2: Layout Components

### `AppShell`
```tsx
<AppShell>
  <TopBar />
  <Sidebar />
  <MainArea>
    <Content />
  </MainArea>
  <RightPanel />
  <StatusBar />
</AppShell>
```
**Props:** defaultSidebarOpen, defaultRightPanelOpen

### `Sidebar`
```tsx
<Sidebar collapsed={...} onToggle={...}>
  <SidebarSection label="Library" icon={Library}>
    <SidebarItem icon={FileText} label="Documents" active />
    <SidebarItem icon={Folder} label="Collections" />
  </SidebarSection>
  <SidebarSection label="Tools" icon={Wrench}>
    <SidebarItem icon={Search} label="Search" shortcut="⌘K" />
  </SidebarSection>
</Sidebar>
```

### `TopBar`
```tsx
<TopBar>
  <TopBarLeft>
    <Logo />
    <Breadcrumbs items={[{label, href}]} />
  </TopBarLeft>
  <TopBarCenter>
    <SearchTrigger onClick={...} />
  </TopBarCenter>
  <TopBarRight>
    <IconButton icon={Upload} label="Upload" />
    <UserMenu />
  </TopBarRight>
</TopBar>
```

### `StatusBar`
```tsx
<StatusBar>
  <StatusItem label="Model" value="Llama 3.2" />
  <StatusItem label="Documents" value="12" />
  <StatusItem label="Processing" value="1" progress={0.6} />
</StatusBar>
```

### `Tabs`
```tsx
<Tabs value={activeTab} onChange={setActiveTab}>
  <Tab value="notes" icon={FileText} label="Notes" count={145} />
  <Tab value="flashcards" icon={Layers} label="Flashcards" count={22} />
  <Tab value="quiz" icon={HelpCircle} label="Quiz" count={10} />
  <Tab value="mindmap" icon={GitBranch} label="Mind Map" />
  <Tab value="timeline" icon={Clock} label="Timeline" />
</Tabs>
```

---

## Layer 3: Library Components

### `DocumentCard`
```tsx
<DocumentCard document={doc} onClick={...} onFavorite={...} />
```
**Visual:** Card with file icon, title, metadata (pages, notes, cards), favorite star, status badge

### `DocumentGrid`
```tsx
<DocumentGrid documents={docs} view="grid|list" onDocumentClick={...} />
```

### `UploadZone`
```tsx
<UploadZone onFilesSelected={files => ...} accept=".pdf,.png,.jpg" maxSize={200} />
```
**Visual:** Dashed border drop zone with icon, supported formats list, drag-over glow animation

### `UploadProgress`
```tsx
<UploadProgress file={file} progress={0.65} stage="llm_processing" />
```
**Visual:** Pipeline visualization with 8 stages, current stage pulsing, completed with green checks

### `CollectionList`
```tsx
<CollectionList collections={cols} onSelect={...} onCreate={...} />
```

### `CollectionCard`
```tsx
<CollectionCard collection={col} documentCount={...} />
```

---

## Layer 4: Document Workspace Components

### `DocumentWorkspace`
```tsx
<DocumentWorkspace document={doc}>
  <OutlinePanel sections={sections} activeSection={...} />
  <TabContent value="notes">
    <NotesTab document={doc} />
  </TabContent>
  <TabContent value="flashcards">
    <FlashcardsTab document={doc} />
  </TabContent>
  ...
</DocumentWorkspace>
```

### `OutlinePanel`
```tsx
<OutlinePanel sections={sections} activeSection={...} onSectionClick={...} />
```
**Visual:** Hierarchical list of section headings, highlighting active, scroll-linked

### `NotesTab`
```tsx
<NotesTab documentId={doc.id} editable={true} onEdit={...} />
```
**Visual:** Rendered Markdown with optional edit mode toggle

### `MarkdownRenderer`
```tsx
<MarkdownRenderer content={markdown} readingMode={true} />
```
**Visual:** Styled Markdown with table of contents, LaTeX rendering, Mermaid rendering, code highlighting

### `MarkdownEditor`
```tsx
<MarkdownEditor value={...} onChange={...} onPreview={...} />
```
**Visual:** Split pane (edit/preview) or source-only mode, syntax highlighting

### `FlashcardsTab`
```tsx
<FlashcardsTab documentId={doc.id}>
  <FlashcardFilters />
  <FlashcardList cards={cards} onStartReview={...} />
  <FlashcardGenerator onGenerate={...} />
</FlashcardsTab>
```

### `FlashcardList`
```tsx
<FlashcardList cards={cards} view="grid|list" />
```

### `FlashcardCard`
```tsx
<FlashcardCard card={flashcard} onEdit={...} onDelete={...} />
```
**Visual:** Card with front text, tag badges, difficulty indicator, source reference

---

## Layer 5: Review Components

### `FlashcardReview`
```tsx
<FlashcardReview cards={queue} onComplete={stats => ...} />
```
**Visual:** Full-screen, single card, flip animation, rating buttons

### `FlashcardFlipper`
```tsx
<FlashcardFlipper front="..." back="..." flipped={...} onFlip={...} />
```
**Animation:** 3D rotateY flip with perspective

### `RatingButtons`
```tsx
<RatingButtons onRate={(rating) => ...} />
```
**Visual:** 4 buttons: Again (red), Hard (orange), Good (green), Easy (blue) — each with interval label

### `ReviewStats`
```tsx
<ReviewStats stats={sessionStats} />
```
**Visual:** Cards reviewed, retention rate, time spent, streak, progress chart

---

## Layer 6: Quiz Components

### `QuizTab`
```tsx
<QuizTab documentId={doc.id}>
  <QuizConfig difficulty="medium" count={10} onStart={...} />
  <QuizSession questions={questions} onComplete={...} />
  <QuizHistory sessions={pastSessions} />
</QuizTab>
```

### `QuizConfig`
```tsx
<QuizConfig difficulty="medium" count={10} onStart={startQuiz} />
```
**Visual:** Difficulty slider (easy/medium/hard), count selector (5/10/15/20), start button

### `QuizSession`
```tsx
<QuizSession questions={questions} onComplete={results => ...} />
```
**Visual:** Question card, 4 option buttons, timer, progress bar, submit button, flag for review

### `QuizQuestion`
```tsx
<QuizQuestion question={q} selected={...} onSelect={...} showResult={...} />
```
**Visual:** Question text, option A/B/C/D buttons, correct/incorrect highlight on submit, explanation

### `QuizResult`
```tsx
<QuizResult session={session} />
```
**Visual:** Score percentage, correct/total, time taken, topic breakdown, review missed questions

---

## Layer 7: Diagram Components

### `MindMapTab`
```tsx
<MindMapTab documentId={doc.id}>
  <DiagramViewer diagram={diagram} />
  <DiagramList diagrams={allDiagrams} />
</MindMapTab>
```

### `DiagramViewer`
```tsx
<DiagramViewer mermaidCode="..." type="flowchart" interactive={true} />
```
**Visual:** Rendered Mermaid SVG with zoom, pan, fit-to-screen, export

### `MermaidRenderer`
```tsx
<MermaidRenderer code={mermaidCode} onRender={svg => ...} />
```
**Visual:** Mermaid SVG with error boundary, loading state

### `TimelineTab`
```tsx
<TimelineTab events={events} />
```
**Visual:** Vertical timeline with date markers, event cards, clickable

---

## Layer 8: Chat Components

### `ChatPanel`
```tsx
<ChatPanel documentId={doc.id}>
  <ChatHeader documentTitle="..." />
  <ChatMessages messages={messages} />
  <ChatInput onSend={...} onCommand={...} />
</ChatPanel>
```

### `ChatHeader`
```tsx
<ChatHeader title="AI Chat" contextDocument="Quantum Mechanics" />
```
**Visual:** Title, active document context badge, clear history button, model indicator

### `ChatMessages`
```tsx
<ChatMessages messages={msgs} loading={isLoading} />
```
**Visual:** Scrollable message list, auto-scroll to bottom, streaming token animation

### `ChatMessage`
```tsx
<ChatMessage role="user|assistant" content="..." citations={[...]} />
```
**Visual:** User: right-aligned, primary bg. Assistant: left-aligned, surface bg. Citations as clickable page links

### `ChatInput`
```tsx
<ChatInput onSend={text => ...} disabled={loading} />
```
**Visual:** Text input with send button, slash-command autocomplete, model status indicator

### `StreamingText`
```tsx
<StreamingText tokens={tokenStream} onComplete={...} />
```
**Animation:** Typewriter effect (30ms per token), Markdown rendering in real-time

---

## Layer 9: Knowledge Graph Components

### `KnowledgeGraph`
```tsx
<KnowledgeGraph nodes={nodes} edges={edges} onNodeClick={...} />
```
**Visual:** Force-directed graph with D3.js/Cytoscape, physics simulation, zoom/pan

### `GraphNode`
```tsx
<GraphNode concept={concept} selected={...} highlighted={...} />
```
**Visual:** Circle/diamond/rect based on type, label, color-coded, glow when selected

### `GraphEdge`
```tsx
<GraphEdge source={...} target={...} relationship="..." />
```
**Visual:** Arrow line with relationship label, hover shows tooltip

### `NodeDetailPanel`
```tsx
<NodeDetailPanel concept={concept} />
```
**Visual:** Slide-over panel with concept details, source docs, connections, actions

### `GraphControls`
```tsx
<GraphControls onZoomIn={...} onZoomOut={...} onFit={...} onLayoutChange={...} />
```
**Visual:** Zoom buttons, fit, layout selector (force/hierarchical/radial), search, reset

---

## Layer 10: Search Components

### `SearchModal`
```tsx
<SearchModal open={...} onClose={...} onResultClick={...} />
```
**Visual:** Full-screen overlay, centered search input, results list below, keyboard shortcuts shown

### `SearchInput`
```tsx
<SearchInput value={...} onChange={...} onClear={...} />
```
**Visual:** Input with search icon, clear button, Cmd+K badge, auto-focus

### `SearchResultItem`
```tsx
<SearchResultItem result={result} />
```
**Visual:** Document icon, title, snippet with highlighted match, page number, relevance score bar

### `SearchFilters`
```tsx
<SearchFilters filters={filters} onChange={...} />
```
**Visual:** Chip filters: documents, collections, date range, file type

---

## Layer 11: Processing Components

### `ProcessingModal`
```tsx
<ProcessingModal job={job} onCancel={...} />
```
**Visual:** Modal with pipeline visualization, 8 stages, current progress, time estimate, cancel button

### `PipelineVisualization`
```tsx
<PipelineVisualization stages={stages} currentStage={3} />
```
**Visual:** Horizontal step bar, numbered circles, completed (green check), current (pulsing primary), pending (gray)

### `StageIndicator`
```tsx
<StageIndicator stage={stage} status="completed|active|pending|error" />
```

### `ProgressBar`
```tsx
<ProgressBar value={0.65} variant="primary|success|warning" />
```

---

## Layer 12: Settings Components

### `SettingsDrawer`
```tsx
<SettingsDrawer open={...} onClose={...}>
  <SettingsSection label="General" icon={Settings}>
    <SettingsRow label="Theme">
      <ToggleGroup options={["Light", "Dark", "System"]} />
    </SettingsRow>
  </SettingsSection>
</SettingsDrawer>
```

### `ModelManager`
```tsx
<ModelManager models={models} onDownload={...} onSelect={...} />
```
**Visual:** Model cards per type (OCR, Embedding, LLM), download button, installed badge, size

### `ModelCard`
```tsx
<ModelCard model={model} onDownload={...} selected={...} />
```
**Visual:** Model name, size, status (downloaded/downloading/not-installed), select radio, progress if downloading

---

## Layer 13: Export Components

### `ExportDialog`
```tsx
<ExportDialog open={...} document={doc} onExport={...} />
```

### `ExportFormatPicker`
```tsx
<ExportFormatPicker selected={...} onChange={...} />
```
**Visual:** Grid of format cards with icons, sizes, recommended badge

### `ExportOptions`
```tsx
<ExportOptions format="markdown" options={opts} onChange={...} />
```
**Visual:** Checkboxes for what to include (notes, flashcards, quiz, diagrams, images)

---

## Layer 14: Feedback Components

### `Toast`
```tsx
<Toast message="..." type="success|error|info|warning" action={{label, onClick}} />
```
**Visual:** Slide-in notification, auto-dismiss, action button

### `NotificationCenter`
```tsx
<NotificationCenter notifications={notifs} />
```
**Visual:** Bell icon with unread count, dropdown list of notifications

### `EmptyState`
```tsx
<EmptyState icon={BookOpen} title="No documents" description="..." action={{label, onClick}} />
```
**Visual:** Large icon, title, description, optional action button

### `ErrorState`
```tsx
<ErrorState error={err} onRetry={...} suggestions={[...]} />
```
**Visual:** Error icon, message, suggestions list, retry button

### `Skeleton`
```tsx
<Skeleton variant="text|card|image|circle" width="..." height="..." />
```
**Visual:** Animated placeholder shimmer

### `LoadingOverlay`
```tsx
<LoadingOverlay active={true} message="Processing..." />
```
**Visual:** Semi-transparent overlay with spinner + message

---

## Layer 15: Navigation Components

### `Breadcrumbs`
```tsx
<Breadcrumbs items={[{label: "Library", href: "/"}, {label: "Quantum", href: "/doc/123"}]} />
```

### `Pagination`
```tsx
<Pagination current={1} total={10} onChange={page => ...} />
```

### `DropdownMenu`
```tsx
<DropdownMenu trigger={<Button>Actions</Button>} items={menuItems} />
```

### `ContextMenu`
```tsx
<ContextMenu items={menuItems} onOpen={...} />
```

### `Tooltip`
```tsx
<Tooltip content="Search all documents (⌘K)">
  <SearchButton />
</Tooltip>
```

### `Modal`
```tsx
<Modal open={...} onClose={...} title="..." size="sm|md|lg|xl|full" closeOnOverlayClick>
  {children}
</Modal>
```

### `Drawer`
```tsx
<Drawer open={...} onClose={...} side="left|right" width={360}>
  {children}
</Drawer>
```

---

## Component Hierarchy

```
App
└── AppShell
    ├── TopBar
    │   ├── Logo
    │   ├── Breadcrumbs
    │   ├── SearchTrigger (opens SearchModal)
    │   ├── IconButton (Upload)
    │   └── UserMenu (DropdownMenu)
    ├── Sidebar
    │   ├── SidebarSection (Library)
    │   │   ├── SidebarItem (Documents)
    │   │   └── SidebarItem (Collections)
    │   └── SidebarSection (Learning)
    │       ├── SidebarItem (Flashcards)
    │       └── SidebarItem (Quiz)
    ├── MainArea
    │   ├── LibraryView
    │   │   ├── DocumentGrid / DocumentList
    │   │   ├── DocumentCard
    │   │   └── CollectionList
    │   ├── DocumentWorkspace
    │   │   ├── OutlinePanel
    │   │   ├── Tabs
    │   │   │   ├── NotesTab → MarkdownRenderer / MarkdownEditor
    │   │   │   ├── FlashcardsTab → FlashcardList → FlashcardCard
    │   │   │   ├── QuizTab → QuizConfig → QuizSession → QuizQuestion
    │   │   │   ├── MindMapTab → DiagramViewer → MermaidRenderer
    │   │   │   └── TimelineTab
    │   │   └── ExportDialog
    │   ├── SearchModal
    │   │   ├── SearchInput
    │   │   ├── SearchFilters
    │   │   └── SearchResultItem
    │   └── ProcessingModal → PipelineVisualization
    ├── RightPanel
    │   └── ChatPanel
    │       ├── ChatHeader
    │       ├── ChatMessages → ChatMessage
    │       └── ChatInput
    ├── StatusBar
    └── SettingsDrawer
        ├── SettingsSection
        └── ModelManager → ModelCard
```

## Component Count: 60+ components
