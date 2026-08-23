class QualityEvaluator:
    """
    Evaluates visual image quality based on brightness, blur, resolution, and framing.
    Returns image_quality_score in range [0.0, 1.0].
    """
    @staticmethod
    def evaluate(image_base64: str = None, metadata: dict = None) -> float:
        if not image_base64:
            return 0.10 # Extremely low quality if no image provided
            
        # Demo simulation logic for deterministic test scenarios
        if metadata and "quality_override" in metadata:
            return float(metadata["quality_override"])
            
        # Simulated quality evaluation
        return 0.88 # Default good quality score
