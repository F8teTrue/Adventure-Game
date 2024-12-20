# Adventure Game

**Dette er en README for Adventure Game mappen og omhandler ikke andre filer eller mapper.**

## 📖 Om spillet
**Adventure Game** er et tekstbasert RPG der du utforsker områder, aksepterer oppdrag, bekjemper monstre, og samler gjenstander. Målet er å fullføre oppdragene mens du oppgraderer karakteren din og overlever utfordringene i en mystisk verden.

---

## 🎮 Funksjonalitet

### Hovedmekanikker
- **Utforskning**: Utforsk ulike områder, kjemp mot monstre og mystiske vesner, og finn skatter.
- **Oppdrag/Quests**: Aksepter kamp eller historie baserte oppdrag fra Quest Hall. Slik kommer man videre i spillet.
- **Karakterprogresjon**: Samle erfaringspoeng (XP) for å øke nivået ditt og forbedre attributtene dine.
- **Handel**: Kjøp og selg gjenstander som kan hjelpe deg på eventyrene og reisene dine.
- **NPC-interaksjoner**: Gjennom historie oppdrag kan du snakke med NPC-er for å avdekke historien og låse opp nye områder.

### Spillkomponenter
| Komponent       | Beskrivelse |
|-----------------|-------------|
| **Karakter**    | Lag din egen karakter og oppgrader dens ferdigheter. |
| **Områder**     | Lås opp og utforsk områder med varierende vanskelighetsgrader. |
| **Kamper**      | Bekjemp monstre ved hjelp av ulike gjenstander. |
| **Historie**    | Opplev en sammenhengende fortelling gjennom oppdrag. |

---

## 🚀 Komme i gang

### Systemkrav
- **Python 3.10+**
- Operativsystem: Windows er testet og fungerer. Burde fungere med MacOS eller Linux, men har ikke testet.

### Installasjon
1. **Klon repoet**:
   ```bash
   git clone https://github.com/F8teTrue/Adventure-Game.git
   cd Adventure-Game
   ```
   **Programmet må kjøres, mens man er i mappen "Adventure-Game" på grunn av filer som åpnes i koden og pathen til dem. Hvis man vil kjøre koden fra "Adventure Game" mappen, må man endre fil paths i "items.py" og "game_data.py".**

2. **Pip installasjoner**:
   ```bash
   pip install -r "Adventure Game/requirements.txt"
   ```
   Eller manuelt innstaller Python-pakkene Colorama og Keyboard.
3. **Start spillet**:
   ```bash
   python "Adventure Game/main.py"
   ```
   Eller kjør filen "main.py" fra din code editor.

## 📜 Spilleinstruksjoner

### Oppdrag
1. Gå til Quest Hall for å velge oppdrag.
2. Følg oppdragets mål, som kan inkludere å utforske et område, bekjempe monstre, eller snakke med NPC-er. Man låser opp områder gjennom historie oppdrag.

### Utforskning
- Velg et område å utforske basert på oppdrag eller hvis du bare vil utforske og kjempe.
- Møt monstre i en tur basert kampstruktur og finn skatter.

### Butikker
- Bruk opptjent gull til å kjøpe gjenstander som våpen, rustning eller eliksirer.

### Hvordan navigere
**Home** er der man starter og fungerer som et hovedpunkt i spillet. **Home** gir deg tilgang til:
- **Village**: Dette er den lokale landsbyen hvor spilleren kan besøke en butikk og Quest Hall, samt snakke med NPC-er etter å ha tatt på seg historie oppdrag.
- **Explore**: Dette lar deg velge mellom områder spilleren har låst opp for utforskning.
- **Inventory**: Lar spilleren bruke gjenstandene de eier. Man har også tilgang til dette mens man utforsker.
- **Status**: Lar spilleren se flere av attributtene til karakteren de spiller.

## Videreutvikling
Planlagte funksjoner for fremtiden inkluderer:
- Lagring av progresjon.
- Flere områder med unike monstre, hendelser og skatter.
- En mer kompleks historie og flerveisvalg.
- Flere gjenstander.
- Overgang fra rent tekstbasert til noe mer visuelt.

## Lisens
Dette prosjektet er lisensiert under [MIT-lisensen](LICENSE).
