## 1. Intelegerea problemei
Se da un sir de $n$ numere intregi (unde $1 \le n \le 100.000$). Trebuie sa gasim suma maxima pe care o poate avea o *secventa* (subsir de elemente *consecutive*) din sirul dat. 
- **Atentie:** Secventa trebuie sa fie neaparat continua (de la indicele $i$ la $j$).
- **Restricții:** $n$ poate ajunge pana la $100.000$, ceea ce inseamna ca o solutie in timp $O(n^2)$ nu se va incadra in timpul limita de la bacalaureat/olimpiada ($1$ secunda). Avem nevoie de o complexitate liniara $O(n)$.

## 2. Ideea de rezolvare
- **Abordarea naiva ($O(n^2)$ sau $O(n^3)$):** Luam toate perechile posibile de capete $(i, j)$ ale secventei, calculam suma elementelor dintre ele si o retinerm pe cea maxima. Prea lenta pentru $n = 100.000$.
- **Solutia optima - Algoritmul lui Kadane ($O(n)$):** 
  Parcurgem sirul element cu element si tinem evidenta a două sume:
  1. `suma_curenta`: suma secventei curente pe care o construim.
  2. `suma_maxima`: cea mai mare suma gasita pana in momentul curent.
  
  La fiecare pas, cand adaugam elementul curent $x$ la `suma_curenta`, avem doua optiuni:
  - Extindem secventa anterioara adaugand $x$.
  - Incepem o secventa noua chiar de la elementul $x$ (daca `suma_curenta` anterioara devenise negativa, fiind anulata sau micsorata de elementele anterioare, nu are rost sa o caram dupa noi).
  
  Matematic: `suma_curenta = max(x, suma_curenta + x)`, iar `suma_maxima = max(suma_maxima, suma_curenta)`.

## 3. Codul complet
```cpp
#include <iostream>
#include <algorithm>

using namespace std;

int main() {
    // Optimizare pentru citire/afisare rapida
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n)) return 0;

    int x;
    cin >> x; // Citim primul element

    long long suma_curenta = x;
    long long suma_maxima = x;

    // Citim restul de n-1 elemente si aplicam algoritmul lui Kadane din zbor
    for (int i = 2; i <= n; ++i) {
        cin >> x;
        // Decidem: continuam secventa veche sau incepem una noua de la x?
        suma_curenta = max((long long)x, suma_curenta + x);
        // Actualizam maximul global
        suma_maxima = max(suma_maxima, suma_curenta);
    }

    cout << suma_maxima << "\n";

    return 0;
}
```

## 4. Explicatie pas cu pas
1. **Citirea primului element:** Initializam atat `suma_curenta` cat si `suma_maxima` cu primul element citit. Folosim tipul `long long` pentru a preveni posibile depasiri de integer (overflow) in cazul in care sumele sunt foarte mari.
2. **Bucla `for`:** Parcurgem elementele de la al doilea pana la al $n$-lea. Nu este nevoie sa salvam tot sirul intr-un tablou (`vector` sau `array`), deoarece procesam elementele on-line (pe masura ce le citim), ceea ce ne economiseste memoria.
3. **Linia `suma_curenta = max((long long)x, suma_curenta + x);`**: Aici este "magia" lui Kadane. Daca suma acumulata pana acum a devenit negativa (`suma_curenta < 0`), ea va trage in jos orice suma viitoare. Prin urmare, e mai profitabil sa o abandonam si sa pornim o noua secventa incepand direct cu elementul curent `x`.
4. **Linia `suma_maxima = max(suma_maxima, suma_curenta);`**: Comparam maximul istoric cu valoarea `suma_curenta` obtinuta acum si o actualizam daca este cazul.

## 5. Exemplu de rulare
Pentru intrarea:
`8`
`-2 1 -3 4 -1 2 1 -5`

- `i = 1`: `x = -2` $\rightarrow$ `suma_curenta = -2`, `suma_maxima = -2`
- `i = 2`: `x = 1` $\rightarrow$ `suma_curenta = max(1, -2 + 1) = max(1, -1) = 1`. `suma_maxima = max(-2, 1) = 1`
- `i = 3`: `x = -3` $\rightarrow$ `suma_curenta = max(-3, 1 + (-3)) = max(-3, -2) = -2`. `suma_maxima = max(1, -2) = 1`
- `i = 4`: `x = 4` $\rightarrow$ `suma_curenta = max(4, -2 + 4) = max(4, 2) = 4`. `suma_maxima = max(1, 4) = 4`
- `i = 5`: `x = -1` $\rightarrow$ `suma_curenta = max(-1, 4 + (-1)) = max(-1, 3) = 3`. `suma_maxima = max(4, 3) = 4`
- `i = 6`: `x = 2` $\rightarrow$ `suma_curenta = max(2, 3 + 2) = max(2, 5) = 5`. `suma_maxima = max(4, 5) = 5`
- `i = 7`: `x = 1` $\rightarrow$ `suma_curenta = max(1, 5 + 1) = max(1, 6) = 6`. `suma_maxima = max(5, 6) = 6`
- `i = 8`: `x = -5` $\rightarrow$ `suma_curenta = max(-5, 6 + (-5)) = max(-5, 1) = 1`. `suma_maxima = max(6, 1) = 6`

Iesire finala: `6` (secventa este `[4, -1, 2, 1]`).

## 6. Complexitate
- **Timp:** $O(n)$, deoarece parcurgem sirul o singura data folosind o bucla de la $1$ la $n$. Operatiile din interiorul buclei sunt elementare ($O(1)$).
- **Memorie:** $O(1)$, pentru ca nu stocam numerele intr-un tablou. Folosim doar cateva variabile simple, indiferent de marimea lui $n$.