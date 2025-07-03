import openai
import os
import streamlit as st

def generuj_test(temat, klasa, liczba_zadan, trudnosc, typ):
    openai.api_key = st.secrets["openai_api_key"]

    prompt = (
        f"Stwórz {liczba_zadan} zadań matematycznych dla uczniów klasy {klasa}. "
        f"Temat: {temat}. "
        f"Typ zadań: {typ}. "
        f"Poziom trudności: {trudnosc}. "
        f"Każde zadanie umieść jako osobny punkt. "
        f"Pod każdym zadaniem umieść odpowiedź w formacie:\nOdpowiedź: ...\n"
        f"Nie twórz tabel. Pisz wyłącznie po polsku."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jesteś pomocnym asystentem nauczyciela matematyki."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Błąd:", e)
        return None
