# Speaker notes — Skill-first AI · Dengo 28 mai 2026

**Duração-alvo:** 35–40 minutos com Q&A.
**Plateia:** ~38 lideranças seniores brasileiras (C-level, Heads, Diretores)
de B3, Bradesco, BV, BB, BTG, Pan, Safra, Braskem, CPFL, Fiesp, Interplayers,
Itaú, PAGBANK, Petrobras, Prodesp, SENAI-SP, SESI-SP, Stone, UOL, XP.
**Idioma:** PT-BR. Inglês só nos nomes de skills, manifestos e arquivos.
**Energia:** filósofo grumpy. Pausa nas perguntas. Não venda. Conte.

## Regra de ouro

> Slides são o guia. Demos voltam para os slides **antes** de qualquer transição.
> Se a demo travar, o slide seguinte resolve o ponto. **Não improvisar a transição.**

## Setup antes de entrar (15 min antes)

1. Ambiente local rodando:
   ```powershell
   uv run uvicorn skill_first_ai.foundry.mcp_server:app --port 8080
   ```
2. APIM AI Gateway com o MCP source `skill-first-mcp` apontado para a URL pública (ngrok, dev tunnel ou ACA).
3. Foundry portal aberto em duas abas:
   - **Aba A:** prompt agent `finance-orchestrator`.
   - **Aba B:** prompt agent `hr-orchestrator` (mesmo MCP source, system prompt diferente).
4. Terminal pronto na pasta do repo, virtualenv ativado, `pytest -q` rodando verde.
5. Slides em fullscreen no projetor, **Marp Preview** aberto no laptop espelhando.
6. Screenshots de fallback prontas em `presentation/_fallback/` (caso a demo falhe).

---

## Slide 1 — Título (0:00 – 0:45)

- Apresente-se rápido: GBB Senior CSA na Microsoft, conselheiro acadêmico FIAP/IBM, autor de algumas dezenas de posts e cursos sobre arquiteturas agênticas.
- **Não** liste credenciais. O importante é que isso aqui sai de prática, não de slide deck corporativo.
- Frase de abertura sugerida:
  > "Eu vou tentar não vender nada hoje. Vou contar o que eu venho vendo dar errado quando empresas adotam agentes em escala — e o que parece dar certo."

## Slide 2 — A pergunta honesta (0:45 – 2:30)

- **Faça a pergunta literal.** Espere alguém responder (alguém sempre responde).
- Quando o número aparecer ("uns oito"), repita em voz alta e siga: *"quantos deles fazem as mesmas seis coisas em prompts ligeiramente diferentes?"*
- **Pausa**. Deixe o desconforto existir. É o gancho do resto da palestra.

## Slide 3 — A armadilha (2:30 – 5:00)

- Caminhe pela tabela. Aponte para a coluna da direita.
- Diga: *"isso aqui não é hipótese. É o que eu vejo em quase todo cliente nos últimos doze meses."*
- Frase para fixar: *"cinco agentes, vinte cópias das mesmas quatro capacidades, cinco prompts ligeiramente diferentes."*

## Slide 4 — Vocabulário (5:00 – 7:00)

- Caminhe linha por linha.
- O ponto não é o glossário; é mostrar que **a maior parte das discussões sobre "agente" mistura os quatro**.
- Use a frase: *"governança de chatbot é uma coisa. Governança de agente autônomo é outra. Quando o time não separa, a governança aplicada é sempre a errada."*

## Slide 5 — Decomposição (7:00 – 9:00)

- Liste as seis. Devagar. Cada uma com uma pausa.
- Frase para fechar antes da demo: *"nenhuma dessas seis é específica de finanças. Repare quando vocês forem mapear as suas."*

## Slide 6 — DEMO 1 · Foundry portal (9:00 – 12:00)

**Aba A — `finance-orchestrator`**

1. Mostre o prompt agent na lista. Diga: *"é só um prompt agent. Não tem código próprio."*
2. Abra a configuração. Mostre os seis tools no painel. Aponte para o `mcp_source: skill-first-mcp`.
3. Vá para o playground. Digite (devagar, em PT-BR):
   > Quero solicitar reembolso de USD 1800 de uma viagem para visitar um cliente novo.
4. **Pause antes de enviar.** Aponte para o painel de traces. Diga: *"vocês vão ver seis tool calls, nessa ordem."*
5. Envie. Comente cada tool call: política → permissão → documento → justificativa → ticket → evidência.
6. Pegue o `ticket_id` na resposta e mostre que o `evidence_log` tem o mesmo correlation id.

**Transição obrigatória:**
> "Voltando para a apresentação. A pergunta agora é: **o que faz aquelas seis ferramentas serem reutilizáveis?**"

## Slide 7 — O contrato (12:00 – 14:00)

- Leia o código devagar. Não economize tempo aqui.
- Para cada um dos quatro pontos, use a versão verbal:
  - *"Identidade: a única coisa que separa uma skill de um pedaço de código solto é ter nome e versão estáveis."*
  - *"Tradução: nada entra antes de virar tipo. Pydantic não está aqui por capricho — é a barreira anti-prompt-injection mais barata que existe."*
  - *"Falha categorizada: a skill nunca pede para o modelo decidir o que fazer com erro. Ela devolve uma categoria nomeada e quem decide é o orquestrador."*
  - *"Evidência: o `SkillTrace` é o que vai sobrar quando o auditor pedir relatório."*

## Slide 8 — Resultado monótono (14:00 – 15:00)

- Frase para fixar: *"se a sua skill precisa de um modo especial para um agente específico, ela ainda não é uma skill. É um pedaço do agente disfarçado."*
- Esse é o slide que ganha o time de governança.

## Slide 9 — DEMO 2 · Repositório (15:00 – 18:00)

**Tela única, VS Code, fonte ampliada (Ctrl+= duas vezes).**

1. Abra `src/skill_first_ai/contracts/skill.py`. Mostre a `BaseSkill`. Aponte para `run`. Diga: *"esse método aqui é o único lugar onde tempo, erro e trace são montados. As skills concretas não duplicam isso."*
2. Abra `src/skill_first_ai/skills/policy_lookup.py`. Sessenta e poucas linhas. Mostre o manifesto. Mostre o `_execute`.
3. Abra `src/skill_first_ai/registry/registry.py`. Aponte para `default_registry()`. Diga: *"se uma skill não está aqui, nenhum agente pode chamar. Toda a governança começa nesse `register()`."*
4. Abra `src/skill_first_ai/foundry/mcp_server.py`. Mostre os dois endpoints: `list_tools` e `call_tool`.

**Transição obrigatória:**
> "Voltando para a apresentação. A próxima pergunta é: **como a gente impede que essas skills virem bagunça em seis meses?**"

## Slide 10 — Governança (18:00 – 20:00)

- Caminhe pelos três blocos. Pause em cada chip.
- Frase para fechar: *"a barreira não é técnica. É social. O contrato escrito força o time a decidir antes de publicar."*

## Slide 11 — DEMO 3 · Governança rodando (20:00 – 22:00)

**Terminal grande. `pytest -v`.**

```powershell
uv run pytest tests/test_governance.py -v
```

1. Mostre os nomes dos testes passando. Leia em voz alta:
   - `test_skill_has_complete_manifest`
   - `test_skill_declares_schemas`
   - `test_side_effecting_skills_require_pii_review`
   - `test_skill_input_schema_matches_golden`
2. Quebre um propositalmente (ou tenha um branch `demo/broken-skill` pronto): adicione uma skill sem `owner` em uma cópia local e rode de novo.
3. Mostre o erro de governança. Diga: *"essa skill nem entra. O CI rejeita."*

**Transição obrigatória:**
> "Voltando para a apresentação. A última peça é a mais importante: **por que isso muda o que a gente discute em comitê?**"

## Slide 12 — Reuso real (22:00 – 24:00)

- Mostre o YAML. Aponte para a frase: "mesmas seis skills".
- Diga: *"esse é o único momento que importa em comitê. O segundo agente custa quase nada quando o primeiro foi feito direito."*

## Slide 13 — DEMO 4 · Foundry portal, segundo agente (24:00 – 26:30)

**Aba B — `hr-orchestrator`**

1. Abra o prompt agent `hr-orchestrator`. Aponte para o painel de tools — os mesmos seis.
2. Vá para o playground. Digite:
   > Quero solicitar 18 dias de férias em julho.
3. Mesma sequência de tool calls aparece. Aponte: política diferente, permissão diferente, **skills iguais**.
4. **Não fique muito tempo.** É um beat curto que prova o ponto.

**Transição obrigatória:**
> "Voltando para a apresentação para fechar. A última pergunta é a que mais incomoda em comitê."

## Slide 14 — Anti-padrões (26:30 – 29:00)

- Caminhe pelos quatro. Use exemplos curtos da própria plateia se possível ("muitos de vocês têm um agente chamado X que é exatamente isto").
- Frase para fechar: *"a maior parte dos quatro acontece porque ninguém parou para escrever o contrato antes."*

## Slide 15 — A pergunta central (29:00 – 30:30)

- **Pause longa antes de virar o slide.**
- Leia em voz alta, devagar:
  > "A empresa precisa de mais agentes, ou de melhores capacidades reutilizáveis?"
- Frase de fechamento: *"a resposta honesta para a maioria das empresas hoje é a segunda — e ninguém está medindo isso."*

## Slide 16 — O que levar para segunda (30:30 – 32:30)

- Caminhe pela lista. Frase para cada item:
  1. *"Conte. Não vai doer pintar os duplicados."*
  2. *"Liste as capacidades por trás. Provavelmente são menos do que parece."*
  3. *"Cinco ou seis skills. Não cinquenta. Esse repositório aqui são seis."*
  4. *"O contrato cabe num README de uma página."*
  5. *"O primeiro teste que vocês escrevem é o de governança. Não o funcional."*
  6. *"Foundry como destino. O registry vem primeiro."*

## Slide 17 — Fechamento (32:30 – 33:30)

- *"Menos agentes. Mais capacidades. Obrigado."*
- Mostre o link do repo. Não fique mais de 10 segundos.

## Q&A (33:30 – 40:00)

**Perguntas prováveis e respostas curtas:**

- *"E quando a gente já tem 12 agentes em produção?"* → Não refatore os 12. Construa o registry com as skills que eles já chamam. Próximo agente novo nasce só consumindo o registry. Migra os antigos por necessidade, não por princípio.
- *"Isso não vira monolito?"* → O registry não é um monolito. É um catálogo. Os ownership ficam por skill, não pelo registry. (Apontar para o campo `owner` no manifesto.)
- *"Foundry suporta isso nativamente?"* → Prompt agents + MCP source via APIM AI Gateway. O repositório mostra. Hosted Agent é opcional para times que querem orquestrador containerizado.
- *"E o custo?"* → Mesma chamada de modelo. O ganho é em código duplicado e revisão de policy.
- *"Como evolui de versão?"* → Semver no manifesto. Agentes pinned na major. Bump major exige migração explícita. Os goldens forçam essa conversa.
- *"E avaliação?"* → Eval por skill (a parte mais barata) e eval do orquestrador (a parte cara). A separação reduz o custo da segunda.
- *"Onde isso quebra?"* → Quando o time tenta colocar lógica de negócio dentro do orquestrador em vez de uma skill. O sinal é "esse passo precisa de um if". Sinal claro de skill faltando.

## Fallback se a demo travar

- **Demo 1 falhou?** Pule direto para o slide 7. Mostre as screenshots em `presentation/_fallback/foundry-finance-trace.png`. *"O Foundry está com lag — mas o trace aparece exatamente assim. Vou passar adiante e a gente volta."*
- **Demo 2 falhou?** Mostre os trechos no slide 7 + 8 e o repositório no GitHub direto. Não enrole.
- **Demo 3 falhou?** Mostre o output salvo em `presentation/_fallback/pytest-governance.txt`. O ponto importante é o **nome** dos testes — não o sucesso na hora.
- **Demo 4 falhou?** Pior caso. Volte para o slide 12 e leia o YAML em voz alta. O ponto é o mesmo.

## Última checagem antes de subir ao palco

- [ ] Notebook na fonte 18+, terminal na fonte 20+.
- [ ] Internet do venue testada com `curl https://api.openai.com` antes do início.
- [ ] APIM API key em variável de ambiente, **não no slide**.
- [ ] Aba B (`hr-orchestrator`) já carregada — não carregar ao vivo.
- [ ] Screenshot de fallback aberta em segundo monitor.
- [ ] Repositório público acessível: `gh repo view Cataldir/skill-first-ai`.
