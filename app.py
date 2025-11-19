import streamlit as st

from recommend import load_clothes, generate_outfits


def main():
    st.set_page_config(
        page_title="Wardrobe Outfit Recommender",
        page_icon="👗",
        layout="centered",
    )

    st.title("👗 Wardrobe Outfit Recommender")
    st.write(
        "Upload or use your saved wardrobe data and get outfit suggestions based on "
        "occasion, weather, and simple color harmony."
    )

    # Load default data
    clothes_df = load_clothes()

    st.sidebar.header("Settings")
    occasion = st.sidebar.selectbox(
        "Occasion",
        ["Casual", "Smart casual", "Work", "Formal"],
        index=0,
    )
    weather = st.sidebar.selectbox(
        "Weather",
        ["Mild", "Cold", "Hot"],
        index=0,
    )
    n_outfits = st.sidebar.slider(
        "Number of outfit suggestions",
        min_value=1,
        max_value=5,
        value=3,
    )

    st.subheader("Your wardrobe (from CSV)")
    st.dataframe(clothes_df)

    if st.button("✨ Generate outfit ideas"):
        outfits = generate_outfits(clothes_df, occasion, weather, n_outfits)

        if not outfits:
            st.warning("No outfits could be generated with the current filters.")
            return

        st.subheader("Suggested Outfits")

        for i, outfit in enumerate(outfits, start=1):
            st.markdown(f"### Outfit {i}")
            cols = st.columns(len(outfit["items"]))
            for col, item in zip(cols, outfit["items"]):
                with col:
                    st.markdown(
                        f"**{item['name']}**  \n"
                        f"- Category: `{item['category']}`  \n"
                        f"- Color: `{item['color']}`  \n"
                        f"- Style: `{item['style']}`  \n"
                        f"- Formality: `{item['formality']}`"
                    )
                    notes = str(item.get("notes", "")).strip()
                    if notes and notes.lower() != "nan":
                        st.caption(notes)

            st.markdown("---")

    st.info(
        "Tip: later you can extend this with images, user preferences, or a way to "
        "edit the wardrobe directly in the app."
    )


if __name__ == "__main__":
    main()
