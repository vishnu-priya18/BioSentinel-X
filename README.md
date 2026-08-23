# BioSentinel-X: Software-Defined Biomedical Waste Decision Operating System

> **Tagline**: *"Don't just classify the waste. Know what you don't know."*
> **SIH Problem Statement**: SIH26115 — Design and Develop a Smart Mobile Medical Waste Collection and Segregation System (Software Edition)
> **Core Innovation Thesis**: BioSentinel-X separates machine learning prediction from permission to act. It combines evidence fusion, content observability assessment, uncertainty estimation, conflict detection, operational risk analysis, deterministic safety policies, human verification, risk-aware collection, Waste Passports, and tamper-evident audit trails.

---

## 1. Project Directory Tree

```
medicalwaste/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI Routes & App Entrypoint
│   │   ├── config.py                  # Environment Specs & Threshold Settings
│   │   ├── database.py                # SQLAlchemy 2.0 DB Connection
│   │   ├── seed_data.py               # Deterministic DEMO-001 to DEMO-008 Seeder
│   │   ├── domain/                    # Clean Domain Architecture
│   │   │   ├── evidence/              # Quality, Observability & Fusion Engines
│   │   │   ├── intelligence/          # WasteClassifier Protocol, Uncertainty & Anomaly
│   │   │   ├── decision/              # Policy Engine, DecisionTrace & Counterfactual
│   │   │   ├── compliance/            # Dynamic QR & Waste Passport Engine
│   │   │   ├── collection/            # Risk Routing Priority Score Math
│   │   │   └── audit/                 # SHA-256 Tamper-Evident Event Hash Chainer
│   │   ├── models/                    # SQLAlchemy Declarative Models (21 Tables)
│   │   ├── schemas/                   # Pydantic Request/Response Schemas
│   │   └── api/                       # API Route Controllers
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── types/                     # TypeScript Definitions
│       ├── context/                   # Auth & Demo State
│       ├── components/                # WhyNotPanel, AiVsBioSentinel, ExplainScoreModal, etc.
│       ├── pages/                     # 23 Complete Application Pages
│       └── services/                  # API Client with Offline Fallback
├── tests/                             # Pytest Unit & Policy Test Suite
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
└── README.md
```

---

## 2. Quick Setup & Run Instructions

### Local Development (Python + Node.js)

1. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
   ```
   *Healthcheck Verification*: Visit `http://localhost:8080/health`

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   *UI Access*: Visit `http://localhost:3000`

### Run with Docker Compose

```bash
docker compose up --build
```
* Access Frontend: `http://localhost:3000`
* Access Backend API Docs (Swagger): `http://localhost:8000/docs`

---

## 3. Environment Variables

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | `sqlite:///./biosentinel_x.db` | SQLAlchemy DB Connection string (PostgreSQL ready) |
| `SECRET_KEY` | `biosentinel-x-sih-2026-secret-key-32bytes-min` | JWT signature key |
| `HIGH_CONFLICT_THRESHOLD` | `0.60` | Conflict score threshold for escalation |
| `HIGH_RISK_THRESHOLD` | `0.65` | Operational risk threshold |
| `HIGH_UNCERTAINTY_THRESHOLD` | `0.60` | Softmax uncertainty entropy threshold |
| `VERIFICATION_THRESHOLD` | `0.35` | Verification queue threshold |

---

## 4. Run Unit & Policy Tests

```bash
python -c "import sys, os; sys.path.insert(0, os.path.abspath('backend')); import pytest; exit(pytest.main(['tests/']))"
```
*Includes tests for all 5 decision states (`SAFE_TO_AUTOMATE`, `NEEDS_VERIFICATION`, `HIGH_RISK_ESCALATION`, `UNKNOWN`, `SYSTEM_ERROR`), opaque containers, barcode conflict detection, and SHA-256 tamper-evident hash chaining.*

---

## 5. SIH 3-Minute Grand Finale Presentation Script

* **0:00–0:20 (The Problem & Thesis)**:
  * *"Biomedical waste segregation fails not only because AI makes mistakes, but because traditional systems don't know when evidence is insufficient."*
* **0:20–0:50 (Normal Safe Case — DEMO-001)**:
  * Scan DEMO-001 (Clear IV set photo, valid barcode, normal weight).
  * Show Result: **RED — Confidence 94%**, Evidence Quality: Strong $\rightarrow$ `SAFE_TO_AUTOMATE`.
* **0:50–1:20 (THE KILLER MOMENT: Opaque Bag — DEMO-003)**:
  * Scan DEMO-003 (Plastic bag photo). AI Prediction: RED (91% Confidence).
  * Point to BioSentinel-X check: Container: **OPAQUE**, Observability: **NOT OBSERVABLE**.
  * **Pause for Judges**: Show how AI Prediction = RED (91%), BUT Decision = `UNKNOWN` / `NEEDS_VERIFICATION`. *"91% is the model's confidence. It is not permission to act."*
* **1:20–1:50 (Evidence Conflict — DEMO-004)**:
  * Scan DEMO-004: Barcode $\rightarrow$ Yellow, Image $\rightarrow$ Red, Weight $\rightarrow$ Abnormal.
  * Show Result: **CONFLICT DETECTED** (Score 0.71) $\rightarrow$ `HIGH_RISK_ESCALATION`.
* **1:50–2:20 (Operational Intelligence & ICU Surge)**:
  * Trigger ICU Waste Surge $\rightarrow$ Anomaly Z-score = +4.8 $\rightarrow$ Priority Score $P_{\text{task}} = 94.2 \rightarrow$ Collection Route Updated. Click **"Explain Score"** to show exact mathematical formula breakdown!
* **2:20–2:50 (Waste Passport & Tamper-Evident Audit)**:
  * Open Waste Passport for DEMO-007. Show dynamic QR code & SHA-256 Tamper-Evident Hash Chain.
* **2:50–3:00 (Closing Line)**:
  * *"We don't build an AI that always gives an answer. We build a system that knows when an answer isn't safe enough to act on."*

---

## 6. Architecture & Non-Negotiable Safety Principles

```
┌────────────────────────────────────────────────────────┐
│ 1. WHAT DOES THE MODEL PREDICT?                        │
│    AI Classification (Category, Probability, Model Ver)│
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 2. WHAT EVIDENCE DO WE HAVE?                           │
│    Evidence Fusion (Image, Barcode, Weight, Dept, Obs)│
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 3. HOW TRUSTWORTHY IS IT?                              │
│    Uncertainty + Conflict Detector + Operational Risk  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 4. ARE WE ALLOWED TO ACT?                              │
│    Deterministic Policy Engine (SAFE, VERIFY, ESCALATE)│
└───────────────────────────┬────────────────────────────┘
```

1. **Explicit Unknown State**: Opaque containers output `"CONTENT NOT OBSERVABLE"` and transition to `UNKNOWN` or `NEEDS_VERIFICATION`.
2. **Deterministic Backend Policy**: Final operational decisions are evaluated strictly by backend code, never by an LLM or frontend script.
3. **Immutable DecisionTrace**: Every waste analysis outputs a single, immutable JSON dataclass object.
4. **Append-Only History**: Human verifiers create new verification events rather than overwriting historical records.
5. **SHA-256 Tamper-Evident Audit Chain**: Derives SHA-256 previous/current hash linkage without claiming physical chain-of-custody proof or blockchain magic.

---

## 7. Known Limitations & Future Production Integration Points

* **Classifier Adapter**: The prototype uses `DemoWasteClassifier` for deterministic SIH demonstration. The adapter interface (`WasteClassifier` protocol) supports zero-code swap to ONNX or TensorRT models in production.
* **Regulatory Connectors**: Mock connectors simulate CPCB/SPCB portal endpoints for demonstration purposes.
* **Synthetic Data**: All hospital telemetry and waste records are synthetic demo data.
