-- Technology sections: a logo beside its justification.
--
-- A tool or a technological choice is written in the chapter as a fenced div
-- carrying its logo:
--
--   ::: {.tech logo="Logos/nextjs_logo.png"}
--   **Next.js 16** with **React 19**
--
--   *Alternatives:* Remix, Nuxt (Vue).
--
--   Server rendering per route...
--   :::
--
-- In the PDF each section is one row: the logo centred in the left third, the
-- text in the right two thirds (the techrow environment, latex/header.tex).
-- The row is not split across pages, so a logo never sits alone at the foot of
-- a page. In the DOCX the logo is simply set above its text.

function Div(div)
  if not div.classes:includes('tech') then return nil end
  local logo = div.attributes['logo']
  if not logo then return nil end

  if FORMAT:match('latex') then
    -- The logo stays a pandoc Image rather than a raw \includegraphics, so
    -- pandoc finds it on the resource path and copies it into the directory
    -- LaTeX runs in, as it does for every other image. The box is the same for
    -- every logo (62% of the column, 1.35 cm high) and keepaspectratio fits
    -- wide wordmarks and square marks alike inside it.
    local img = pandoc.Image({}, logo, '',
      pandoc.Attr('', {}, { { 'width', '62%' }, { 'height', '1.35cm' } }))
    local blocks = {
      pandoc.RawBlock('latex', '\\begin{techrow}'),
      pandoc.Para({ img }),
      pandoc.RawBlock('latex', '\\techrowtext'),
    }
    for _, b in ipairs(div.content) do table.insert(blocks, b) end
    table.insert(blocks, pandoc.RawBlock('latex', '\\end{techrow}'))
    return blocks
  end

  -- Other formats: a small logo, then the text.
  local img = pandoc.Image({}, logo, '', pandoc.Attr('', {}, { { 'width', '2.5cm' } }))
  local blocks = { pandoc.Para({ img }) }
  for _, b in ipairs(div.content) do table.insert(blocks, b) end
  return blocks
end
