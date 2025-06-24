# ziggyquest

## Setup
### Jak zainstalować
1. Pobierz repozytorium z https://github.com/Tysek64/ziggyquest
2. Jeżeli jesteś na systemie z bashem uruchom `install.sh`. Jeżeli jesteś na windowsie, to zainstaluj WSLa i spróbuj ponownie.
3. Jeżeli bardzo chcesz uruchomić na windowsie to stwórz wirtualne środowisko ręcznie wg wymagań z requirements.txt

### Jak uruchomić
1. Jeżeli jesteś na systemie z bashem uruchom `run.sh`
2. Jeżeli jesteś na windowsie, to aktywuj wirtualne środowisko i w folderze głównym projektu wykonaj komendę `python -m src.GUIMain`

### Jak odinstalować
1. Jeżeli jesteś na systemie z bashem uruchom `uninstall.sh`
2. Jeżeli jesteś na windowsie, to usuń foldery z venvem

## Jak grać
### Gra na jednym komputerze:
1. Wybierz opcje Singleplayer

### Gra po LANie
1. Wybierz opcje Multiplayer
2. Wpisz adres ip komputera i zaznacz czerwony kwadrat na komputerze, który hostuje rozgrywkę, wciśnij confirm
3. Na drugim komputerze wpisz adres pierwszego komputera i nie zaznaczaj czerwonego kwadratu, wciśnij confirm

## Zasady gry
Jest to gra turowa, w której każdy gracz posiada drużynę postaci. Celem gry jest zabicie wszystkich postaci drugiego gracza.
Rozgrywka rozpoczyna się od wyboru postaci, gracze dobierają naprzemienie postacie z różnych kategorii. Po wyczerpaniu
postaci rozpoczyna się walka.
Podczas walki każdy gracz wybiera postać, którą chce wykonać ruch. Każda postać ma swoje unikalne umiejętności, które są
wyjaśnione w pliku `characters/manual.html`. Każda postać ma swoje HP, MP, nazwę, które widać na karcie postaci w walce.

HP - punkty zdrowia postaci. Gdy hp spadnie do 0 postać umiera i nie można wykonać nią ruchu do momentu przywrócenia hp
MP - punkty magii. Każda umiejętność wiąże się z kosztem w mp. Jeżeli umiejętność wymaga większej liczby mp niż obecna, to
nie można jej użyć.

## Edycja postaci
Każda postać jest zapisywana w pliku JSON. Do tworzenia postaci wystarczy uruchomić w przeglądarce plik `characters/creator.html`,
w którym jest prosty interfejs do tworzenia nowych postaci. Plik z postacią należy umieścić w katalogu określającym jej kategorie
w katalogu `characters` np. `characters/Kategoria I`.
