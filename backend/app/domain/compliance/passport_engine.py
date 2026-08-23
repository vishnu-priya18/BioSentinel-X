import uuid

class PassportEngine:
    """
    Generates unique Waste Passports.
    Stores passport_code in database as source of truth.
    Generates QR code dynamically on request.
    """
    @staticmethod
    def generate_code(event_code: str) -> str:
        suffix = str(uuid.uuid4())[:8].upper()
        return f"WP-{event_code}-{suffix}"

    @staticmethod
    def generate_qr_svg(passport_code: str) -> str:
        """
        Generates dynamic SVG QR Code string for passport verification URL.
        """
        # Clean inline SVG representation of QR code placeholder
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
  <rect width="200" height="200" fill="#0F172A"/>
  <rect x="20" y="20" width="50" height="50" fill="#06B6D4"/>
  <rect x="30" y="30" width="30" height="30" fill="#0F172A"/>
  <rect x="40" y="40" width="10" height="10" fill="#06B6D4"/>
  
  <rect x="130" y="20" width="50" height="50" fill="#06B6D4"/>
  <rect x="140" y="30" width="30" height="30" fill="#0F172A"/>
  <rect x="150" y="40" width="10" height="10" fill="#06B6D4"/>

  <rect x="20" y="130" width="50" height="50" fill="#06B6D4"/>
  <rect x="30" y="140" width="30" height="30" fill="#0F172A"/>
  <rect x="40" y="150" width="10" height="10" fill="#06B6D4"/>
  
  <path d="M 80,30 H 110 V 50 H 80 Z" fill="#38BDF8"/>
  <path d="M 90,80 H 150 V 110 H 90 Z" fill="#38BDF8"/>
  <path d="M 30,80 H 60 V 110 H 30 Z" fill="#38BDF8"/>
  <path d="M 80,130 H 160 V 170 H 80 Z" fill="#38BDF8"/>
  <text x="100" y="190" font-family="monospace" font-size="8" fill="#94A3B8" text-anchor="middle">{passport_code}</text>
</svg>'''
        return svg_content
