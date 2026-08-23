import datetime
from sqlalchemy.orm import Session
from app.models.domain_models import (
    Role, Hospital, Department, User, WasteCategory, WasteEvent,
    EvidenceItem, AiPrediction, UncertaintyAssessment, Decision,
    VerificationEvent, WastePassport, CollectionTask, DepartmentProfile,
    Anomaly, Alert, AuditEvent, AuditHashChain, SystemSetting
)
from app.domain.audit.audit_chain_engine import AuditChainEngine
from app.domain.compliance.passport_engine import PassportEngine

def seed_database(db: Session):
    # Check if already seeded
    if db.query(Role).first():
        return

    print("Seeding BioSentinel-X deterministic demo data (DEMO-001 to DEMO-008)...")

    # 1. Roles
    roles = {
        "ADMIN": Role(id="role-admin", role_name="ADMIN", permissions_json=["ALL"]),
        "SUPERVISOR": Role(id="role-supervisor", role_name="SUPERVISOR", permissions_json=["MONITOR", "VERIFY", "ASSIGN"]),
        "SANITATION_WORKER": Role(id="role-worker", role_name="SANITATION_WORKER", permissions_json=["SCAN", "COLLECT"]),
        "VERIFIER": Role(id="role-verifier", role_name="VERIFIER", permissions_json=["VERIFY", "INSPECT"]),
        "VIEWER": Role(id="role-viewer", role_name="VIEWER", permissions_json=["VIEW"])
    }
    for r in roles.values():
        db.add(r)

    # 2. Hospital
    hosp = Hospital(id="hosp-01", name="Sentinel General Hospital", code="SGH-DELHI", address="New Delhi, India")
    db.add(hosp)

    # 3. Departments
    depts = {
        "ICU": Department(id="dept-icu", hospital_id="hosp-01", name="ICU Ward", code="ICU-01", baseline_daily_waste_kg=12.5, criticality_score=95.0),
        "EMG": Department(id="dept-emg", hospital_id="hosp-01", name="Emergency Ward", code="EMG-01", baseline_daily_waste_kg=15.0, criticality_score=90.0),
        "LAB": Department(id="dept-lab", hospital_id="hosp-01", name="Pathology Laboratory", code="LAB-01", baseline_daily_waste_kg=2.1, criticality_score=85.0),
        "WDA": Department(id="dept-wda", hospital_id="hosp-01", name="Ward A", code="WDA-01", baseline_daily_waste_kg=8.0, criticality_score=60.0),
        "WDB": Department(id="dept-wdb", hospital_id="hosp-01", name="Ward B", code="WDB-01", baseline_daily_waste_kg=7.5, criticality_score=60.0),
        "OT": Department(id="dept-ot", hospital_id="hosp-01", name="Operation Theatre", code="OT-01", baseline_daily_waste_kg=20.0, criticality_score=98.0)
    }
    for d in depts.values():
        db.add(d)

    # Department Profiles
    for d in depts.values():
        dp = DepartmentProfile(id=f"dp-{d.id}", dept_id=d.id, avg_daily_waste_kg=d.baseline_daily_waste_kg, integrity_score=95.0)
        db.add(dp)

    # 4. Waste Categories
    cats = {
        "Yellow": WasteCategory(id="cat-yel", code="Yellow", display_name="Yellow (Incineration)", color_hex="#F59E0B", description="Anatomical waste, soiled linen, chemical waste", active=True),
        "Red": WasteCategory(id="cat-red", code="Red", display_name="Red (Autoclave/Recycle)", color_hex="#EF4444", description="Contaminated plastic tubing, IV bottles, catheters", active=True),
        "White": WasteCategory(id="cat-wht", code="White", display_name="White Sharps", color_hex="#F8FAFC", description="Needles, scalpels, blades in puncture-proof container", active=True),
        "Blue": WasteCategory(id="cat-blu", code="Blue", display_name="Blue Glassware", color_hex="#3B82F6", description="Glass bottles, medicine vials, metallic implants", active=True),
        "Unknown": WasteCategory(id="cat-unk", code="Unknown", display_name="Unknown / Unsafe", color_hex="#64748B", description="Uncertain or unobservable waste content", active=True)
    }
    for c in cats.values():
        db.add(c)

    # 5. Users
    users = [
        User(id="usr-admin", email="admin@sentinel.org", password_hash="hash_admin", full_name="Dr. Rajesh Sharma", role_id="role-admin", dept_id="dept-icu"),
        User(id="usr-supervisor", email="supervisor@sentinel.org", password_hash="hash_sup", full_name="Anita Roy", role_id="role-supervisor", dept_id="dept-emg"),
        User(id="usr-worker", email="worker@sentinel.org", password_hash="hash_wrk", full_name="Staff Worker #412", role_id="role-worker", dept_id="dept-icu"),
        User(id="usr-verifier", email="verifier@sentinel.org", password_hash="hash_ver", full_name="Safety Verifier Vikram", role_id="role-verifier", dept_id="dept-lab"),
    ]
    for u in users:
        db.add(u)

    db.commit()

    # Helper function to create DEMO event records
    prev_hash = AuditChainEngine.GENESIS_HASH

    def create_demo_event(
        event_code, dept_id, declared_cat_code, weight_kg, opacity_state,
        pred_cat_code, confidence, quality_score, observability, conflict_score,
        conflict_codes, entropy, uncertainty_score, decision_state, reason_codes,
        required_evidence, z_score=0.0, is_verified=False
    ):
        nonlocal prev_hash

        ev = WasteEvent(
            id=f"evt-{event_code.lower()}",
            event_code=event_code,
            dept_id=dept_id,
            user_id="usr-worker",
            declared_category_id=cats[declared_cat_code].id,
            weight_kg=weight_kg,
            container_type="PLASTIC_BAG",
            opacity_state=opacity_state,
            user_notes=f"Simulated event scenario {event_code}"
        )
        db.add(ev)

        # AI Prediction
        pred = AiPrediction(
            id=f"pred-{event_code.lower()}",
            event_id=ev.id,
            model_name="DEMO_SIMULATION_MODEL_V1.0",
            predicted_category_id=cats[pred_cat_code].id,
            class_probabilities_json={"Yellow": 0.05, "Red": confidence, "White": 0.02, "Blue": 0.03},
            confidence=confidence,
            is_simulated=True
        )
        db.add(pred)

        # Uncertainty Assessment
        unc = UncertaintyAssessment(
            id=f"unc-{event_code.lower()}",
            event_id=ev.id,
            entropy=entropy,
            quality_score=quality_score,
            uncertainty_score=uncertainty_score,
            observability_state=observability,
            level_enum="HIGH_UNCERTAINTY" if uncertainty_score >= 0.6 else ("MEDIUM_UNCERTAINTY" if uncertainty_score >= 0.35 else "LOW_UNCERTAINTY")
        )
        db.add(unc)

        # Decision Trace Payload
        trace_payload = {
            "event_id": event_code,
            "prediction": {"category": pred_cat_code, "confidence": confidence, "probabilities": {"Red": confidence}, "model_version": "DEMO_V1"},
            "evidence": {"image_quality": quality_score, "observability": observability, "barcode_support": 1.0 if not conflict_codes else 0.12, "weight_support": 1.0 if z_score < 2.5 else 0.31, "historical_support": 0.85, "missing_evidence": []},
            "conflicts": {"score": conflict_score, "detected": len(conflict_codes) > 0, "conflict_codes": conflict_codes},
            "uncertainty": {"entropy": entropy, "uncertainty_score": uncertainty_score, "calibration_status": "CALIBRATED_PROTOTYPE"},
            "risk": {"score": round(max(conflict_score, uncertainty_score), 2), "hazard_risk": 0.3, "anomaly_risk": 0.8 if z_score >= 2.5 else 0.1, "delay_risk": 0.1, "department_criticality": 0.9},
            "decision": {"state": decision_state, "reason_codes": reason_codes, "action_recommended": "Auto Approve" if decision_state == "SAFE_TO_AUTOMATE" else "Send for Human Verification"},
            "counterfactual": {"required": required_evidence},
            "versions": {"model_version": "DEMO_V1", "fusion_version": "V1", "policy_version": "V1", "risk_version": "V1", "trace_version": "V1"},
            "timestamps": {"created_at": datetime.datetime.utcnow().isoformat()}
        }

        dec = Decision(
            id=f"dec-{event_code.lower()}",
            event_id=ev.id,
            decision_state=decision_state,
            final_category_id=cats[pred_cat_code].id,
            risk_level="HIGH" if decision_state in ["HIGH_RISK_ESCALATION", "UNKNOWN"] else "LOW",
            reasons_json=reason_codes,
            missing_evidence_json=[],
            conflicting_evidence_json=conflict_codes,
            action_recommended="Proceed" if decision_state == "SAFE_TO_AUTOMATE" else "Inspect",
            trace_json=trace_payload
        )
        db.add(dec)

        # Audit Event & SHA-256 Hash Chain
        aud = AuditEvent(
            id=f"aud-{event_code.lower()}",
            entity_name="WasteEvent",
            entity_id=ev.id,
            action="CREATE_AND_ANALYZE",
            performed_by="usr-worker",
            payload_json=trace_payload
        )
        db.add(aud)

        cur_h = AuditChainEngine.compute_hash(prev_hash, trace_payload)
        chain = AuditHashChain(
            id=f"chain-{event_code.lower()}",
            audit_event_id=aud.id,
            previous_hash=prev_hash,
            current_hash=cur_h
        )
        db.add(chain)
        prev_hash = cur_h

        # If verified, issue Waste Passport & Collection Task
        if decision_state == "SAFE_TO_AUTOMATE" or is_verified:
            p_code = PassportEngine.generate_code(event_code)
            passp = WastePassport(
                id=f"pass-{event_code.lower()}",
                passport_code=p_code,
                event_id=ev.id,
                declared_category_id=cats[declared_cat_code].id,
                verified_category_id=cats[pred_cat_code].id,
                weight_kg=weight_kg,
                risk_level="LOW",
                status="ISSUED",
                evidence_hash=cur_h
            )
            db.add(passp)

            ct = CollectionTask(
                id=f"task-{event_code.lower()}",
                passport_id=passp.id,
                dept_id=dept_id,
                assigned_worker_id="usr-worker",
                priority_score=78.5,
                status="PENDING"
            )
            db.add(ct)

    # Seed DEMO-001 to DEMO-008 deterministically
    create_demo_event("DEMO-001", "dept-icu", "Red", 0.22, "OBSERVABLE", "Red", 0.94, 0.88, "OBSERVABLE", 0.0, [], 0.18, 0.12, "SAFE_TO_AUTOMATE", ["Visual quality clear", "High confidence"], ["ALL_SAFETY_BOUNDS_SATISFIED"])
    create_demo_event("DEMO-002", "dept-emg", "Yellow", 4.5, "OBSERVABLE", "Yellow", 0.62, 0.25, "OBSERVABLE", 0.1, [], 0.52, 0.48, "NEEDS_VERIFICATION", ["Visual quality too low"], ["HIGH_QUALITY_IMAGE_CAPTURE"])
    create_demo_event("DEMO-003", "dept-icu", "Red", 2.1, "NOT_OBSERVABLE", "Red", 0.91, 0.85, "NOT_OBSERVABLE", 0.0, [], 0.22, 0.55, "UNKNOWN", ["Container contents not observable"], ["OBSERVABLE_CONTENT_OR_TRANSPARENT_CONTAINER"])
    create_demo_event("DEMO-004", "dept-lab", "Red", 3.2, "OBSERVABLE", "Red", 0.88, 0.82, "OBSERVABLE", 0.71, ["BARCODE_VISUAL_CONFLICT", "ABNORMAL_WEIGHT"], 0.58, 0.64, "HIGH_RISK_ESCALATION", ["Barcode category conflict", "Abnormal weight"], ["VALID_CATEGORY_BARCODE_MATCH", "NORMAL_DEPARTMENT_WEIGHT_BASELINE"])
    create_demo_event("DEMO-005", "dept-lab", "Red", 18.5, "OBSERVABLE", "Red", 0.85, 0.80, "OBSERVABLE", 0.65, ["ABNORMAL_WEIGHT"], 0.35, 0.68, "HIGH_RISK_ESCALATION", ["Weight 18.5kg is 8.8x baseline (Z=+4.8)"], ["NORMAL_DEPARTMENT_WEIGHT_BASELINE"], z_score=4.8)
    create_demo_event("DEMO-006", "dept-icu", "Yellow", 14.2, "OBSERVABLE", "Yellow", 0.92, 0.88, "OBSERVABLE", 0.0, [], 0.15, 0.14, "SAFE_TO_AUTOMATE", ["ICU Waste volume surge"], ["ALL_SAFETY_BOUNDS_SATISFIED"])
    create_demo_event("DEMO-007", "dept-emg", "Yellow", 4.5, "OBSERVABLE", "Yellow", 0.88, 0.85, "OBSERVABLE", 0.0, [], 0.20, 0.18, "SAFE_TO_AUTOMATE", ["Human verifier approved DEMO-002"], ["ALL_SAFETY_BOUNDS_SATISFIED"], is_verified=True)
    create_demo_event("DEMO-008", "dept-ot", "Blue", 5.0, "OBSERVABLE", "Blue", 0.96, 0.90, "OBSERVABLE", 0.0, [], 0.10, 0.10, "SAFE_TO_AUTOMATE", ["Audit Hash Chain verified"], ["ALL_SAFETY_BOUNDS_SATISFIED"])

    # Seed Anomaly record for DEMO-005
    anom = Anomaly(
        id="anom-demo-005",
        dept_id="dept-lab",
        event_id="evt-demo-005",
        anomaly_type="WEIGHT_SURGE_ANOMALY",
        observed_value=18.5,
        baseline_value=2.1,
        z_score=4.8,
        severity="CRITICAL",
        recommended_action="Supervisor review recommended for unexpected waste weight surge (8.8x baseline)."
    )
    db.add(anom)

    # Seed Alert
    alr = Alert(
        id="alr-01",
        hospital_id="hosp-01",
        dept_id="dept-lab",
        alert_type="CRITICAL_WEIGHT_SURGE",
        title="Pathology Lab Weight Anomaly (Z=+4.8)",
        message="Laboratory waste bag DEMO-005 registered 18.5kg vs 2.1kg baseline (8.8x multiplier).",
        severity="CRITICAL"
    )
    db.add(alr)

    db.commit()
    print("BioSentinel-X database successfully seeded!")
