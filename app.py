import streamlit as st
from test_generator import generuj_test
import pytesseract
from PIL import Image
import json
from openai import OpenAI
import base64

st.set_page_config(page_title="Asystent AI dla nauczyciela matematyki")

st.markdown("""
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#2b2b2b">
""", unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["openai_api_key"])



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

    with st.form("formularz_klucz"):
        liczba_zadan = st.number_input("Podaj liczbę zadań:", min_value=1, max_value=20, step=1)
        zadania = []
        for i in range(1, liczba_zadan + 1):
            col1, col2, col3 = st.columns([1, 2, 2])
            with col1:
                typ = st.selectbox(f"Zadanie {i} - Typ", ["zamknięte", "otwarte"], key=f"typ_{i}")
            with col2:
                odp = st.text_input(f"Poprawna odpowiedź (A/B/C/D lub wynik)", key=f"odp_{i}")
            with col3:
                pkt = st.number_input(f"Punkty", min_value=1, max_value=10, step=1, key=f"pkt_{i}")
            zadania.append({"nr": i, "typ": typ, "odp": odp.upper(), "pkt": pkt})

        submit_klucz = st.form_submit_button("Zapisz klucz odpowiedzi")

    if submit_klucz:
        st.session_state["klucz_odpowiedzi"] = zadania
        st.success("Klucz odpowiedzi zapisany!")

    uploaded_image = st.file_uploader("Prześlij zdjęcie lub skan testu ucznia (JPG/PNG)", type=["png", "jpg", "jpeg"])

    if uploaded_image and "klucz_odpowiedzi" in st.session_state:
        st.image(uploaded_image, caption="Załadowany test", use_column_width=True)

        image_bytes = uploaded_image.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        try:
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Jesteś nauczycielem sprawdzającym test matematyczny na podstawie zdjęcia."},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Na podstawie poniższego zdjęcia rozpoznaj odpowiedzi ucznia. Następnie porównaj je z tym kluczem: {st.session_state['klucz_odpowiedzi']}. Oceń każdą odpowiedź, przyznaj punkty i podaj wynik końcowy."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_b64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )

            wynik = response.choices[0].message.content
            st.markdown("### 📋 Wynik oceny:")
            st.markdown(wynik)

        except Exception as e:
            st.error(f"Wystąpił błąd podczas OCR przez GPT: {e}")

    elif uploaded_image:
        st.warning("Najpierw uzupełnij klucz odpowiedzi.")


