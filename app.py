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
    st.subheader("📤 Sprawdź test ucznia")

    odpowiedzi_input = st.text_area(
        "Wklej odpowiedzi ucznia (np. 1. A, 2. B, ...):",
        height=200,
        placeholder="Przykład:\n1. C\n2. A\n3. B\n4. D\n5. C"
    )

    if st.button("Sprawdź odpowiedzi"):
        if odpowiedzi_input.strip() == "":
            st.warning("Wprowadź odpowiedzi ucznia.")
        else:
            with st.spinner("Wysyłam dane do modelu GPT..."):
                client = OpenAI(api_key=st.secrets["openai_api_key"])

                prompt = f"""
Na podstawie poniższych odpowiedzi ucznia wygeneruj słownik w formacie Python:
{{1: "C", 2: "A", ...}}.
Jeśli numer lub litera są nieczytelne lub błędne – pomiń lub wpisz "?".

Odpowiedzi ucznia:
\"\"\"{odpowiedzi_input}\"\"\"
"""

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Jesteś pomocnym asystentem nauczyciela matematyki."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0,
                    max_tokens=500
                )

                odpowiedzi_tekst = response.choices[0].message.content.strip()
                st.subheader("📦 Odpowiedzi ucznia (parsowane):")
                st.code(odpowiedzi_tekst)

                try:
                    odpowiedzi_ucznia = eval(odpowiedzi_tekst)
                except Exception as e:
                    st.error(f"Nie udało się sparsować odpowiedzi: {e}")
                    odpowiedzi_ucznia = {}

                poprawne_odpowiedzi = {
                    1: "C",
                    2: "A",
                    3: "D",
                    4: "B",
                    5: "C"
                }

                def sprawdz_test(odpowiedzi_ucznia, klucz):
                    punkty = 0
                    feedback = ""
                    for nr, poprawna in klucz.items():
                        odp = odpowiedzi_ucznia.get(nr, "?")
                        if odp == poprawna:
                            punkty += 1
                            feedback += f"{nr}. ✅ poprawna\n"
                        else:
                            feedback += f"{nr}. ❌ błędna (oczekiwano: {poprawna}, otrzymano: {odp})\n"
                    return punkty, feedback

                if odpowiedzi_ucznia:
                    score, szczegoly = sprawdz_test(odpowiedzi_ucznia, poprawne_odpowiedzi)
                    st.success(f"Wynik: {score}/{len(poprawne_odpowiedzi)}")
                    st.markdown("### Szczegóły oceny:")
                    st.markdown(szczegoly)

