---
marp: true
theme: default
size: 16:9
paginate: true
backgroundColor: "#FFFFFF"
color: "#373435"
header: "**Skill-first AI** · Dengo · 28 mai 2026"
footer: "Ricardo Cataldi · @cataldir · github.com/Cataldir/skill-first-ai"
style: |
  :root {
    --brand-teal: #61AEBE;
    --brand-slate: #617595;
    --brand-mint: #50C19B;
    --brand-fog: #E6E7E8;
    --brand-ink: #373435;
  }
  section {
    font-family: "Inter", "Segoe UI", "Calibri", sans-serif;
    color: var(--brand-ink);
    padding: 64px 80px;
  }
  h1, h2, h3 {
    color: var(--brand-slate);
    font-weight: 700;
    letter-spacing: -0.01em;
  }
  h1 { font-size: 56px; line-height: 1.1; }
  h2 { font-size: 44px; }
  h3 { font-size: 28px; }
  strong { color: var(--brand-teal); }
  em { color: var(--brand-slate); font-style: italic; }
  code {
    background: var(--brand-fog);
    color: var(--brand-ink);
    border-radius: 4px;
    padding: 2px 6px;
    font-family: "JetBrains Mono", "Cascadia Mono", monospace;
  }
  pre {
    background: var(--brand-ink);
    color: var(--brand-fog);
    border-radius: 8px;
    padding: 16px 20px;
    font-size: 22px;
  }
  pre code { background: transparent; color: inherit; padding: 0; }
  blockquote {
    border-left: 6px solid var(--brand-teal);
    padding-left: 20px;
    color: var(--brand-slate);
    font-style: italic;
  }
  ul, ol { line-height: 1.55; }
  table { border-collapse: collapse; font-size: 24px; }
  th, td { border: 1px solid var(--brand-fog); padding: 10px 14px; text-align: left; }
  th { background: var(--brand-slate); color: white; }
  section.demo {
    background: var(--brand-ink);
    color: var(--brand-fog);
  }
  section.demo h1, section.demo h2, section.demo h3 { color: var(--brand-teal); }
  section.demo strong { color: var(--brand-mint); }
  section.demo blockquote {
    border-left-color: var(--brand-mint);
    color: var(--brand-fog);
  }
  section.title {
    background: linear-gradient(135deg, var(--brand-slate) 0%, var(--brand-ink) 100%);
    color: var(--brand-fog);
  }
  section.title h1 { color: white; font-size: 68px; }
  section.title h3 { color: var(--brand-teal); }
  section.question {
    background: var(--brand-fog);
  }
  section.question h2 { color: var(--brand-slate); font-size: 52px; }
  .chip {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    background: var(--brand-mint);
    color: white;
    font-weight: 600;
    font-size: 18px;
  }
  .chip.warn { background: var(--brand-teal); }
  .chip.dark { background: var(--brand-slate); }
  .cue {
    margin-top: 36px;
    padding: 18px 22px;
    border: 2px dashed var(--brand-teal);
    border-radius: 12px;
    font-size: 22px;
  }
---

<!-- _class: title -->

# Skill-first AI

### Menos agentes. Mais capacidades inteligentes.

**Ricardo Cataldi**
GBB Senior Cloud Solution Architect · Microsoft
Conselheiro acadêmico · FIAP / IBM

Dengo · TDC AI Tech Circle · 28 mai 2026

---

## Antes de começar — uma pergunta honesta

> Quantos agentes a sua empresa já criou nos últimos 12 meses?

Conte os pilotos. Conte os PoCs. Conte os "Copilot for X" que a área de TI
construiu para uma diretoria específica. Conte os bots de RH, de financeiro,
de jurídico, de atendimento.

**Não é trick question.** É o ponto de partida.

Se a resposta começa com "uns sete, oito…", a próxima pergunta importa mais
do que parece: **quantos deles fazem as mesmas seis coisas em prompts ligeiramente
diferentes?**

---

## A armadilha do "um agente por área"

<div class="chip warn">Padrão observado em quase toda enterprise hoje</div>

| Área | Agente | O que ele faz por dentro |
|------|--------|---------------------------|
| RH | Agente de RH | consulta política · valida permissão · busca documento · abre chamado |
| Financeiro | Agente Financeiro | consulta política · valida permissão · busca documento · abre chamado |
| Jurídico | Agente Jurídico | consulta política · valida permissão · busca documento · abre chamado |
| TI | Agente de Acessos | consulta política · valida permissão · busca documento · abre chamado |
| Atendimento | Agente CS | consulta política · valida permissão · busca documento · abre chamado |

Cinco agentes. **Vinte cópias** das mesmas quatro capacidades.
Cinco prompts ligeiramente diferentes. Zero auditoria compartilhada.

---

## Vocabulário — antes que a gente concorde, precisamos separar

| Termo | O que é | O que **não** é |
|-------|---------|-----------------|
| **Automação tradicional** | fluxo determinístico, regras fixas | inteligente |
| **Skill (capacidade)** | função tipada, versionada, governada | conversa |
| **Workflow** | orquestração explícita de skills | adivinhação |
| **Agente** | composição autônoma de skills + memória | bot de FAQ |

> Quando o time fala "agente", costuma estar misturando os quatro.
> Cada um exige um nível diferente de governança.

---

## Decompondo um "agente financeiro" genérico

Antes de pedir "crie um agente financeiro", responda:
**quais capacidades já deveriam existir?**

Pelo menos seis, todas reutilizáveis:

1. `policy_lookup` — consultar política
2. `permission_check` — validar permissão
3. `document_search` — buscar documentos
4. `justification_draft` — gerar justificativa
5. `ticket_open` — abrir chamado
6. `evidence_log` — registrar evidência

**Nenhuma dessas é específica de finanças.**
RH precisa das seis. TI precisa das seis. Jurídico precisa das seis.

---

<!-- _class: demo -->

## Demo 1 — Foundry portal

<div class="chip">demo segmentada · ~3 min</div>

**O que vou mostrar**

- Um **prompt agent** no Foundry chamado `finance-orchestrator`.
- Seis tools MCP, expostas via APIM AI Gateway, vindas do registry.
- Um turno conversacional: *"quero reembolso de USD 1800 para visitar um cliente novo"*.
- A sequência de tool calls aparecendo: `policy_lookup` → `permission_check` →
  `document_search` → `justification_draft` → `ticket_open` → `evidence_log`.

<div class="cue">
🎯 <strong>Voltar para a apresentação antes de continuar.</strong>
A pergunta agora é: <em>o que faz aquelas seis ferramentas serem reutilizáveis?</em>
</div>

---

## O contrato — o que faz uma capability ser reutilizável

Quatro trabalhos. Sempre os mesmos.

```python
class BaseSkill(abc.ABC, Generic[InputT, OutputT]):
    manifest: ClassVar[SkillManifest]   # identidade
    InputSchema: ClassVar[type[BaseModel]]   # tradução
    OutputSchema: ClassVar[type[BaseModel]]  # tradução
    def run(self, payload, *, correlation_id=None) -> SkillResult:
        ...   # falha categorizada + trace de evidência
```

1. **Identidade** — nome estável + versão semântica que dá pra fixar.
2. **Tradução** — Pydantic converte o que o agente mandou em modelo de domínio.
3. **Falha categorizada** — `OK · INVALID_INPUT · REFUSED · TEMPORARY_FAILURE`.
4. **Evidência** — `SkillTrace` com correlation id, latência, categoria.

---

## O resultado é monótono — e isso é uma qualidade

```python
class SkillResult(BaseModel, Generic[OutputT]):
    category: ResultCategory
    output: OutputT | None
    message: str
    trace: SkillTrace
```

Todo consumidor — agente Foundry, servidor MCP, FastAPI interno, import direto
em Python — recebe **o mesmo envelope**.

> Se a sua skill precisa de um "modo especial" para um agente específico,
> ela ainda não é uma skill. É um pedaço do agente disfarçado.

---

<!-- _class: demo -->

## Demo 2 — Repositório

<div class="chip">demo segmentada · ~3 min</div>

**O que vou mostrar**

- `src/skill_first_ai/contracts/skill.py` — `BaseSkill`, `SkillManifest`, `ResultCategory`.
- `src/skill_first_ai/skills/policy_lookup.py` — uma skill real, ~70 linhas.
- `src/skill_first_ai/registry/registry.py` — o registry e o `default_registry()`.
- `src/skill_first_ai/foundry/mcp_server.py` — como vira MCP server num único arquivo.

<div class="cue">
🎯 <strong>Voltar para a apresentação antes de continuar.</strong>
A próxima pergunta é: <em>como a gente impede que essas skills virem bagunça
em seis meses?</em>
</div>

---

## Governança — testar, versionar, governar

Três coisas tornam o registry confiável o suficiente para várias áreas usarem:

<div class="chip dark">testar</div> **Schema golden** — qualquer mudança no input
de uma skill é detectada como drift e exige bump de versão deliberado.

<div class="chip dark">versionar</div> **Semver no manifesto** — agentes fixam
versão. Skill nova nasce em `1.0.0`; breaking change vira `2.0.0`.

<div class="chip dark">governar</div> **Manifesto obrigatório** — sem `owner`,
sem `description`, sem `side_effects` ou `pii` declarados, a skill **nem entra**
no registry.

> A barreira não é técnica. É social.
> O contrato escrito força o time a decidir antes de publicar.

---

<!-- _class: demo -->

## Demo 3 — Governança rodando

<div class="chip">demo segmentada · ~2 min</div>

**O que vou mostrar**

```powershell
uv run pytest tests/test_governance.py -v
```

- `test_skill_has_complete_manifest` — owner, descrição, versão.
- `test_skill_declares_schemas` — `extra='forbid'` no input.
- `test_side_effecting_skills_require_pii_review` — side-effect implica PII review.
- `test_skill_input_schema_matches_golden` — snapshot do JSON schema.

<div class="cue">
🎯 <strong>Voltar para a apresentação antes de continuar.</strong>
A última peça é a mais importante: <em>por que isso muda o que a gente discute
em comitê?</em>
</div>

---

## Reuso real — o teste do segundo agente

O mesmo registry. Outro `system_prompt`. **Agente de RH pronto.**

```yaml
name: hr-orchestrator
tools:
  - policy_lookup       # mesma skill, manifesto idêntico
  - permission_check    # mesma skill, manifesto idêntico
  - document_search     # mesma skill, manifesto idêntico
  - justification_draft # mesma skill, manifesto idêntico
  - ticket_open         # mesma skill, requires_human_approval: true
  - evidence_log        # mesma skill, append-only
```

> Quando o reuso aparece, **a próxima conversa em comitê muda**.
> Não é mais "vamos criar mais um agente". É "qual capacidade está faltando?"

---

<!-- _class: demo -->

## Demo 4 — Foundry portal, segundo agente

<div class="chip">demo segmentada · ~2 min</div>

**O que vou mostrar**

- Prompt agent `hr-orchestrator` consumindo **as mesmas seis tools MCP**.
- Mesmo turno conversacional, contexto diferente: *"quero solicitar 18 dias de férias em julho"*.
- Mesma sequência de tool calls. Resultado diferente porque a política e a
  permissão são diferentes — **as skills são iguais**.

<div class="cue">
🎯 <strong>Voltar para a apresentação para fechar.</strong>
A última pergunta é a que mais incomoda em comitê.
</div>

---

## Anti-padrões — o que eu vejo dar errado

<div class="chip warn">vanity agent</div>
Cada diretoria pede "o meu agente". Quando você abre, é a mesma busca + a mesma
política, com outro nome. Não construa. Mostre o agente vizinho.

<div class="chip warn">skill-shaped agent</div>
Time chama de "agente" o que é só uma função tipada. Promova para skill, registre,
versione. Vira ativo da empresa.

<div class="chip warn">orchestrator-shaped skill</div>
Skill que internamente faz três coisas (chama API, formata, escreve em banco).
Quebre em três. Cada uma tem dono diferente.

<div class="chip warn">silent retry</div>
Skill que engole erro e devolve `OK` "vazio". Use `TEMPORARY_FAILURE`. O agente
decide se tenta de novo. **Você não tira a decisão dele.**

---

<!-- _class: question -->

## A pergunta que define o roadmap dos próximos 12 meses

# A empresa precisa de **mais agentes**

# ou de **melhores capacidades reutilizáveis**?

<br>

> A resposta honesta para a maioria das empresas hoje
> é **a segunda** — e ninguém está medindo isso.

---

## O que levar para segunda-feira

1. **Inventário de agentes.** Liste o que já existe. Pinte os duplicados.
2. **Inventário de capacidades.** Quais skills os agentes existentes chamam?
3. **Registry mínimo.** Comece com 5–6 capacidades verdadeiras. Não 50.
4. **Contrato escrito.** `SkillManifest` + `ResultCategory` em um README.
5. **Primeiro teste de governança.** "Sem owner, não registra." Vire regra.
6. **Foundry como destino, não como ponto de partida.** Prompt agents em cima
   do MCP server, não o contrário.

> O próximo agente que vocês forem aprovar vale a pergunta:
> **"qual skill nova esse agente exige?"** Se a resposta for "nenhuma",
> talvez ele já exista.

---

<!-- _class: title -->

# Menos agentes.

# Mais capacidades.

<br>

**Código, slides e notas:**
`github.com/Cataldir/skill-first-ai`

**Conversa em aberto:**
`linkedin.com/in/cataldir` · `medium.com/@cataldi.ricardo`

Obrigado.
