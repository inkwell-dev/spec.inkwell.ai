-- A3 fold-out pages for the figures too large to read on A4.
--
-- A figure whose image carries the class .foldout is set on a page of its own,
-- A3 landscape (420 × 297 mm), which is folded once into the A4 report. Its
-- height equals an A4 page's, so the text area keeps its height and only grows
-- in width. The page is placed after the current one (\afterpage), so the
-- text before the figure still fills its page.
--
-- With .sideways the figure is also turned a quarter: for a tall, narrow
-- figure, which then uses the long side of the sheet.
--
-- With .here the fold-out is placed exactly where it is written instead of
-- after the current page. Two fold-outs close together need it: the second
-- one's \afterpage would otherwise attach to the same page break as the
-- first, and both sheets would come out before the text between them (the
-- global class diagram used to precede its own section heading this way).
--
-- The figure itself stays a pandoc Figure, so its image goes through pandoc's
-- usual conversion (an SVG is turned into PDF); only the page around it is
-- raw LaTeX.
local function classes(fig)
  local foldout, sideways, here = false, false, false
  fig:walk({ Image = function(img)
    for _, c in ipairs(img.classes) do
      if c == 'foldout' then foldout = true end
      if c == 'sideways' then sideways = true end
      if c == 'here' then here = true end
    end
  end })
  return foldout, sideways, here
end

function Figure(fig)
  if not FORMAT:match('latex') then return nil end
  local foldout, sideways, here = classes(fig)
  if not foldout then return nil end
  -- The figure is centred vertically on its sheet: a figure smaller than the
  -- sheet would otherwise sit at the top, which on a sideways page reads as a
  -- figure pushed against one side once the page is turned.
  local open = '\\foldoutbegin' .. (sideways and '\\foldoutsideways' or '') .. '\\vspace*{\\fill}'
  local close = '\\vspace*{\\fill}\\foldoutend'
  if here then
    return { pandoc.RawBlock('latex', open), fig, pandoc.RawBlock('latex', close) }
  end
  return {
    pandoc.RawBlock('latex', '\\afterpage{' .. open),
    fig,
    pandoc.RawBlock('latex', close .. '}'),
  }
end
