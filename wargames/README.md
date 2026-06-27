# W.O.P.R. — SHALL WE PLAY A GAME?

A single-page, mobile-friendly arcade inspired by the WOPR terminal from the 1983
film *WarGames*. Boot into a phosphor-blue CRT, dial in over a 300-baud modem, and
pick a game from Joshua's menu.

All thirteen titles from the movie's game list appear on the menu. The card and
board games respond in-character ("ACCESS RESTRICTED… select another game"), while
the seven war games are **fully playable** with touch and keyboard:

| # | Game | What you do |
|---|------|-------------|
| 08 | **Fighter Combat** | Vector dogfight — drag to fly, auto-cannon, survive escalating waves |
| 09 | **Guerrilla Engagement** | Judgment under fire — tap hostiles, spare civilians, or it's over |
| 10 | **Desert Warfare** | Artillery duel vs. WOPR — drag back to aim, fight the wind, crater the dunes |
| 11 | **Air-to-Ground Actions** | Bombing run — flatten each sector before your descent puts you into a building |
| 12 | **Theaterwide Tactical Warfare** | Three-front strategy — out-allocate WOPR's divisions and break through |
| 13 | **Theaterwide Biotoxic & Chemical** | Containment puzzle — wall off the outbreak before it reaches population centers |
| 14 | **Global Thermonuclear War** | Missile-command defense… with the only winning move it ever taught us |

## Controls

- **Mobile:** tap and drag. Every game is designed for touch in portrait.
- **Desktop:** mouse for taps/drags; arrow keys + space also fly the fighter.
- **SND** toggles the WebAudio sound (state is remembered).

No build step, no dependencies — it's one `index.html`. Open it in a browser to play.

## Deployment

Pushed via the workflow in `.github/workflows/pages.yml`, which publishes the
contents of this folder to GitHub Pages. In the repo: **Settings → Pages →
Build and deployment → Source → GitHub Actions**.

*A strange game. The only winning move is not to play.*
