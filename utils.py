import math

# Simple mapping from color name to RGB
COLOR_MAP = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "blue": (70, 130, 180),
    "navy": (0, 0, 128),
    "yellow": (255, 255, 0),
    "beige": (245, 245, 220),
    "grey": (128, 128, 128),
    "gray": (128, 128, 128),
    "pink": (255, 182, 193),
    # add more as needed
}

def color_to_rgb(color_name: str):
    """Convert a simple color name to RGB. Falls back to grey."""
    if not isinstance(color_name, str):
        return (128, 128, 128)
    key = color_name.strip().lower()
    return COLOR_MAP.get(key, (128, 128, 128))

def color_distance(c1: str, c2: str) -> float:
    """Euclidean distance between two color names."""
    r1, g1, b1 = color_to_rgb(c1)
    r2, g2, b2 = color_to_rgb(c2)
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

def occasion_to_formality_range(occasion: str):
    """
    Map an occasion to an allowed range of formality.
    We'll treat formality as: low < medium < high
    """
    if occasion == "Casual":
        return ["low", "medium"]
    elif occasion == "Smart casual":
        return ["medium"]
    elif occasion == "Work":
        return ["medium", "high"]
    elif occasion == "Formal":
        return ["high"]
    else:
        # fallback: allow everything
        return ["low", "medium", "high"]

def normalize_formality(value: str):
    """Ensure formality values look consistent."""
    if not isinstance(value, str):
        return "medium"
    return value.strip().lower()
