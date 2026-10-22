# Nové vzhľady kalendára: koncepty a prompty

Pracovný dokument na spoločnú revíziu. Nič z toho sa zatiaľ negenerovalo.

## Pravidlá pre všetky koncepty
- **Pre príležitosť a klienta, nie len Vianoce.** Každý koncept stojí na konkrétnom dôvode klienta, napríklad výročie, nová séria, otvorenie predajne alebo začiatok sezóny. Vzorom je Harfa Sport a „Slavíme 30 let“.
- **Klienti sú anonymní** (napr. „Duty free na hranici“), bez log a bez reálnych značiek v obraze.
- **Funkčne nič navyše oproti appke.** Kalendár vie toto:
  - N okienok,
  - stavy dnes, otvorené, zamknuté a zmeškané,
  - odmenu typu `sleva`, `doprava`, `darek`, `prodejna`, `akce` (ikony `ICO`),
  - kód na kopírovanie,
  - odpočet,
  - CTA tlačidlo.

  Vzhľad mení len to, ako to vyzerá.
- **Interakcia v deme (spoločná pre všetky vzhľady):**
  - Klik na dnešné okienko spustí animáciu otvorenia podľa vzhľadu, napríklad vysunutie kartičky ako vo veniec-moodboarde. Potom sa ukáže karta odmeny s kódom „Kopírovat“ a CTA.
  - Zamknuté okienko sa zatrasie s hláškou „Otevře se za X dní“.
  - Zmeškané okienko ukáže „Tento den propadl“.
- **Čísla a texty kreslí kód, nikdy obrázok.** Prompt vždy chce prázdne plochy bez textu, aby sedel jazyk, počet a súradnice.
- **Pohyb je v kóde (CSS/SVG)** nad obrázkom, ako hojdajúce sa vajíčko pri Veľkej noci. Rešpektuje `prefers-reduced-motion`.

## Kód, alebo Higgsfield?
Rozhoduje, čo sa má hýbať a ako presne musí sedieť počet okienok. **Všetko, čo sa skladá, otvára alebo počíta, kreslí kód (SVG/CSS).** Každý kus je samostatný prvok, dá sa animovať a presne sedí na počet dní aj farby klienta. Higgsfield je len tam, kde rozhoduje fotografická atmosféra a obraz je pozadie, nad ktorým kód kreslí okienka.

| # | Koncept | Médium | Prečo |
|---|---|---|---|
| 1 | Odpočet ke startu (stavebnica) | **celé v kóde** | raketa sa skladá z kociek, každá kocka je samostatný SVG prvok, ktorý dopadne a zacvakne |
| 2 | 7 nocí pro lepší spánek | Higgsfield foto + kódová vrstva (mesiac, para, záclona) | atmosféra spálne je fotografická |
| 3 | Cestovní pas | Higgsfield flat lay + razítka a listovanie v kóde | razítka musia niesť texty a dopadať |
| 4 | Víkendy na chalupě | Higgsfield mapa + trasa a pochodujúca bodka v kóde | maľovaná krajina, presná trasa |
| 5 | Obálky ve tvaru výročí | Higgsfield stena + obálky v kóde | tvar čísla a počet sa mení podľa klienta |

**Latka kvality:** každý koncept má jednu myšlienku, ktorá má začiatok a koniec. Napríklad pri rakete: odpočet, ku ktorému každý deň pribudne dielik, a na konci štart. Otvorenie okienka má byť fyzický zážitok (dopad, vysunutie, razítko), po ktorom príde karta odmeny s kódom. Prepínanie, mobil, klávesnica a `prefers-reduced-motion` musia fungovať ako hotový nástroj, nie ako statický obrázok.

## Higgsfield: spoločné nastavenie
- Model: **GPT Image 2.5** (`gpt_image_2_5`, variant `flare`), `quality: high`, `resolution: 2k`. Dobre drží kompozíciu, počty objektov aj fotoreál a vie editovať s referenciou, keď treba niečo opraviť.
- Pomer strán: **4:5** (demo plocha je 4:5, max 560 px). Pri širokej kompozícii 5:4.
- Jeden poriadne napísaný prompt na koncept a žiadne štyri varianty. Zlý výsledok doladíme editáciou.
- Postprocess:
  - orez na presný pomer,
  - export WebP, dlhšia strana ~1600 px, do ~300 kB,
  - zameranie súradníc okienok pomocným HTML.
- Zostatok k 22. 10. 2026: ~302 kreditov (starter). Pred každým generovaním ukážem cenu.

---

## 1. Hračky / stavebnice: „Odpočet ke startu“ ⭐ úplne iný layout, celé v kóde
**Klient (anonymne):** predajňa hračiek a stavebníc. Typ Sparkys alebo predajca, ktorý má sezónu stavebníc.
**Príležitosť:** štart novej série stavebníc.
**Dĺžka:** 10 dní, čo je odpočet T−10 až T−1.

**Myšlienka:** na odpaľovacej rampe stojí plán rakety. Každý deň zákazník odkryje jeden dielik: kocka dopadne na model, zacvakne a k nej príde dárok. Zmeškaný deň v modeli chýba a ostane len čiarkovaný obrys, čo je dôvod chodiť každý deň. Desiaty deň je raketa celá a odštartuje, rovnako ako nová séria.

**Čím je iný:** namiesto obrázka s okienkami je tu modrotlačový plán. Model rakety rastie zdola nahor a okienka sú rad desiatich kociek pod ním. Na displeji svieti „Start za X dny“.
**Médium:** izometrické kocky s čudlíkmi v SVG, bez Higgsfieldu.

**Odmeny (10):** −10 % na stavebnice · doprava zdarma · minifigúrka k nákupu · −15 % na novú sériu · stavanie s nami v predajni · sáčky dielikov 2+1 · −20 % nad 1 000 Kč · doprava zdarma · plagát novej série · **10. deň: −25 % na celú novú sériu**
**Farby:** plánový papier `#eef3fb`, modrotlač `#1f5fbf`, červená `#e3242b`, žltá `#ffcc00`. Font: Inter 900, JetBrains Mono na displej.

---

## 2. Bytový textil a doplnky: „7 nocí pro lepší spánek“
**Stav:** postavené (vzhľad `spani`). Obrázok vygenerovaný na prvý pokus: GPT Image 2.5, high, 2k, 2,75 kreditu, uložený ako `img/spani.webp` (1440×1800, ~200 kB). Farby podľa MK Ložkoviny (hnedá #483628, zlatá #c3a15a), bez loga. Okienka sú predmety v izbe, mesiac, hviezdy, para, lampa a sviečka sú v kóde. Siedma noc ukáže úplnok a „Dobrou noc“.

**Klient (anonymne):** e-shop s posteľnou bielizňou a bytovými doplnkami.
**Príležitosť:** uvedenie novej kolekcie / Svetový deň spánku (marec) / jesenná výmena perín.
**Dĺžka:** 7 dní („nocí“).

**Scéna:** útulná spálňa za súmraku. Okienka sú **predmety v izbe**: vankúš, perina, pléd, lampička, papuče, hrnček čaju a sviečka.
**Pohyb:**
- V okne za posteľou sa mesiac mení podľa počtu otvorených nocí (SVG fázy mesiaca ako ukazovateľ postupu).
- Záclona sa jemne vlní a zo šálky stúpa para.
- Otvorenie: predmet sa rozsvieti teplým svetlom a z vankúša sa vysunie „visačka“ s odmenou.

**Odmeny (7):** −15 % na obliečky · doprava zdarma · darček: levanduľový sprej · 2+1 na vankúše · −20 % na periny · predĺžené vrátenie na 100 nocí · **7. noc: súťaž o kompletnú výbavu postele**
**Farby:** krémová `#f5efe6`, šalviová `#8a9a7b`, nočná modrá `#24304a` a teplé svetlo `#ffcf8a`. Font: Georgia (nadpis), Inter.

**Prompt:**
```
Warm, cosy Scandinavian bedroom at dusk, photographed straight-on from the foot of the bed, vertical 4:5. A neatly made double bed with crisp linen bedding in cream and sage green, two plump pillows, a folded chunky knit throw at the foot of the bed. On the left a bedside table with a small glowing lamp and a ceramic mug of tea; on the right a bedside table with a lit candle in a glass. A pair of soft felt slippers on a round wool rug in front of the bed. Behind the bed a large window with sheer linen curtains, deep blue evening sky outside, an empty sky area in the upper part of the window. Exactly seven clearly separated, distinct hero objects: pillow, duvet, throw, lamp, mug, candle, slippers — each well spaced and not overlapping. Soft warm practical lighting mixed with cool blue window light, natural textures, editorial interior photography, no people, no text, no logos.
```

---

## 3. Duty free na hranici (Travel Free): „Cestovní pas“ ⭐ alternatíva iného layoutu
**Stav:** postavené (vzhľad `pas`). Higgsfield robí len stôl s cestovnými vecami po okrajoch (GPT Image 2.5, high, 2k, 2,75 kreditu, prvý pokus, `img/pas-stul.webp`). Farby podľa Travel Free (červená #e30613, grafit #242527, zlatá #f1c86f), bez loga. Razítka sú anonymné pobočky na hraniciach (HRANICE CZ/DE, CZ/AT), nie mestá. Pas, guilloche, 14 razítok s atramentovým okrajom, listovanie dvojstrán a záverečné razítko „PAS JE PLNÝ“ sú v kóde.

**Klient (anonymne):** sieť duty-free predajní na hraniciach (potraviny, káva, čokoláda, kozmetika a darčekové koše).
**Príležitosť:** letná sezóna ciest / výročie predajní.
**Dĺžka:** 14 dní.

**Čím je iný:** demo je **otvorený pas na stole**. Okienka sú prázdne rámčeky na razítka, 7 na každej dvojstrane, takže dve dvojstrany. Šípkami alebo swipe sa **listuje** (CSS 3D otočenie strany).
**Ako to otvorí:** razítko krajiny (SVG kreslené kódom: kruh s názvom mesta, dátum a ikona odmeny) „dopadne“ s jemným odrazom a stopou atramentu.
**Kód kreslí:** razítka a ich texty. Obrázok je len prázdny pas na stole s cestovnými drobnosťami.

**Odmeny (14):** −10 % na kávu · čokoláda zdarma k nákupu · −15 % kozmetika · darčekový kôš so zľavou · 2+1 sladkosti · tankovacia kupónová akcia · −20 % parfumy · ochutnávka v predajni · voucher na ďalší nákup · … · **14. deň: veľký cestovný kôš**
**Farby:** pasová bordová `#5b1e2d`, papier `#f3ecdd`, razítkové farby (modrá `#2952a3`, zelená `#2f7d4f`, červená `#c8352e`). Font: JetBrains Mono (razítka), Georgia.

**Prompt:**
```
Top-down flat lay on a warm wooden table: an open burgundy passport lying flat in the centre, its two inner pages blank cream paper with a very subtle fine guilloche security pattern and no text, no stamps, no photo, no numbers — completely empty pages ready for stamps. Around the passport, arranged neatly near the edges: a paper boarding-pass-shaped card with no readable text, a small bar of chocolate in plain gold foil, a takeaway cup of coffee, a small unbranded perfume bottle, sunglasses, a few coins, a sprig of lavender. Soft natural window light from the upper left, gentle shadows, travel lifestyle product photography, vertical 4:5, no logos, no brand names, no legible text anywhere.
```

---

## 4. Chaty a chalupy: „Víkendy na chalupě“
**Stav:** postavené (vzhľad `chalupa`) pre klienta typu chaty-chalupy-dds.cz, anonymne. Maľovaná mapa z Higgsfieldu (GPT Image 2.5, high, 2k, 2,75 kreditu, prvý pokus, `img/chalupa-mapa.webp`). Trasa je zameraná na piesočný chodník v obraze, zastávky sú špendlíky. Turista v štýle maskota klienta (šiltovka, žlté tričko, batoh) po otvorení dôjde po trase k ďalšej zastávke. Kalendár je týždenný (8 víkendov), hlášky počítajú v týždňoch. Farby: limetková #eef6d3, olivovo-zelená #7a9b0a, žltá #ffd200.

**Klient (anonymne):** prenájom chát a chalúp / outdoorový obchod.
**Príležitosť:** otvorenie letnej sezóny / spustenie bookingu.
**Dĺžka:** 8 víkendov (týždenný kalendár, okienko sa otvorí v piatok).

**Scéna:** ilustrovaná mapa krajiny s turistickým chodníkom. Okienka sú **zastávky**: chata, jazero, rozhľadňa, ohnisko, les, mostík, mlyn a kaplnka.
**Pohyb:**
- Kód nakreslí čiarkovanú trasu SVG cestou cez stredy okienok a po nej „kráča“ bodka k dnešnej zastávke.
- Z komína chaty stúpa dym a jazero sa jemne vlní.
- Otvorenie: na zastávke sa zapichne vlajočka a vysunie sa kartička s odmenou.

**Odmeny (8):** −10 % na víkendový pobyt · last-minute víkend · raňajky zdarma · −15 % na outdoorovú výbavu · neskorý check-out · požičanie bicykla zdarma · darček na uvítanie · **8. víkend: súťaž o víkend zdarma**
**Farby:** lúčna zelená `#7fa65a`, jazerná `#4f8fb3`, drevo `#8b5a3c`, papier `#f7f1e3`. Font: Georgia, Inter.

**Prompt:**
```
Hand-painted illustrated map of a peaceful Central European summer countryside seen from a high oblique bird's-eye view, vertical 4:5, gouache and watercolour storybook style with soft paper texture. Rolling green hills, a pine forest, meadows with wildflowers, and a winding empty footpath (no markers on it). Along the path, exactly eight clearly separated landmarks spread across the whole image: a small wooden log cabin with a stone chimney, a calm blue lake with a wooden jetty, a wooden lookout tower on a hill, a campfire circle with logs, a dense spruce forest grove, a little wooden footbridge over a stream, an old water mill, and a small white chapel. Warm late-afternoon light, gentle palette of meadow green, lake blue, warm wood brown and cream. No text, no labels, no numbers, no compass, no people.
```

---

## 5. Navyše, pre akýkoľvek e-shop: „Obálky ve tvaru výročí“
**Stav:** prerobené druhýkrát (vzhľad `obalky`). Tvar čísla 10 z obálok nefungoval, takže je to fotka z Higgsfieldu s úhľadnou mriežkou 2 × 5 rovnakých červených obálok na štipcoch (GPT Image 2.5, high, 2k, 2,75 kreditu, `img/obalky-stena.webp`). Jedna obálka = jeden rok s vami. V kóde sú len čísla, žiara dnešnej obálky so štítkom „Dnes“, kartička vysunutá z otvorenej obálky, vyblednutie zmeškanej a páska „Děkujeme za 10 let“ na konci.

**Klient (anonymne):** e-shop alebo predajňa, ktorá slávi výročie (5, 10, 15 alebo 30 rokov).
**Príležitosť:** narodeniny firmy. Univerzálny nástupca „Slavíme 30 let“.
**Dĺžka:** podľa výročia, napr. 15 dní na 15 rokov.

**Nápad podľa moodboardu:** papierové obálky rôznych veľkostí pripnuté na stene tak, že **spolu tvoria číslo výročia**. Väčšia obálka znamená väčšiu odmenu.
**Prečo hybrid:** obrázok s presne N obálkami v tvare čísla model spoľahlivo nevykreslí. Higgsfield preto robí **len stenu a interiér**. Obálky kreslí kód (CSS/SVG s papierovou textúrou a tieňom), takže tvar čísla, počet aj farba sú presné pre každého klienta.
**Ako to otvorí:** chlopňa obálky sa odklopí (3D rotácia) a vysunie sa kartička s odmenou, ako na veniec-moodboarde.

**Farby:** jedna značková farba klienta (demo: koralová `#f2705f`) na bielej stene. Font: Inter 800.

**Prompt (len pozadie):**
```
Bright Scandinavian interior, straight-on view of a large empty white-painted wooden plank wall taking up the upper two thirds of the frame, completely empty with no decorations, frames or text. In the lower part: a light oak floor, on the right a mid-century wooden chair with a woven seat holding a grey patterned cushion and two small wrapped gifts in kraft paper and coral ribbon; on the left a large woven seagrass basket filled with kraft-paper wrapped gifts and paper rolls. Soft diffused daylight from the left, calm minimal styling, editorial interior photography, vertical 4:5, no people, no text, no logos.
```

---

## 6. Prémiový nábytok (typ Konsepti): „Archiv v barvách“
**Stav:** prerobené (vzhľad `vzorky`), anonymne. Prvá verzia s kreslenou pohovkou a vejárom bola slabá.
**Myšlienka:** 8 dní pred výpredajom „pokladů ze showroomu a skladu“ je showroom čiernobiely. Každý odkrytý deň vráti farbu jednému vankúšu na pohovke a jeho látka (vzorka s cikcakovým okrajom, No. 01–08, talianske názvy) otvorí dárok. Zmeškaný vankúš ostane sivý. Ôsmy deň sa celý showroom rozfarbí a objaví sa petrolejový štítok „24.–26. 9.“.
**Médium:** fotka showroomu z Higgsfieldu (GPT Image 2.5, high, 2k, 2,75 kreditu, prvý pokus, `img/showroom.webp`). Sivá je CSS filter; farba je tá istá fotka orezaná presne na vankúš, takže všetko sedí. Farby vzoriek sú odčítané priamo z fotky.

## Hlavička landing page (krok 4, len na porovnanie s moodboardom 01)
Stromček v hlavičke nahradí **animovaný kalendár v kóde** v štýle bento videa:
- dlaždice rôznych tvarov (vstupenka, visačka, darček, kruh) s číslami dní,
- v slučke sa postupne otvárajú,
- z dlaždíc sa vysúvajú štítky odmien („−20 %“, „Doprava zdarma“, „Dárek“),
- každých pár sekúnd sa zmení farebná téma, aby bolo vidno, že vzhľad je na míru.

Je to čisté SVG/CSS, bez Higgsfieldu a bez videa.

## Ďalšie nápady na produkt (nie na implementáciu teraz)
- Séria otvorených dní so „streak“ odznakom a bonusom za 5 dní v rade.
- Zmeškaný deň sa dá dobehnúť za zdieľanie.
- Veľká výhra posledný deň, pri ktorej je vidno, koľko ľudí sa zapojilo.
- QR kód na okienko pre kamennú predajňu („vyzdvihni si v obchode“).
- E-mailová alebo push pripomienka „dnes máš otvorené okienko“.
- Slot na obrázok alebo produkt klienta v karte odmeny, nielen ikona.

## Otázky na spoločnú revíziu
1. Úplne iný layout má koncept 1 (raketa, celá v kóde). Je to prvý postavený vzhľad a nastavuje latku kvality pre ostatné.
2. Je v poriadku hybrid v koncepte 5 (pozadie z Higgsfieldu, obálky v kóde)?
3. Poradie generovania: navrhujem 1 → 4 → 2 → 3 → 5.

## Prepínač vzhľadov
Pás malých náhľadov (60×75 px, `img/nahledy/*.webp` 240×300) vľavo hore vedľa prepínača Zobrazení, ako galéria vo Fancyboxe. Dve sady: **Vánoce a advent** a **Kdykoli během roku**. Pod pásom je hlavička vybraného vzhľadu: kategória, názov, typ klienta a dĺžka, štítok „Skutečná kampaň“. Červená bodka a štítok „Nový návrh“ sú interné a pred publikáciou sa odstránia (`.vz-new`, `.vz-cap-s.new`). Náhľady sa robia screenshotom `#demo-stage > *` cez Playwright a orezom na 4:5.
