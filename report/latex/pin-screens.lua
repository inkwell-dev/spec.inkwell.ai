-- Screenshots stay exactly where the text describes them; diagrams float.
-- A screenshot is followed by the sentences that interpret it, so letting it
-- drift to a float page separates the two. Diagrams are introduced by number
-- and may move to the top or bottom of a nearby page.
local function is_screen(fig)
  local found = false
  fig:walk({ Image = function(img)
    if img.src:find('figures/screens/', 1, true) then found = true end
  end })
  return found
end

function Figure(fig)
  if FORMAT ~= 'latex' or not is_screen(fig) then return nil end
  return {
    pandoc.RawBlock('latex', '\\pinfigures'),
    fig,
    pandoc.RawBlock('latex', '\\floatfigures'),
  }
end
