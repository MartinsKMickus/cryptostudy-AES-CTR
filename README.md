# cryptostudy-AES-CTR
Studiju projekts praktiskās kriptogrāfijas kursā.

## Prasības
Nošifrēt failu un atšifrēt nošifrēto failu, izmantojot šādu algoritmu:
- Failu šifrs: CTR (bez padding).
- Bitu bloku šifrs: AES.
- Atslēgas ievade: 128 bitu kā 32 16-nieku sistēmas simboli (0,...9,a,...,f). <i>0x0123456789ABCDEF0123456789ABCDEF</i>

### Ievade/Izvade
<b>Šifrēšana:</b>
- Norāde uz šifrējamo failu.
- Šifrēšanas atslēga.
- Nonce 16 bitus gara jeb 4 heksadecimālie simboli.
- Darbība/Poga "šifrēt".
Rezultātā izveido failu, kurā 1.bloks ir 128 (AES) bitu
inicializācijas vektors, tālāk seko nošifrētais fails.

<b>Atšifrēšana:</b>
- Norāde uz atšifrējamo failu.
- Šifrēšanas atslēga
- Darbība/Poga "atšifrēt".

## Palaišana
Programmu vajadzētu palaist ar iespēju pie izsaukšanas norādīt parametrus:
- Šifrēt: `python program.py encrypt 'file' KEY NONCE`
- Atšifrēt `python program.py decrypt 'file' KEY`
