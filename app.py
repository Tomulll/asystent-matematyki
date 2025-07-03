import streamlit as st
from test_generator import generuj_test

st.set_page_config(page_title="Asystent AI dla nauczyciela matematyki")

st.title("🧠 Asystent AI – Generator Sprawdzianów")

st.markdown("Wypełnij formularz poniżej, a asystent AI wygeneruje gotowy test z matematytki wraz z odpowiedziami.")

with st.form("formularz_testu"):
    temat = st.text_input("Temat sprawdzianu (np. Dodawanie ułamków):")
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

