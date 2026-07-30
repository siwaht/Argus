<div align="center">

# Argus

A general-purpose AI agent inspired by Hermes, built on LangChain, LangGraph and DeepAgents.

</div>

---

## Tools and capabilities

- Tools
- MCP
- Backend file system
- Long-term memory
- Short-term memory
- Multi-agent system
- Cron jobs for scheduling tasks
- RAG
- Permissions
- Human-in-the-loop
- Guardrails
- Skills

---

## Architecture

```mermaid
flowchart LR
    U[User Message]
    RM[Recall Memory]
    MA{Main Agent}
    PG{Permissions + Guardrails}
    HA[Human Approval]

    SKILLS[Skills]
    FBS[File Backend System]
    FBA[add]
    FBU[update]
    FBD[delete]

    R[Research Sub-Agent]
    S[Scheduler Sub-Agent]
    G[RAG Sub-Agent]
    MCP[MCP/Tools Sub-Agent]

    WEB[Web Search - Firecrawl MCP]
    SCR[Scrape + Extract]

    CRON[Cron Jobs]
    REM[Reminders]
    TD1[write_todos]

    VS[Vector Search - pgvector]

    MFB[File Backend System]
    MFBA[add]
    MFBU[update]
    MFBD[delete]

    SM[Save Memory]
    FR[Final Response]

    U --> RM
    RM --> MA

    MA -->|takes an action| PG
    PG -->|needs approval| HA

    PG -->|own tool| SKILLS
    SKILLS --> FBS
    FBS --> FBA
    FBS --> FBU
    FBS --> FBD

    PG -->|delegate| R
    PG -->|delegate| S
    PG -->|delegate| G
    PG -->|delegate| MCP

    R --> WEB
    R --> SCR

    S --> CRON
    S --> REM
    S --> TD1

    G --> VS

    MCP --> MFB
    MFB --> MFBA
    MFB --> MFBU
    MFB --> MFBD

    MA -->|done| SM
    SM --> FR
```
