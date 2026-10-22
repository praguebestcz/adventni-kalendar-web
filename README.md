# Adventní kalendář na míru - prezentační web

Stránka pro klienty PragueBest: proč a jak si nechat postavit adventní (nebo jiný) kalendář dárků na míru. Živě na https://adventni-kalendar.pbst.app.

## Co je v repu

* `index.html` - hlavní stránka (vzhledy kalendáře, administrace, technologické okénko, nabídka vývoje a auditu, kontakt); **generuje se**, ručně se neupravuje
* `index-old.html` - původní stránka (`noindex`) a zároveň zdroj, ze kterého se `index.html` generuje: vzhledy, demo a texty se mění tady
* `tools/v2/` - generátor `build_v2.py` (+ `v2.css`, `logo.svg`) a git hooky, které ho spouští; podrobnosti v `docs/landing-uprava.md`
* `email/index.html` - online verze e‑mailu klientům (obsah a styl podle aktuální stránky, obrázky v `img/mail-v2/`); `/email-v2` na ni přesměrovává
* `archiv/` - starší verze, které se nenasazují (vynechané v `.vercelignore`), např. `archiv/email-v1/` - původní e‑mail
* `fonts/` - self‑hosted Inter, JetBrains Mono a Satoshi (woff2)
* `img/` - ilustrace vzhledů; `img/mail-v2/` - obrázky pro e‑mail (PNG/JPG, absolutní odkazy na živou adresu), z `img/mail/` používá jen `admin.jpg`, zbytek patří archivnímu e‑mailu
* `vercel.json` - statické nasazení bez buildu, přesměrování starých adres `/index-v2.html` a `/email-v2` na `/` a `/email/`

Stránka je čisté HTML/CSS/JS, bez buildu a bez závislostí. Otevře se dvojklikem na `index.html`.

Po úpravě `index-old.html` je potřeba přegenerovat `index.html`:

```bash
python3 tools/v2/build_v2.py
```

Automaticky to dělají hooky, stačí je jednou zapnout: `git config core.hooksPath tools/v2/hooks`.

## Nasazení

Vercel projekt `adventni-kalendar-na-miru` (tým PragueBest). Repo zatím není napojené na Git integraci Vercelu, nasazuje se ručně z `main`: `npx vercel --prod`.

## Související

* Samotná aplikace kalendáře (Next.js, databáze, recept): repo `praguebestcz/calendars`
* Text e‑mailu k vložení do pošty: `spec-workspace` → `projects/mastershop/outputs/ai-first-aplikace/email-klientum.md`
