import os
import random
import pandas as pd

from utils import color_distance, occasion_to_formality_range, normalize_formality


def load_clothes(csv_path: str = None) -> pd.DataFrame:
    """Load clothing items from CSV."""
    if csv_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, "data", "clothes.csv")

    df = pd.read_csv(csv_path)
    # Normalize categories & formalities a bit
    df["category"] = df["category"].str.strip().str.lower()
    df["formality"] = df["formality"].apply(normalize_formality)
    df["color"] = df["color"].str.strip().str.lower()
    return df


def filter_by_occasion_and_weather(df: pd.DataFrame, occasion: str, weather: str) -> pd.DataFrame:
    """Apply simple filters based on occasion & weather."""
    allowed_formality = occasion_to_formality_range(occasion)
    filtered = df[df["formality"].isin(allowed_formality)]

    # Weather logic is intentionally simple & explainable
    if weather == "Cold":
        # prefer tops, bottoms, outerwear, closed shoes
        filtered = filtered[
            filtered["category"].isin(["top", "bottom", "outerwear", "shoes"])
        ]
    elif weather == "Hot":
        # prefer tops, bottoms, dresses, avoid outerwear
        filtered = filtered[
            filtered["category"].isin(["top", "bottom", "dress", "shoes"])
        ]
    else:
        # Mild - keep everything
        pass

    return filtered


def generate_top_bottom_combos(df: pd.DataFrame):
    tops = df[df["category"] == "top"]
    bottoms = df[df["category"] == "bottom"]

    combos = []
    for _, top in tops.iterrows():
        for _, bottom in bottoms.iterrows():
            dist = color_distance(top["color"], bottom["color"])
            combos.append(
                {
                    "items": [top, bottom],
                    "score": -dist,  # smaller distance = better → negative
                }
            )
    return combos


def generate_dress_outfits(df: pd.DataFrame):
    dresses = df[df["category"] == "dress"]
    outfits = []
    for _, dress in dresses.iterrows():
        outfits.append(
            {
                "items": [dress],
                "score": 0,  # neutral score, you can tune this later
            }
        )
    return outfits


def maybe_add_outerwear(df: pd.DataFrame, outfit_items, weather: str):
    """If it's cold, add a random outerwear piece that matches vaguely."""
    if weather != "Cold":
        return outfit_items

    outerwear = df[df["category"] == "outerwear"]
    if outerwear.empty:
        return outfit_items

    # Simple: choose one with closest color to first item
    base_color = outfit_items[0]["color"]
    outerwear = outerwear.copy()
    outerwear["dist"] = outerwear["color"].apply(lambda c: color_distance(c, base_color))
    best_outer = outerwear.sort_values("dist").iloc[0]
    return outfit_items + [best_outer]


def generate_outfits(
    df: pd.DataFrame,
    occasion: str,
    weather: str,
    n_outfits: int = 3,
):
    """
    Main function: returns a list of outfits.
    Each outfit is a dict with:
      - items: list of Series (clothing rows)
      - score: numeric preference score
    """
    filtered = filter_by_occasion_and_weather(df, occasion, weather)

    if filtered.empty:
        return []

    combos = generate_top_bottom_combos(filtered)
    dresses = generate_dress_outfits(filtered)

    all_outfits = combos + dresses

    # Sort by score descending (higher = better)
    all_outfits.sort(key=lambda x: x["score"], reverse=True)

    # Take top n, then add outerwear if needed
    selected = all_outfits[: max(n_outfits, 1)]
    final_outfits = []
    for outfit in selected:
        items_with_outer = maybe_add_outerwear(filtered, outfit["items"], weather)
        final_outfits.append(
            {
                "items": items_with_outer,
                "score": outfit["score"],
            }
        )

    return final_outfits
