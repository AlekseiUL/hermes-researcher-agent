---
name: markitdown-document-ingestion
description: Convert public research documents and mixed file formats into Markdown before evidence review. Use for PDF, DOCX, PPTX, XLSX, HTML, CSV/JSON/XML, EPUB, ZIP bundles, and document intake before summaries, source ledgers, or research briefs.
version: 1.0.0
author: Aleksei Ulianov / Sprut_AI
license: MIT
metadata:
  hermes:
    tags: [documents, markdown, pdf, docx, pptx, xlsx, ingestion, research]
    related_skills: [research-intelligence]
---

# MarkItDown Document Ingestion

## When to use

Use this skill when a research task includes a document or file that should become readable Markdown before analysis:

- public PDFs, reports, whitepapers, policy files, manuals, or papers;
- DOCX / PPTX / XLSX files shared as research sources;
- HTML files, CSV, JSON, XML, EPUB;
- trusted small ZIP bundles of public documents after size/file-count inspection;
- source packs that need to feed a source ledger or research brief.

The goal is not to make the document “true”. The goal is to create a readable analysis copy, then run the normal research evidence gate.

## Recommended local tool

Microsoft MarkItDown is the preferred lightweight converter when available:

```bash
markitdown input.pdf -o output.md
markitdown input.docx -o output.md
markitdown input.pptx -o output.md
```

If the CLI is not installed, install it in your own environment according to the upstream project docs, for example in a local virtual environment:

```bash
python3 -m pip install markitdown
```

Do not put credentials or private documents into third-party services during conversion unless the user explicitly approves that path.

## Safe workflow

1. Confirm the document is in scope for the research task.
2. Convert one explicit file, not a broad directory.
3. For archives, inspect file count, total size, and paths before extraction or conversion; reject path traversal, huge archives, and unknown nested content.
4. Save the Markdown copy under a task-specific working folder.
5. Check the output before relying on it.
6. Cite the original document as source-of-truth; Markdown is only an analysis copy.

Example:

```bash
mkdir -p research-artifacts/document-ingestion
markitdown ./sources/report.pdf -o ./research-artifacts/document-ingestion/report.md
wc -c ./research-artifacts/document-ingestion/report.md
sed -n '1,80p' ./research-artifacts/document-ingestion/report.md
```

## Verification after conversion

Check for common failure modes:

- empty or tiny Markdown output;
- only metadata but no body;
- garbled text or broken Cyrillic/Unicode;
- missing pages, tables, speaker notes, or slides;
- tables converted as unreadable plain text;
- scanned PDF produced almost no text;
- private data accidentally included in the output.

If the output is weak, say so in the research brief instead of pretending the document was fully parsed.

## OCR and scanned PDFs

MarkItDown is useful for many text-based documents, but scanned PDFs may need OCR. If the PDF appears to be mostly images:

- label the conversion as degraded;
- try another local OCR-capable tool if available;
- ask for approval before using external OCR or LLM-vision services on private/sensitive documents;
- keep the original PDF as source-of-truth.

## Evidence gate integration

After conversion, continue with the research workflow:

```text
Document -> Markdown analysis copy -> source ledger -> evidence gate -> decision brief
```

In the final brief, include:

```text
Document ingestion:
- original: <file/source>
- converted copy: <path if saved>
- status: complete / partial / OCR-needed / degraded
- caveat: <tables/pages/images/comments that may be missing>
```

## Boundaries

Allowed by default:

- public documents provided by the user or collected from public sources;
- local conversion into Markdown;
- summaries and evidence extraction from the converted text.

Requires explicit approval:

- private, legal, financial, medical, HR, customer, or account-export documents;
- uploading files to external OCR/LLM/document services;
- unpacking archives unless provenance is trusted and size/file-count/path inspection has passed;
- batch conversion across broad directories;
- converting ZIP/archive contents from unknown provenance, nested archives, or archives with suspicious paths;
- saving converted copies into shared/public locations.

Forbidden:

- converting credential stores, browser profiles, cookies, `.env` files, auth exports, session dumps, or private logs into general reports;
- treating converted Markdown as legally authoritative when the original document is the real source;
- hiding conversion gaps from the final answer.
