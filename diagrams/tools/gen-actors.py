#!/usr/bin/env python3
"""Draw the actors of the system as an infographic (.drawio).

  python3 diagrams/tools/gen-actors.py
  make one F=fig-1-13-actors

It replaces the report's table of actors. The table listed five rows; the
figure also shows how they relate, which the table could only say in prose:

  * the top row is the generalisation chain, Visitor → Reader → Writer, each
    arrow naming what the next actor adds;
  * the second row holds the two actors that specialise nobody, each tagged
    with the reason it stands apart;
  * the strip at the bottom lists the account states that are not actors.

The drawing helpers and the colours are those of the architecture figures
(gen-architecture.py), so the infographic matches them on the page.
"""
import importlib.util
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('arch', HERE / 'gen-architecture.py')
arch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arch)
Figure, FONT = arch.Figure, arch.FONT
BLUE, GREEN, PURPLE, GREY, YELLOW = arch.BLUE, arch.GREEN, arch.PURPLE, arch.GREY, arch.YELLOW
ORANGE = ('#ffe6cc', '#d79b00')


def card(f: Figure, x, y, w, h, code, name, account, items, colour):
    """One actor: a coloured header with its code and name, the account that
    represents it, then what it does, one item per line."""
    fill, stroke = colour
    # The card body: white, framed in the actor's colour.
    body = f._id()
    # An item starting with '~' continues the previous one: it is indented
    # under the text of that item instead of carrying a bullet of its own.
    lines = [('&nbsp;&nbsp;&nbsp;' + escape(i[1:])) if i.startswith('~') else ('•&nbsp;' + escape(i))
             for i in items]
    html = f'<i>{escape(account)}</i><br><br>' + '<br>'.join(lines)
    style = (f'rounded=1;arcSize=5;whiteSpace=wrap;html=1;align=left;verticalAlign=top;'
             f'spacing=12;spacingTop=58;fillColor=#ffffff;strokeColor={stroke};strokeWidth=2;'
             f'fontSize=15;{FONT}')
    f.cells.append(f._vertex(body, html, style, x, y, w, h))
    # The header band, drawn over the top of the card.
    head = f._id()
    style = (f'rounded=1;arcSize=12;whiteSpace=wrap;html=1;align=left;verticalAlign=middle;'
             f'spacingLeft=12;fillColor={fill};strokeColor={stroke};strokeWidth=2;'
             f'fontSize=19;fontStyle=1;{FONT}')
    f.cells.append(f._vertex(head, f'{escape(code)}&nbsp;&nbsp;{escape(name)}', style, x, y, w, 46))
    return body


def tag(f: Figure, x, y, w, text, colour):
    """A small label above a card: why this actor stands apart."""
    cid = f._id()
    style = (f'rounded=1;arcSize=50;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;'
             f'fillColor={colour[0]};strokeColor={colour[1]};fontSize=14;fontStyle=2;{FONT}')
    f.cells.append(f._vertex(cid, escape(text), style, x, y, w, 30))


def actors():
    f = Figure('fig-1-13-actors', 'Actors of the system')
    w, h, gap = 220, 225, 60
    visitor = card(f, 0, 0, w, h, 'A1', 'Visitor', 'no account',
                   ['browses the public feed', 'reads free articles', 'cannot interact'], GREY)
    reader = card(f, w + gap, 0, w, h, 'A2', 'Reader', 'personal account',
                  ['likes, comments, reposts', 'saves, follows, blocks', 'reports content',
                   'premium plan: premium', '~articles and the assistant'], BLUE)
    writer = card(f, 2 * (w + gap), 0, w, h, 'A3', 'Writer', 'personal account, role writer',
                  ['everything a reader does', 'drafts, publishes and', '~analyses own articles',
                   'once eligible: premium', '~articles and listings'], GREEN)
    # The generalisation chain: each arrow says what the next actor adds.
    # The arrows run at the height of the header bands, their labels lifted
    # above the cards, since a gap between two cards is too short to hold one.
    f.edge(visitor, reader, 'signs up', exit=(1, 0.1), entry=(0, 0.1), lift=30)
    f.edge(reader, writer, 'role writer', exit=(1, 0.1), entry=(0, 0.1), lift=30)

    y2 = h + 75
    w2 = (3 * w + 2 * gap - gap) // 2
    tag(f, 40, y2 - 40, w2 - 80, 'a different account type: inherits nothing', PURPLE)
    card(f, 0, y2, w2, 195, 'A4', 'Magazine', 'magazine account',
         ['subscribes and receives monthly credits', 'browses writers and their evaluation reports',
          'previews, buys and publishes licensed articles'], PURPLE)
    tag(f, w2 + gap + 40, y2 - 40, w2 - 80, 'a role granted in the database', ORANGE)
    card(f, w2 + gap, y2, w2, 195, 'A5', 'Administrator', 'personal account, role admin',
         ['works the report queue', 'manages users and articles',
          'grants marketplace eligibility manually', 'works in a console of its own'], ORANGE)

    # Account states: they change what an actor may do, not which actor it is.
    strip = f._id()
    html = ('<b>States, not actors</b><br>a reader’s plan (free or premium)'
            '&nbsp;&nbsp;·&nbsp;&nbsp;a writer’s marketplace eligibility'
            '&nbsp;&nbsp;·&nbsp;&nbsp;a magazine’s subscription (active or not)')
    style = (f'rounded=1;arcSize=20;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;'
             f'spacing=10;fillColor={YELLOW[0]};strokeColor={YELLOW[1]};fontSize=14;{FONT}')
    f.cells.append(f._vertex(strip, html, style, 0, y2 + 215, 3 * w + 2 * gap, 60))
    f.write()


if __name__ == '__main__':
    (arch.DIAGRAMS / 'fig-1-13-actors').mkdir(exist_ok=True)
    actors()
    print('wrote fig-1-13-actors')
