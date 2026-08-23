import pytest
from app.domain.audit.audit_chain_engine import AuditChainEngine

def test_audit_hash_chain():
    prev = AuditChainEngine.GENESIS_HASH
    payload = {"event_id": "DEMO-001", "decision": "SAFE_TO_AUTOMATE"}
    
    hash1 = AuditChainEngine.compute_hash(prev, payload)
    assert len(hash1) == 64
    
    payload2 = {"event_id": "DEMO-002", "decision": "NEEDS_VERIFICATION"}
    hash2 = AuditChainEngine.compute_hash(hash1, payload2)
    assert len(hash2) == 64
    assert hash1 != hash2

def test_tamper_detection():
    class DummyRecord:
        def __init__(self, audit_event_id, previous_hash, current_hash, payload_json):
            self.audit_event_id = audit_event_id
            self.previous_hash = previous_hash
            self.current_hash = current_hash
            self.payload_json = payload_json

    prev = AuditChainEngine.GENESIS_HASH
    p1 = {"event_id": "DEMO-001"}
    h1 = AuditChainEngine.compute_hash(prev, p1)
    
    p2 = {"event_id": "DEMO-002"}
    h2 = AuditChainEngine.compute_hash(h1, p2)
    
    rec1 = DummyRecord("aud-1", prev, h1, p1)
    rec2 = DummyRecord("aud-2", h1, h2, p2)
    
    # Valid chain
    is_valid, msg = AuditChainEngine.verify_chain([rec1, rec2])
    assert is_valid is True
    assert msg == "VALID_HASH_CHAIN"
    
    # Tampered payload in record 1
    tampered_rec1 = DummyRecord("aud-1", prev, h1, {"event_id": "TAMPERED_DEMO-001"})
    is_valid_t, msg_t = AuditChainEngine.verify_chain([tampered_rec1, rec2])
    assert is_valid_t is False
    assert "TAMPERED" in msg_t
