import hashlib
import json
from typing import Dict, Any, Tuple

class AuditChainEngine:
    """
    SHA-256 Tamper-Evident Audit Chain Engine.
    Computes current_hash = SHA256(previous_hash + canonical_json_payload).
    Provides verification algorithm for tamper detection.
    """
    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

    @staticmethod
    def compute_hash(previous_hash: str, payload: Dict[str, Any]) -> str:
        canonical_str = json.dumps(payload, sort_keys=True)
        raw_bytes = f"{previous_hash}:{canonical_str}".encode('utf-8')
        return hashlib.sha256(raw_bytes).hexdigest()

    @staticmethod
    def verify_chain(chain_records: list) -> Tuple[bool, str]:
        """
        Verifies list of (previous_hash, current_hash, payload) records.
        Returns (is_valid, status_message).
        """
        if not chain_records:
            return True, "VALID_EMPTY_CHAIN"

        for i, rec in enumerate(chain_records):
            prev_h = rec.previous_hash
            curr_h = rec.current_hash
            payload = rec.payload_json
            
            expected_h = AuditChainEngine.compute_hash(prev_h, payload)
            if expected_h != curr_h:
                return False, f"TAMPERED_AT_INDEX_{i}_ENTITY_{rec.audit_event_id}"
                
        return True, "VALID_HASH_CHAIN"
