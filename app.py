import streamlit as st
from test_generator import generuj_test
import pytesseract
from PIL import Image
import json
from openai import OpenAI
import base64

client = OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="Asystent AI dla nauczyciela matematyki")

st.title("🧠 Asystent AI dla nauczyciela matematyki")

# Zakładki
zakladki = st.tabs(["📄 Generowanie testu", "📤 Sprawdzanie testu ucznia"])

# === GENEROWANIE TESTU ===
with zakladki[0]:
    st.subheader("📄 Wygeneruj test")

    with st.form("formularz_testu"):
        temat = st.text_input("Temat sprawdzianu (np. Ułamki zwykłe):")
        klasa = st.selectbox("Klasa:", ["4", "5", "6", "7", "8"])
        liczba_zadan = st.slider("Liczba zadań:", min_value=3, max_value=10, value=5)
        trudnosc = st.selectbox("Poziom trudności:", ["łatwy", "średni", "trudny"])
        typ = st.selectbox("Typ zadań:", ["otwarte", "zamknięte", "mieszane"])
        submit = st.form_submit_button("Generuj test")

    if submit:
        if temat.strip() == "":
            st.warning("Wpisz temat sprawdzianu.")
        else:
            with st.spinner("Generuję test..."):
                wynik = generuj_test(temat, klasa, liczba_zadan, trudnosc, typ)
                if wynik:
                    st.success("✅ Test wygenerowany!")
                    st.subheader("📄 Treść testu:")
                    st.markdown(wynik)
                else:
                    st.error("Coś poszło nie tak. Spróbuj ponownie.")
                


# === 📤 SPRAWDZANIE TESTU ===



with zakladki[1]:
    st.subheader("📤 Sprawdź test ucznia (na podstawie zdjęcia)")

    uploaded_image = st.file_uploader(
        "Prześlij zdjęcie lub skan testu ucznia (JPG/PNG)", type=["png", "jpg", "jpeg"]
    )

    if uploaded_image:
        st.image(uploaded_image, caption="Załadowany test", use_column_width=True)

        try:
            # Wczytaj i zakoduj obraz do base64
            image_bytes = uploaded_image.read()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")

            client = OpenAI(api_key=st.secrets["openai_api_key"])

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "Jesteś pomocnym asystentem nauczyciela matematyki. Twoim zadaniem jest odczytanie odpowiedzi z odręcznego testu ucznia, a następnie porównanie ich z poprawnymi odpowiedziami."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""
        Na podstawie poniższego zdjęcia testu ucznia:

        1. Rozpoznaj odpowiedzi w formacie: {{1: "A", 2: "B", ...}}.
        2. Porównaj je z kluczem odpowiedzi.
        3. Oblicz wynik i dodaj krótkie podsumowanie (ile poprawnych, ile błędnych).
        4. Nie pisz nic poza analizą – tylko wynik i detale.

        Poprawne odpowiedzi to:
        {{1: "C", 2: "A", 3: "D", 4: "B", 5: "C"}}
        """
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_b64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=800
            )

            wynik = response.choices[0].message.content.strip()
            st.success("✅ Analiza zakończona!")
            st.markdown("### 📋 Wynik sprawdzianu ucznia:")
            st.markdown(wynik)

        except Exception as e:
            st.error(f"Wystąpił błąd podczas OCR przez GPT: {e}")


