from user_profile import UserProfile

def filter_offers(offers: list, user_profile: UserProfile) -> list:
    """
    Función abstracta que simula el filtrado de ofertas utilizando un gran modelo de lenguaje.
    Se toma un perfil en texto libre para su interpretación.
    """
    filtered = []
    # ... lógica abstracta que utilizaría un LLM para filtrar ofertas ...
    for offer in offers:
        # Simulación de decisión del LLM basado en offer y user_profile['profile']
        # Ejemplo abstracto: se incluye la oferta si el perfil no está vacío.
        if user_profile.get("profile"):
            filtered.append(offer)
    return filtered
