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
-- The figure itself stays a pandoc Figure, so its image goes through pandoc's
-- usual conversion (an SVG is turned into PDF); only the page around it is
-- raw LaTeX.
local function classes(fig)
  local foldout, sideways = false, false
  fig:walk({ Image = function(img)
    for _, c in ipairs(img.classes) do
      if c == 'foldout' then foldout = true end
      if c == 'sideways' then sideways = true end
    end
  end })
  return foldout, sideways
end

function Figure(fig)
  if not FORMAT:match('latex') then return nil end
  local foldout, sideways = classes(fig)
  if not foldout then return nil end
  return {
    pandoc.RawBlock('latex', '\\afterpage{\\foldoutbegin' .. (sideways and '\\foldoutsideways' or '')),
    fig,
    pandoc.RawBlock('latex', '\\foldoutend}'),
  }
end
