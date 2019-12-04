# Geometric Algorithms Project

### **List of contents**
- [Introduction](#introduction)
- [Algorithm](#algorithm)
- [Data structures](#data-structures)
- [Implementation details](#implementation-details)
- [Bibliography](#bibiliography)

## Introduction

Stated issue is to compute **subdivision overlay** on two-dimensional surface and to compute the resulting subdivision. This problem is neccessary to logical operations on subdivisions which form methods used in map-related operations, like in computer design tools, cartography or geology.

Following solution to stated problem is based on two key elements
* Data structure keeping elements of subdivision - [Double Connected Edge List (DCEL)](./utils/data_structures.py)
* Algorithm detecting overlay subdivision - [modified sweeping algorithm](./sweeping_algorithm.ipynb)

Project also includes visualisation and test data sets.

## Algorithm

Algorithm resembles sweeping algorithm that detects points of intersections in a set of line segments, however it is based on DCEL instead of more simple data structures. It is also extended by adding intersection points to set of vertexes and followingly created edges.

## Data structures

Structure used in project is _Doubly Connected Edge List_ (DCEL), which is a doubly linked list consisting of elements:

* _Vertex_ - representing vertexes of subdivisions
* _Hedge_ - representing edges in form of two vectors oppositly directed (each one is a half-edge - here: hedge)
* _Face_ - **TEGO NIE UŻYWAMY TO CHYBA TRZEBA WYJEBAC**


## Bibliography

* Computational Geometry Algorithms and Applications, 3rd Ed - de Berg
* **DOPISAC**