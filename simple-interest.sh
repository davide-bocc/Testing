#!/bin/bash

# Calcolo degli interessi semplici
read -p "Inserisci il capitale: " P
read -p "Inserisci il tasso di interesse annuale (in %): " r
read -p "Inserisci il numero di anni: " t

# Formula: I = P * r * t / 100
I=$(echo "$P * $r * $t / 100" | bc)

echo "L'interesse semplice è: $I
