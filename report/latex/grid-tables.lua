-- Grid tables: a rule between every row and every column, no hyphenation in
-- the cells, and a little vertical padding inside the lines.
--
-- Pandoc writes each table as a booktabs longtable (\toprule, \midrule,
-- \bottomrule, no vertical rules). This filter lets pandoc write the table as
-- usual, then rewrites that LaTeX: vertical rules in the column spec, \hline
-- after every row, and the cells set ragged-right with hyphenation off, so a
-- word that does not fit moves whole to the next line instead of breaking.
--
-- Every table is styled. Per-table settings are keyed by the start of the
-- caption: pandoc-crossref has already moved the table id into the caption,
-- so the caption text is what identifies a table here.

-- Column widths (fractions of the line) for tables whose markdown dash counts
-- give a poor split.
local WIDTHS = {
  ['Comparison of existing solutions'] = {0.33, 0.09, 0.12, 0.10, 0.11, 0.12, 0.10},
}

-- Columns shaded light grey, by position: the project's own column in the
-- comparison, so it stands out from the existing solutions.
local HIGHLIGHT = {
  ['Comparison of existing solutions'] = {[7] = true},
}

local function caption_key(t, settings)
  local text = pandoc.utils.stringify(t.caption.long or {})
  for prefix in pairs(settings) do
    if text:sub(1, #prefix) == prefix then return prefix end
  end
end

-- The header row in bold: done on the table itself, so it holds whether
-- pandoc writes a header cell plain or inside a minipage.
local function bold_header(t)
  for _, row in ipairs(t.head.rows) do
    for _, cell in ipairs(row.cells) do
      for _, block in ipairs(cell.contents) do
        if block.t == 'Plain' or block.t == 'Para' then
          block.content = {pandoc.Strong(block.content)}
        end
      end
    end
  end
end

-- ── Column widths from the content ─────────────────────────────────────────
-- Pandoc sizes p-columns from the dashes of the markdown separator line, which
-- knows nothing of the content: a column of "Sprint 1" cells or a header such
-- as "Throughput" ends up narrower than its own words. Widths are computed here
-- instead, in units of roughly one character:
--   * a column is at least as wide as its longest word, so no word is split;
--     a short cell ("Sprint 1", "285 req/s", "63 / 96") counts as one word;
--   * the width left over goes to the columns with the most text.

local SHORT = 14          -- a cell up to this long is kept on one line ("09/02 – 20/02")
local CODE = 1.3          -- a monospace character, against a serif one
local BOLD = 1.1

-- Width of a run of inlines, and of its longest unbreakable piece.
local function measure(inlines, weight)
  local total, longest, word = 0, 0, 0
  local function add(n, breakable_after)
    total = total + n; word = word + n
    if breakable_after then longest = math.max(longest, word); word = 0 end
  end
  local function walk(list, w)
    for _, el in ipairs(list) do
      if el.t == 'Str' then add(utf8.len(el.text) * w, false)
      elseif el.t == 'Space' or el.t == 'SoftBreak' or el.t == 'LineBreak' then
        longest = math.max(longest, word); word = 0; total = total + w
      elseif el.t == 'Code' then
        -- breakable after its own separators (see break_code)
        for piece in el.text:gmatch('[^%-/_%.]*[%-/_%.]?') do
          if #piece > 0 then add(#piece * CODE * w, true) end
        end
      elseif el.t == 'Strong' then walk(el.content, w * BOLD)
      elseif el.content then walk(el.content, w) end
    end
  end
  walk(inlines, weight or 1)
  longest = math.max(longest, word)
  return total, longest
end

local function cell_inlines(cell)
  local out = {}
  for _, block in ipairs(cell.contents) do
    if block.content then
      for _, el in ipairs(block.content) do out[#out + 1] = el end
      out[#out + 1] = pandoc.Space()
    end
  end
  return out
end

local function auto_widths(t)
  local n = #t.colspecs
  local need, want = {}, {}
  for j = 1, n do need[j], want[j] = 2, 2 end
  local function visit(rows, weight)
    for _, row in ipairs(rows) do
      for j, cell in ipairs(row.cells) do
        if j <= n then
          local total, longest = measure(cell_inlines(cell), weight)
          if total <= SHORT then longest = total end
          need[j] = math.max(need[j], longest + 1)
          want[j] = math.max(want[j], math.min(total, 70) + 1)
        end
      end
    end
  end
  visit(t.head.rows, BOLD)
  for _, body in ipairs(t.bodies) do visit(body.body, 1) end
  -- Characters a line holds at the table's size, less the cell padding.
  local room = 105 - 2.4 * n
  local sum_need, sum_want = 0, 0
  for j = 1, n do sum_need = sum_need + need[j]; sum_want = sum_want + want[j] end
  local width = {}
  if sum_want <= room then
    for j = 1, n do width[j] = want[j] end
  else
    local k = math.max(0, (room - sum_need) / math.max(1, sum_want - sum_need))
    for j = 1, n do width[j] = need[j] + (want[j] - need[j]) * k end
  end
  local sum = 0
  for j = 1, n do sum = sum + width[j] end
  for j = 1, n do t.colspecs[j] = {t.colspecs[j][1], width[j] / sum} end
end

-- Long identifiers in code may wrap after their own separators (- / _ .),
-- never inside a name and never with an added hyphen.
local function break_code(t)
  local function split(el)
    if el.t ~= 'Code' or #el.text <= SHORT then return nil end
    local out = {}
    for piece in el.text:gmatch('[^%-/_%.]*[%-/_%.]?') do
      if #piece > 0 then
        if #out > 0 then out[#out + 1] = pandoc.RawInline('latex', '\\allowbreak{}') end
        out[#out + 1] = pandoc.Code(piece)
      end
    end
    return out
  end
  return t:walk({Code = split})
end

local function uses_p_columns(t)
  for _, spec in ipairs(t.colspecs) do
    if type(spec[2]) == 'number' then return true end
  end
  return false
end

function Table(t)
  if not FORMAT:match('latex') then return nil end
  local wkey = caption_key(t, WIDTHS)
  if wkey then
    for i, w in ipairs(WIDTHS[wkey]) do
      t.colspecs[i] = {t.colspecs[i][1], w}
    end
  elseif uses_p_columns(t) then
    auto_widths(t)
  end
  t = break_code(t)
  local hkey = caption_key(t, HIGHLIGHT)
  local shade = hkey and HIGHLIGHT[hkey] or {}
  bold_header(t)

  local tex = pandoc.write(pandoc.Pandoc({t}), 'latex')

  -- Column spec: a rule before, between and after every column. Pandoc's
  -- p-columns are written as >{\centering\arraybackslash}p{(\linewidth - …)}
  -- one per line inside @{}…@{}.
  tex = tex:gsub('\\begin{longtable}%[%]{@{}(.-)@{}}', function(spec)
    local cols = {}
    for c in spec:gmatch('>%b{}p%b{}') do cols[#cols + 1] = c end
    if #cols == 0 then
      for c in spec:gmatch('[lcr]') do cols[#cols + 1] = c end
    end
    -- Ragged-right and no hyphenation in every p-column.
    for i, c in ipairs(cols) do
      cols[i] = c:gsub('\\arraybackslash}', '\\arraybackslash\\hyphenpenalty=10000\\exhyphenpenalty=10000}')
                 :gsub('\\raggedright\\arraybackslash\\hyphenpenalty', '\\raggedright\\arraybackslash\\hyphenpenalty')
    end
    -- With rules on both sides, every column is padded on both sides: the
    -- widths must leave 2 × columns × \tabcolsep, not pandoc's 2 × (columns − 1).
    local n = #cols
    for i, c in ipairs(cols) do
      cols[i] = c:gsub('%- %d+\\tabcolsep', '- ' .. (2 * n) .. '\\tabcolsep')
    end
    -- m-columns: cells centred vertically, so a ✓ sits level with a
    -- criterion that wraps onto two lines.
    for i, c in ipairs(cols) do
      cols[i] = c:gsub('}p{', '}m{')
    end
    for i, c in ipairs(cols) do
      -- The overhang stops the shading half a rule short of each side, so
      -- the vertical rules beside the column are not painted over.
      if shade[i] then
        cols[i] = '>{\\columncolor{gray!15}[\\dimexpr\\tabcolsep-0.5\\arrayrulewidth\\relax]}' .. c
      end
    end
    return '\\begin{longtable}[]{|' .. table.concat(cols, '|') .. '|}'
  end, 1)

  -- Rules: one line between every row, including under the header.
  tex = tex:gsub('\\toprule\\noalign{}', '\\hline')
           :gsub('\\midrule\\noalign{}', '\\hline')
           :gsub('\\bottomrule\\noalign{}', '')
           :gsub('\\toprule', '\\hline')
           :gsub('\\midrule', '\\hline')
           :gsub('\\bottomrule', '')
  -- Every row ends in "\\"; follow each body and header row with a rule,
  -- but not the caption line or the \endhead / \endfirsthead markers.
  tex = tex:gsub('(\\\\)(\n)', function(bs, nl) return bs .. ' \\hline' .. nl end)
  tex = tex:gsub('(\\caption.-) \\hline', '%1')
  -- Two rules in a row (a row rule followed by the old \midrule) collapse to one.
  tex = tex:gsub('\\hline%s*\\hline', '\\hline')

  -- Header cells: pandoc wraps each in a bottom-aligned minipage, which the
  -- row padding and the vertical centring do not reach. Unwrap them, so the
  -- header centres like any other row.
  tex = tex:gsub('\\begin{minipage}%[b%]{\\linewidth}\\%a+\n', '')
           :gsub('\n\\end{minipage}', '')

  -- Padding inside the cells, and the hyphenation rule for any l/c/r columns.
  return pandoc.RawBlock('latex',
    '{\\renewcommand{\\arraystretch}{1.35}\\hyphenpenalty=10000\\exhyphenpenalty=10000\n'
    .. tex .. '\n}')
end
