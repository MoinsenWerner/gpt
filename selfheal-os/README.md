# Self-Heal OS

Ein einfaches Framework, um Linux-Systeme zu überwachen und bei Problemen automatisch zu reagieren. Das Projekt umfasst einen Daemon, ein CLI, sowie eine Web-API mit minimalem Frontend.

## Struktur
Siehe Verzeichnisbaum im Projekt. Wichtigste Komponenten:
* **daemon/** überwacht Ressourcen und Dienste, reagiert bei Fehlern
* **cli/** Werkzeug zur manuellen Steuerung
* **web/** FastAPI-Backend (Port 23673) und kleines React-Frontend

Das Projekt ist als Ausgangspunkt gedacht und kann weiter ausgebaut werden.
