# 5. Joanna joins as an app Tester

Goal: Joanna can message the Zerknij Page and gets replies, while the app stays in Development mode. In Development mode only people with a role on the app (Admin, Developer, Tester) get through; everyone else is ignored.

Needs guide [4](04-meta-app-and-webhook.md). Issue: [0003](../issues/0003-capture-drops-probe-features-findings.md).

## 5.1 Grzegorz: send the invite

1. App dashboard → **App roles** → **Roles** → **Add People** (or **Add Testers**).
2. Role: **Tester**.
3. Find Joanna by her Facebook name. If search doesn't find her, use her Facebook profile username or numeric ID: on her profile, the part after `facebook.com/` in the address.
4. **Add**. She is listed as *Pending* until she accepts.
5. Send her the Page's Messenger link in case search doesn't find the Page: Page → **Settings** → the Page username, then `https://m.me/<username>`.

## 5.2 Joanna: przyjęcie zaproszenia

Instrukcja dla Joanny, krok po kroku. Wystarczy zwykłe konto na Facebooku, nic nie trzeba instalować. Najwygodniej na komputerze, w przeglądarce.

1. Zaloguj się na Facebooka jak zwykle.
2. Wejdź na <https://developers.facebook.com>.
3. Kliknij **Rozpocznij** / **Get Started** (prawy górny róg).
   - Zaakceptuj warunki (*Platform Terms*).
   - Potwierdź numer telefonu lub e-mail, jeśli Facebook poprosi (przyjdzie kod SMS-em lub mailem).
   - Na pytanie o rolę wybierz cokolwiek, np. *Inne* / *Other*.
   - To tylko konto „deweloperskie” przypięte do Twojego Facebooka: nic nie publikuje i nikt go nie widzi.
4. Wejdź na <https://developers.facebook.com/requests>.
5. Przy zaproszeniu do aplikacji **Zerknij dev** kliknij **Akceptuj** / **Confirm**.
6. Gotowe. Otwórz Messengera, wyszukaj **Zerknij** (albo otwórz link `m.me/…`, który podeśle Ci Grzegorz) i napisz `test`. Po kilku sekundach przyjdzie odpowiedź: *Dzięki, mam to! 👀 …*

Jeśli na stronie z kroku 4 nie ma zaproszenia: odczekaj chwilę, odśwież stronę albo daj znać Grzegorzowi, żeby sprawdził, czy wysłał je na właściwe konto.

## 5.3 Grzegorz: check

- App dashboard → **App roles** → **Roles**: Joanna is listed as Tester, no longer *Pending*.
- On the VPS:
  ```bash
  docker compose exec webhook python summarize.py | tail -20
  ```
  A new `Sender 2` appears after her `test` message.
- Look up her PSID (Messenger ID for this Page): it's the `sender.id` of her message in the raw log:
  ```bash
  docker compose exec webhook tail -n 5 /data/payloads.jsonl | jq -r '.raw | fromjson | .entry[].messaging[] | "\(.sender.id)  \(.message.text // "")"'
  ```
  Store both PSIDs (yours from guide 4, hers) outside the repo, e.g. in a password manager, labelled "Grzegorz" and "Joanna". Issue 0004's allowlist needs them. Never commit them.

✅ Done when Joanna gets the acknowledgement reply. Next: [6. Capture real Drops and try the probes](06-capture-and-probes.md).
