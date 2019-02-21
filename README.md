# MusicPlayer
Dette er et hobbyprojekt. Det er en musikafspiller, som vil afspille YouTube videoer fra en queue på host-computeren.
Brugere logger ind på hostens ip-adresse og tilføjer musik ved at søge på titlen af sangen, så vil serveren finde sangen på YouTube og tilføje den til køen.
Dette kan f.eks. kobles på en Raspberry Pi, som sidder til en højtaler for at gøre det muligt at lade enhver på netværket tilføje sange til playlisten.
Det er skrevet i Python 3 med et microframework kaldet Flask til at klare hjemmesidedelen. 
Der bliver brugt et css-framework kaldet Bulma for at få hjemmesiden til at se pæn ud.

## Hvad jeg lærte
* Jeg lærte om web-scraping af hjemmesider. Her var det specifikt at finde linket af den øverste video i søgeresultaterne.
* Jeg lærte om youtube-dl, og hvordan man kan streame musik eller videoer ved hjælp af VLC.
* Jeg lærte at lave en JavaScript forbindelse mellem server og client ved hjælp af socket.io
* Jeg lærte at bruge Bulma sammen med HTML og CSS for at lave en pæn hjemmeside.

