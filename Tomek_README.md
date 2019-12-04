# Geometric Algorithms Project

## Introduction

Problemem tego projektu jest wyznaczanie **przecięcia dwóch podziałów** na płaszczyźnie dwuwymiarowej oraz wyznaczenie podziału z tego wynikającego. Problem ten jest podstawą operacji logicznych na zbiorach, które z kolej są niezbędne przy różnego rodzaju problemach płaszczyzn dwuwymiarowych, np. w geografii lub szeroko pojętym mapowaniu.

Rozwiązanie przedstawione opiera się na dwóch kluczowych elementach:
- [strukturze danych Doubly Connected Edge List (DCEL)](../utils/data_structures.py)
- [zmodyfikowanym algorytmie zamiatania](./sweeping_algorithm.ipynb)

Szczegóły każdego z nich są opisane w powyższych linkach.


## Data structures

Strukturą wykorzystywaną w algorytmie jest _Doubly Connected Edge List_ (DCEL), która składa się z struktur:

* _Vertex_ - klasa wierzchołków
* _Hedge_ - klasa półkrawędzi (wektorów - każda krawędź składa się z dwóch przeciwnie zwróconych półkrawędzi)
* _Face_ - klasa ścian podziału

DCEL zawiera też w sobie metodę dodawania półkrawędzi generującą odpowiedni wierzchołki i ściany.

Na potrzeby algorytmu zamiatania występują też klasy _Event_ i _Line_.

