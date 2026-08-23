class ObservabilityEngine:
    """
    Evaluates content observability state: OBSERVABLE, PARTIALLY_OBSERVABLE, NOT_OBSERVABLE.
    Enforces non-negotiable safety rule: If opaque, internal contents are NOT_OBSERVABLE.
    """
    @staticmethod
    def evaluate(opacity_state: str, container_type: str = "PLASTIC_BAG") -> str:
        state = opacity_state.upper()
        if state in ["NOT_OBSERVABLE", "OPAQUE"]:
            return "NOT_OBSERVABLE"
        elif state in ["PARTIALLY_OBSERVABLE", "TRANSLUCENT"]:
            return "PARTIALLY_OBSERVABLE"
        return "OBSERVABLE"
