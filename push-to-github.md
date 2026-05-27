# Pushing to `github.com/Cataldir/skill-first-ai`

Step-by-step. Run in PowerShell from the parent folder you want the repo
to live in (e.g. `C:\Users\ricar\Github\`).

## 1. Move the staging folder out of the knowledge repo

The repo was bootstrapped inside `i/tmp/skill-first-ai-dengo/` because of
filesystem-tool scoping. Move it where it belongs before initializing git.

```powershell
# In PowerShell, from C:\Users\ricar\Github\
Move-Item `
  "C:\Users\ricar\Github\i\tmp\skill-first-ai-dengo" `
  "C:\Users\ricar\Github\skill-first-ai"

Set-Location "C:\Users\ricar\Github\skill-first-ai"
```

## 2. Initialize git

```powershell
git init -b main
git add .
git commit -m "skill-first-ai: companion repo for the AI Tech Circle talk"
```

## 3. Create the public repo and push

If you have GitHub CLI installed (recommended):

```powershell
gh repo create Cataldir/skill-first-ai `
  --public `
  --source . `
  --description "Fewer agents, more reusable capabilities. A skill-first reference implementation for Microsoft Foundry." `
  --push
```

Otherwise, create the repo manually at https://github.com/new under the
`Cataldir` account, then:

```powershell
git remote add origin https://github.com/Cataldir/skill-first-ai.git
git push -u origin main
```

## 4. Sanity check

```powershell
gh repo view Cataldir/skill-first-ai --web
```

Confirm:

- README renders.
- `presentation/slides.md` is visible.
- `src/skill_first_ai/foundry/agent_definition.yaml` is visible.

## 5. Tag the talk release (optional, helps citations from the deck)

```powershell
git tag -a v1.0.0-aitc -m "AI Tech Circle talk, 28 May 2026"
git push origin v1.0.0-aitc
```

## 6. Sanity check the demo end-to-end

```powershell
uv sync
uv run pytest -v
uv run uvicorn skill_first_ai.foundry.mcp_server:app --port 8080
```

In another terminal:

```powershell
Invoke-WebRequest http://localhost:8080/mcp/tools | Select-Object -ExpandProperty Content
```

You should see six tools published.

## 7. Cleanup of the staging path

After the move, the original folder under `i/tmp/skill-first-ai-dengo/`
is gone. Nothing more to do in the knowledge repo.

If you want to leave a pointer in the knowledge repo (for your own
journal):

```powershell
# from C:\Users\ricar\Github\i\
"`nSee https://github.com/Cataldir/skill-first-ai" >> tmp\skill-first-ai-dengo.note
```

That note is in `tmp/` and is gitignored — it disappears on the next clean.
