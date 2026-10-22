# Úprava celej landing page (vetva `landing-vizual`)

Poznámka od Michala, 22. 10. 2026. Robí sa oddelene od nových vzhľadov kalendára.

## Čo chceme
- **Globálne štýly a layout:** prejsť celú stránku. Niečo zmazať, upraviť, preusporiadať alebo doplniť, prípadne vizuálne spraviť inak.
- **Logo PragueBest:** doplniť ho na stránku.
- **Preč s „AI slopom“:**
  - Odstrániť hairline/eyebrow titulky, teda `section-label` nad hlavnými nadpismi (napr. „02 - Vzhledy“, „08 - Kontakt“).
  - Hlavný nadpis má sám povedať, čo sekcia robí, a nemá odkazovať na číslo alebo názov sekcie.
- **Hlavička:** hneď musí byť jasné, že ide o kalendár. Namiesto stromčeka dať animovaný kalendár v kóde (pozri `docs/vzhledy/koncepty.md`, moodboard 01).

## Inšpirácia: givingli.com (Michalovi sa veľmi páči)
- **Hero:** veľký centrovaný popis, okolo neho rozhádzané obrázky v rôznej rotácii. U nás to budú screenshoty našich kalendárov, napríklad náhľady z `img/nahledy/` alebo väčšie výrezy scén.
- **Pod textom dve CTA:** jedna na demo ukážku (`#ukazka`), druhá na kontakt alebo ponuku.
- **Sekcie:** striedajú sa text a obrázok, je v nich jednoduchosť a krátke, jasné nadpisy a texty doplnené obrázkami.
- Navrhnúť, čo by sme do takých sekcií dali: vzhľady, ako to funguje, administrácia, výsledky a kontakt. Dnešný obsah zostáva, mení sa forma.

## Dizajn systém PragueBest (z neho vychádzať)
- **Dočasná stránka:** https://praguebest-cz-nklywilr6-praguebests-projects.vercel.app/produkty/weby
- **Lokálne repo:** `C:\_WWW\PRAGUEBEST\website` (Astro, čisté CSS custom properties, bez Tailwindu).
  - Tokeny: `src/styles/tokens/` (primitívy aj sémantické), globálne štýly v `src/styles/global.css`.
  - Popis: `docs/design-system.md`, zoznam toho, čo nerobiť: `docs/dont.md`.
  - Playground tokenov: `npm run dev` → `http://localhost:4321/tokens`.
  - Písmo Satoshi (self-hosted, `public/fonts/satoshi/`), Inter ako záloha.
- Givingli je tomuto dizajn systému veľmi podobné, takže smer sedí.

## Vianočný duch zostáva
- Stránka má aj po úprave pôsobiť vianočne a adventne, nie ako neutrálna produktová stránka.
- Ponechať padajúce prvky na pozadí (dnešný sneh, iskry) a spraviť ich prepracovanejšie. Napríklad viac vrstiev s rôznou rýchlosťou a veľkosťou, jemná paralaxa, aby to bolo bohatšie a krajšie.
- Vianočné akcenty (cezmína, stromček, darčeky, zlaté iskry) zachovať aj v novom layoute v štýle Givingli.
- Rešpektovať `prefers-reduced-motion`.

## Stav: interná verzia 2 (22. 10. 2026)

**Súbory a prepínač** (upravené 22. 10. 2026 večer)
- Nová stránka je hlavná: `index.html` na `/`. Generuje sa skriptom z pôvodnej stránky `index-old.html`, takže obsah je rovnaký.
- `noindex` má `index-old.html`. Staré odkazy na `/index-v2.html` presmeruje `vercel.json` na `/`.
- Interný prepínač „Původní / Nová“ je vypnutý (`SHOW_SWITCHER = False` v `tools/v2/build_v2.py`). Hodnota `True` ho vráti na obe stránky.

**Hlavička a navigácia**
- Lepkavá lišta zodpovedá hlavičke: logo, pilulka so sekciami a „Chci kalendář“. Po zoskrolovaní dostane rozmazané krémové pozadie, červený pásik priebehu a čiernu pilulku pri aktuálnej sekcii.
- Nadpis: „Vánoce se blíží. Letos obdarujte zákazníky adventním kalendářem. Originálně.“, kde „i své“ nahradilo „adventním kalendářem“.
- Pod nadpisom sú dve CTA a trojica výhod.
- Okolo sú 4 čisté náhľady kalendárov bez UI (`img/hero/*.webp`, 520×650). Klik na náhľad zvolí daný vzhľad v deme a zoskroluje naň.

**Rytmus sekcií podľa Givingli**
- „Co kalendář přinese“ je červený pás:
  - obrie biele „+10 %“,
  - karty s ikonami PragueBest (`img/icons/`),
  - Tip ako tri karty vedľa seba.
- Demo kalendára je na svetlom pase a dedí rám monitora z pôvodnej verzie.
- Administrácia je v rovnakom monitore ako demo (rovnaké markup aj CSS ako `index-old.html`) a prefarbuje sa podľa zvoleného vzhľadu.
- „Jak to probíhá“ je červený pás so šiestimi krokmi s obrysovými číslami 01–06.
- „Proč ne krabicová služba“ je porovnanie ako cenník: tlmená karta SaaS proti väčšej čiernej karte PragueBest so štítkom „Doporučujeme“ a CTA.
- Technologické okénko:
  - grafitový rám, červené okenice a klasický čierny terminál,
  - zmienky o okénku č. 25 sú preč.
- „Aplikace na míru“ má ikony PragueBest.
- Kontakt „Další krok“ je čierny pás s červeným akcentom a červeným tlačidlom.
- Pätička: „©2026 – S láskou ke klientům ♥ vytvořilo studio PragueBest“.

**Dizajn systém a vianočný duch**
- Písmo Satoshi, papier `#f2ece0`, atrament `#0a0a0a`, červená `#e30613`.
- Žiadne popisky nad nadpismi.
- Sneh je canvas v troch vrstvách, pri `prefers-reduced-motion` je vypnutý.

**Overené:** desktop 1440 a 1280 aj mobil 390, bez horizontálneho posunu. Demo funguje vo všetkých 13 vzhľadoch, konzola je bez chýb.

## Čo platí ďalej
- Obsah a význam textov ostávajú. Meníme formu, poradie a vizuál, nie posolstvo.
- Zmeny landing page sa držia oddelene od vzhľadov kalendára, aby bolo vidno, čo sa zmenilo.

**Generovanie v2**
- Skript je v repe: `tools/v2/build_v2.py` (+ `v2.css`, `logo.svg`). Spustenie: `python tools/v2/build_v2.py`.
- Git hooky v `tools/v2/hooks` (zapnuté cez `git config core.hooksPath tools/v2/hooks`):
  - `pre-commit` pregeneruje `index.html` pri každom commite, ktorý mení `index-old.html`,
  - `post-merge` ju pregeneruje a commitne po merge vetvy `nove-vzhledy`.
- Vzhľady sa robia v `index-old.html` na `nove-vzhledy`, `index.html` sa ručne neupravuje. Do v2 sa dostanú samy po merge do `landing-vizual`.
- Popisky náhľadov v hlavičke v2 sa berú z prepínača vzhľadov. Obrázky `img/hero/<id>.webp` (520×650) treba pri zmene vzhľadu pregenerovať.
