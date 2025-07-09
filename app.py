import streamlit as st
from test_generator import generuj_test
import pytesseract
from PIL import Image
import json
import openai
import base64

openai.api_key = st.secrets["openai_api_key"]

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
    st.subheader("📤 Sprawdź test ucznia")

    uploaded_image = st.file_uploader("Prześlij zdjęcie lub skan testu ucznia (JPG/PNG)", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        st.image(uploaded_image, caption="Załadowany test", use_column_width=True)

        try:
            # Zakoduj obraz do base64
            image_data = base64.b64encode(uploaded_image.read()).decode("utf-8")

            prompt = (
                "Na tym zdjęciu znajduje się kartka z odpowiedziami do testu (np. 1. A, 2. B…). "
                "Proszę odczytaj odpowiedzi i wypisz je w formacie:\n1. A\n2. B\n3. C itd."
            )

            with st.spinner("Rozpoznaję odpowiedzi..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                            ]
                        }
                    ]
                )

                extracted_text = response.choices[0].message.content

            st.subheader("📝 Rozpoznany tekst:")
            st.text(extracted_text)

            # Przykładowy klucz odpowiedzi – możesz potem to zautomatyzować
            poprawne_odpowiedzi = {
                1: "C",
                2: "A",
                3: "D",
                4: "B",
                5: "C"
            }

            def sprawdz_test(tekst, klucz):
                punkty = 0
                feedback = ""
                for nr, poprawna in klucz.items():
                    if f"{nr}. {poprawna}" in tekst or f"{nr}.{poprawna}" in tekst or f"{nr} {poprawna}" in tekst:
                        punkty += 1
                        feedback += f"{nr}. ✅ poprawna\n"
                    else:
                        feedback += f"{nr}. ❌ błędna lub brak odpowiedzi (oczekiwano: {poprawna})\n"
                return punkty, feedback

            score, szczegoly = sprawdz_test(extracted_text, poprawne_odpowiedzi)

            st.success(f"Wynik: {score}/{len(poprawne_odpowiedzi)}")
            st.markdown("### Szczegóły oceny:")
            st.markdown(szczegoly)

        except Exception as e:
            st.error(f"Wystąpił błąd podczas OCR: {e}")

