"""
Rezolvitor de probleme de informatica cu Gemini (varianta locala).

Rulare:
    python rezolvitor.py                 -> rezolva problema din ENUNT (mai jos)
    python rezolvitor.py problema.txt    -> rezolva problema din fisierul dat

Cheia API se citeste din variabila de mediu GEMINI_API_KEY.
"""

import logging
import os
import sys
import time

from google import genai
from google.genai import errors, types

logging.getLogger("google_genai.models").setLevel(logging.ERROR)

# Primul e cel folosit; daca e supraincarcat, se trece automat la urmatorul
MODELE = ["gemini-3.5-flash-lite", "gemini-2.5-flash", "gemini-3.5-flash"]
LIMBAJ = "C++"

ENUNT = """
Se citeste un numar natural n (1 <= n <= 100000) si apoi n numere intregi.
Sa se determine suma maxima a unei secvente de elemente consecutive din sir.

Exemplu:
Intrare: 8
         -2 1 -3 4 -1 2 1 -5
Iesire:  6
"""

INSTRUCTIUNI = """Esti un profesor de informatica foarte bun, care pregateste elevi pentru bacalaureat si olimpiada.
Primesti enuntul unei probleme si raspunzi in limba romana, structurat EXACT asa:

## 1. Intelegerea problemei
Ce se cere, ce date avem, ce restrictii conteaza.

## 2. Ideea de rezolvare
Algoritmul ales si DE CE l-ai ales (mentioneaza pe scurt si o abordare mai naiva, daca exista).

## 3. Codul complet
Cod corect, complet, compilabil, cu comentarii scurte.

## 4. Explicatie pas cu pas
Explica fiecare parte importanta a codului.

## 5. Exemplu de rulare
Ia un exemplu concret si arata cum evolueaza variabilele pas cu pas.

## 6. Complexitate
Complexitatea in timp si in memorie, cu justificare.
"""


def genereaza_stream(client, contents, config=None, incercari_per_model=2):
    """Incearca modelele pe rand; la 503 / 429 asteapta putin si reincearca, apoi trece la alt model."""
    for model in MODELE:
        for incercare in range(incercari_per_model):
            try:
                primul = True
                for bucata in client.models.generate_content_stream(
                    model=model, contents=contents, config=config
                ):
                    if primul:
                        print(f"[Model folosit: {model}]\n")
                        primul = False
                    yield bucata
                return
            except (errors.ServerError, errors.ClientError) as e:
                if getattr(e, "code", None) not in (429, 500, 503):
                    raise
                print(f"[{model}: {e.code}, reincerc...]")
                time.sleep(3 * (incercare + 1))
    raise RuntimeError("Toate modelele sunt indisponibile acum. Incearca din nou peste cateva minute.")


def rezolva_problema(client, enunt, limbaj=LIMBAJ):
    prompt = f"Limbaj de programare: {limbaj}\n\nEnuntul problemei:\n{enunt.strip()}"
    config = types.GenerateContentConfig(system_instruction=INSTRUCTIUNI)

    text = ""
    for bucata in genereaza_stream(client, prompt, config):
        if bucata.text:
            print(bucata.text, end="", flush=True)
            text += bucata.text
    print()
    return text


def main():
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("Lipseste variabila de mediu GEMINI_API_KEY.")

    enunt = ENUNT
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            enunt = f.read()

    client = genai.Client()  # citeste automat GEMINI_API_KEY
    raspuns = rezolva_problema(client, enunt)

    with open("solutie.md", "w", encoding="utf-8") as f:
        f.write(raspuns)
    print("\n[Raspunsul a fost salvat si in solutie.md]")


if __name__ == "__main__":
    main()
