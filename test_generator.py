from openai import OpenAI
import os
import streamlit as st

def generuj_test(temat, klasa, liczba_zadan, trudnosc, typ):
    client = OpenAI(api_key=st.secrets["openai_api_key"])

    prompt = (
        f"Stwórz {liczba_zadan} zadań matematycznych dla uczniów klasy {klasa}. "
        f"Temat: {temat}. "
        f"Typ zadań: {typ}. "
        f"Poziom trudności: {trudnosc}. "
        f"Przy tworzeniu zadań kieruj się testem ósmoklasisty w szkołach podstawowych który jest najważniejszym testem w szkole podstawowej. "
    )
    
    if typ == "zamknięte":
        prompt += (
            "Każde zadanie powinno zawierać cztery możliwe odpowiedzi oznaczone jako A), B), C), D). "
            "Tylko jedna odpowiedź jest poprawna i powinna być oznaczona np. [✓]. "
            "Nie używaj LaTeX ani nawiasów \\frac — zapisuj ułamki w formacie zwykłym (np. 1/2). "
            "Zadania i odpowiedzi zapisuj po polsku w formacie:\n\n"
            "Zadanie: ...\nA) ...\nB) ...\nC) ...\nD) ...\nPoprawna odpowiedź: ...\n"
    )
    elif typ == "mieszane":
        prompt += (
        "Stwórz mieszany zestaw zadań — maksymalnie 1/3 z nich powinno być zamkniętych (z odpowiedziami A-D), reszta otwarte. "
        "Zadania zamknięte powinny zawierać 4 odpowiedzi, tylko jedna poprawna. "
        "Zadania otwarte powinny zawierać odpowiedź w osobnej linii. "
        "Ostatnie zadanie w zestawie powinno być bardziej złożone może mieć dodatkowy kontekst lub wymagać kilku kroków obliczeniowych. "
        "Nie używaj LaTeX ani \\frac, zapisuj ułamki jako 1/2. "
        "Pisz wyłącznie po polsku."
    )
    else:
        prompt += (
        "Wszystkie zadania powinny być otwarte i mieć prostą, przejrzystą strukturę. "
        "Pod każdym zadaniem podaj odpowiedź w osobnej linii. "
        "Ostatnie zadanie powinno być bardziej złożone – np. z dodatkową treścią lub krokami. "
        "Nie używaj LaTeX ani \\frac, zapisuj ułamki jako 1/2. "
        "Pisz wyłącznie po polsku."
    )


    try:
        response = client.chat.completions.create(
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
        st.error(f"Błąd: {e}")
        return None
