# B2B Prospecting Sales OS

**Version:** 0.9.1 RC  
**Author:** Mitchell Correa / Cyberwolf AI  
**SOP completo:** https://app.notion.com/p/3e9b9257f11881da8dee-fa2b3fd080c2?pvs=204

## ¿Qué es?

**B2B Prospecting Sales OS** es una Skill que convierte la prospección B2B en un proceso **reproducible, auditable y controlado por etapas**.

Está basada en un SOP probado con campañas reales. No es sólo un prompt para “buscar prospectos”: funciona como un **Sales Operating System** que controla estados, fuentes, account isolation, Deep Research, autorizaciones de gasto, consumo de créditos, calidad de evidencia, trabajo multi-cuenta y el Handoff final para Ventas.

Su objetivo es llevar una campaña desde el Campaign Brief hasta un **Prospect Intelligence Book & Sales Handoff** suficientemente completo para que un vendedor pueda trabajar la cuenta sin revisar los chats anteriores.

## ¿Para qué sirve?

Ayuda a responder de forma estructurada:

- qué cuentas cumplen con el ICP;
- cuáles deben priorizarse;
- quiénes son los stakeholders relevantes;
- qué sabemos realmente de la cuenta y qué sigue sin validar;
- qué es evidencia y qué es inferencia;
- cuál es el entry point más razonable;
- qué estrategia y mensaje utilizar;
- qué datos llevar al CRM;
- qué validar durante Discovery.

Está dirigida a Business Development, Account Managers, KAM, SDR, Commercial Directors, Revenue/Commercial Operations, consultores B2B, founders con venta enterprise y equipos de inteligencia comercial.

## Cómo funciona

### Stages 0–7 — Campaign Layer

**0 Campaign Brief** → oferta, geografía, ICP, roles, universo, Tier A y presupuesto de créditos.  
**1 Account Discovery** → identifica empresas objetivo.  
**2 ICP Qualification** → clasifica cuentas sin convertir proxies en hechos.  
**3 Prioritization** → Tier A/B/C como prioridad interna, no intención de compra.  
**4 Decision-Maker Discovery** → stakeholders + Primary / Backup / Escalation.  
**5 Identity Validation** → confirma persona, empresa, cargo y perfil.  
**6 Work Email Enrichment** → sólo con autorización humana explícita.  
**7 Provider Benchmark** → valida calidad antes de escalar.

### Account Fan-Out

Después de Stage 7 cada cuenta se separa:

`ACCOUNT_ISOLATION = TRUE`

La información de una cuenta no puede utilizarse para rellenar huecos de otra.

### Stage 8 — Account Intelligence

Es la única etapa autorizada para **Deep Research**.

Construye estructura corporativa, workforce, RH/beneficios, stakeholders, señales comerciales, hipótesis, Fit Map, Discovery Gap Map, Red Flags, provenance e Intelligence Preservation Ledger.

Las señales importantes siguen:

`EVIDENCIA → QUÉ DEMUESTRA → QUÉ NO DEMUESTRA → INFERENCIA → CONFIANZA`

### Fallback con Gemini

Si el host se queda sin Deep Research en Stage 8:

`Host → GEMINI_RESEARCH_HANDOFF → Gemini Deep Research → EXTERNAL_STAGE_8_DOSSIER → Host Reconciliation`

Gemini funciona como **Research Engine**. ChatGPT Work o Claude Cowork siguen siendo el **SOP Controller / Reconciliation Gate**.

Gemini no puede declarar por sí solo `ACCOUNT_INTELLIGENCE_COMPLETE`.

### Stages 9–12

**9 Outreach Strategy** → Reason to Reach Out, entry point, límites de autoridad, posicionamiento, CTA, canal, mensaje y backup/escalation logic. No ejecuta contacto.

**10 CRM Handoff / GHL** → prepara FINAL CRM PAYLOAD + FINAL VALIDATION GATE. GHL sigue siendo manual y los datos desconocidos permanecen vacíos.

**11 Prospect Intelligence Book & Sales Handoff** → genera el expediente comercial final con CRM Handoff, Executive Brief, Stakeholders, Account Intelligence, Fit, Discovery Gaps, estrategia, mensaje, follow-up, Discovery Playbook, objeciones, Next Best Actions, Unknown Data Register, fuentes y Sales Handoff Final.

Debe pasar:

`BENCHMARK_PARITY_TEST`

y

`VISUAL_SYSTEM_GATE`

No se aprueba por número de páginas o palabras: debe conservar inteligencia account-specific y mantener un diseño profesional uniforme.

**12 Archive & Tracking** → archiva el Handoff aprobado y actualiza el Master Tracker.

Estado final:

`PROSPECTING_WORKFLOW_COMPLETE`

## Multi-account / Multi-agent

Para múltiples cuentas existe un **Campaign Orchestrator** y un **Account Agent / Workstream** por cuenta.

El Orchestrator conserva Campaign State, priorización, Credit Ledger y decisiones humanas.

Cada Account Agent sólo recibe datos, contactos, artifacts y autorizaciones de su propia cuenta.

Si el host no soporta subagentes nativos, se emula con chats, tasks, branches o Account Handoffs separados.

## Hard Credit & Spend Controls

Por defecto:

`SPEND_ALLOWED = FALSE`

La IA nunca puede decidir gastar créditos por su cuenta.

Toda operación potencialmente pagada requiere autorización humana específica sobre proveedor, operación, cuenta, contacto(s), campos, costo/límite máximo, créditos máximos y scope de un solo uso.

La IA no puede ampliar contactos, añadir campos, reutilizar autorizaciones, lanzar retries pagados, cambiar de proveedor automáticamente ni comprar créditos.

Estados de protección:

`BLOCKED_BY_UNVERIFIED_COST`  
`BLOCKED_BY_CREDITS`

## Herramientas e integraciones

La lógica es host-neutral y usa **platform adapters**.

- **Apollo.io:** Account Discovery / Organization Lookup / People Search cuando el plan lo permite.
- **FullEnrich:** Identity Validation y Work Email Enrichment bajo hard spend gates.
- **Web / Browser Research:** discovery público, fuentes y Account Intelligence.
- **Deep Research:** exclusivamente Stage 8.
- **Gemini:** fallback externo cuando no hay Deep Research nativo.
- **Google Drive / Docs:** entrega y archivo de Handoffs.
- **Google Sheets:** Master Tracker y trazabilidad.
- **GHL / GoHighLevel:** captura manual; la Skill prepara el payload.
- **GitHub:** distribución, instalación y versionado.

## Requisitos para funcionamiento óptimo

### Plataforma

Una de las siguientes:

- **ChatGPT Work** con Skills / Plugins / Connectors.
- **Claude Cowork / Claude Code** con Skills y herramientas externas.

### Acceso recomendado

Para ejecutar el workflow completo:

- Apollo.io;
- FullEnrich;
- navegador / web research;
- Deep Research;
- Gemini para fallback;
- creación de documentos editables;
- Google Drive;
- Google Sheets.

No todos los conectores son obligatorios para iniciar. La Skill realiza **PRECHECK 0** para detectar qué capacidades están disponibles antes de comenzar.

### Datos mínimos de campaña

Normalmente se requieren:

- nombre de campaña;
- empresa oferente;
- solución;
- geografía;
- ICP;
- criterio de tamaño;
- roles objetivo;
- exclusiones;
- tamaño del universo;
- máximo Tier A;
- presupuesto de créditos.

## Sistema visual

Todos los Handoffs deben mantener la misma identidad profesional.

La especificación está en:

`references/09-visual-system.md`

Incluye formato Letter, Aptos/Aptos Display, paleta azul, jerarquía H1/H2/H3, portada uniforme, header/footer, tablas nativas, filas alternas y control de clipping/solapamientos.

## Principios

1. La IA investiga; el humano controla el gasto.
2. Evidence first.
3. Cargo no equivale a autoridad.
4. Ausencia pública no equivale a ausencia real.
5. Una cuenta no contamina otra.
6. Deep Research pertenece sólo a Account Intelligence.
7. Unknowns siguen siendo unknowns hasta validarse.
8. Un self-reported PASS no sustituye una auditoría real.
9. El Handoff debe ser útil sin abrir chats anteriores.
10. El workflow termina sólo después de archivo + tracking.

## Estructura

```text
b2b-prospecting-sales-os/
├── SKILL.md
├── plugin.json
├── .claude-plugin/
├── references/
├── templates/
├── schemas/
├── scripts/
└── evals/
```

## Estado

**v0.9.1 Release Candidate**

La promoción a **v1.0.0** debe realizarse después de validar instalación y ejecución end-to-end en ChatGPT Work y Claude Cowork.

## Autor

**Mitchell Correa / Cyberwolf AI**  
B2B Sales Operations · AI Automation · Commercial Intelligence
