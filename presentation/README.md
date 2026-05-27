# Presentation assets

This directory ships everything the live talk needs.

## Files

| File | Purpose |
|------|---------|
| `slides.md` | Marp deck, PT-BR, Cataldi Consultoria palette. Source of truth. |
| `speaker-notes.md` | Click-by-click runbook for the segmented demo, in PT-BR. |
| `README.md` | This file. |

## Talk metadata

- **Event**: Dengo · TDC AI Tech Circle.
- **Date**: 28 May 2026.
- **Audience**: ~38 senior Brazilian leaders (C-level, Heads, Directors)
  from B3, Bradesco, BV, BB, BTG, Pan, Safra, Braskem, CPFL, Fiesp,
  Interplayers, Itaú, PAGBANK, Petrobras, Prodesp, SENAI-SP, SESI-SP,
  Stone, UOL, XP.
- **Title**: Skill-first AI: menos agentes, mais capacidades inteligentes.
- **Duration**: 35–40 min including Q&A.

## Building the deck

### Marp CLI (recommended)

```powershell
# install once
npm install -g @marp-team/marp-cli

# preview (auto-reloads)
marp -w slides.md

# export HTML
marp slides.md -o slides.html

# export PDF
marp slides.md --pdf -o slides.pdf

# export PowerPoint (useful for venue projectors that fight HTML)
marp slides.md --pptx -o slides.pptx
```

### Inside VS Code

Install the **Marp for VS Code** extension. Open `slides.md`. Use the
preview pane to walk slide by slide while editing speaker notes side-by-side.

### Brand palette

The CSS in the deck frontmatter uses the Cataldi Consultoria palette only:

- `--brand-teal: #61AEBE` — titles, CTA emphasis, demo headers
- `--brand-slate: #617595` — H1/H2 color, body emphasis
- `--brand-mint: #50C19B` — success / outcome chips
- `--brand-fog: #E6E7E8` — light surfaces
- `--brand-ink: #373435` — body text, dark backgrounds

Font fallbacks: `Inter`, then `Segoe UI`, then `Calibri`.
Monospace: `JetBrains Mono`, then `Cascadia Mono`.

The logo (`LogoBrain.jpg`) is **not** committed because the repo is public.
Add it locally if needed and reference it via `background-image` in a slide.

## Demo segmentation

Every demo slide is annotated `<!-- _class: demo -->` and ends with a
`🎯 Voltar para a apresentação antes de continuar` cue. **Honor the cue.**

| Slide | Demo target | Duration |
|-------|-------------|----------|
| 6     | Foundry portal — `finance-orchestrator` | ~3 min |
| 9     | Repo docs + contract code | ~3 min |
| 11    | `pytest tests/test_governance.py -v` | ~2 min |
| 13    | Foundry portal — `hr-orchestrator` (reuse) | ~2 min |

If a demo fails, jump to the next slide and use the screenshots under
`_fallback/`. Do not improvise the path back to the deck.

## Fallback assets

Create these before the talk and put them in `_fallback/`:

- `foundry-finance-trace.png` — Foundry tool-call trace for the finance demo.
- `repo-contracts-screenshot.png` — `skill.py` open in VS Code.
- `pytest-governance.txt` — `pytest -v` output captured to text.
- `foundry-hr-trace.png` — Foundry tool-call trace for the HR demo.

These are gitignored so they can carry internal screenshots safely.

## Distribution

The deck is part of the public repo. Anyone who attends can clone, read
the speaker notes, and reproduce the demo end-to-end. That is intentional —
the value of the talk is the conversation it starts in their teams, not
the secret sauce of the slides.
