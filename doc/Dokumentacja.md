# Opis
W grze uczestniczy N drużyn (na razie dwie). Każda drużyna ma 
M postaci (niekoniecznie różnych). Każda postać jest
dataklasą - patrz backend/Character.py. Informacje
przekazujemy przy pomocy paczek - również dataklas. 
## Paczka
Na paczkę składa się:
- id drużyny
- target (host)
- payload - krotka (komenda, zmienna, wartość)

gdzie targetem mogą być:
- broadcast - wszystkie hosty w sieci
- player_unicast - gracz musi wybrać target
- target_unicast (ogólnie adres) - adres hosta
- random_unicast - paczka do losowego hosta
- self_unicast - paczka do siebie

komendą może być:
- SET - ustaw wartość zmiennej na wartość
- INCREASE - zwiększ wartość zmiennej o wartość
- DECREASE - zmniejsz wartość zmiennej o wartość
- EXECUTE - wykonaj polecenie (np. funkcję związaną z umiejętnością)
- NO_REMAIN - wysyłana, gdy w podsieci żadne z urządzeń nie
ma oczekujących paczek i nie oczekuje na żadne paczki
- END_TURN - wysyłany przez router do wszystkich urządzeń,
gdy tura się kończy
- QUERY - zapytanie urządzenia o informacje (np. o listę postaci w drużynie)
- REPLY - odpowiedź na zapytanie. Odpowiadamy wartością jakieś zmiennej, gdzie wartość 
czym kolwiek ta wartość jest (np. string).

zmienną mogą być statystyki postaci (np. hp, mp),
ale są też inne zmienne:
- ABILITIES - do zapytania o umiejętności postaci
- STATS - pytamy o statystyki postaci
- NAME - pytamy o nazwę postaci
- CHARACTER - pytamy o id postaci (np. ktora postać wybieramy do ataku)
- ABILITY - pytamy o opis umiejetnosci postaci


## System komunikacji
Mamy trzy klasy urządzeń - router, switch, host. Router to w 
pewnym sensie menedżer gry - on przekazuje pakiety
między drużynami i zarządza turą. Switch to menedżer drużyny -
on decyduje, kiedy drużyna zakańcza turę i decyduje o odpytywaniu
konkretnych postaci, również przeprowadza z nimi aktualizacje.
Host - to uniwersalna nakładka na urządzenie nie służące
do przekazywania pakietów - w tym celu hosty komunikują się ze
switchami. Każde urządzenie musi implementować metody send_packet
i receive_packet przez rozszerzanie klasy NetDevice. Urządzenia łączymy
poprzez klasę Connection (warstwa abstrakcji, przez którą przesyłamy komunikaty).
Połączenia są owiniętę w klasę Interface, która zapewnia nam adres sieci i adres
hosta dla połączenia. 




Menu powinno odpala serwer/klienta komenda