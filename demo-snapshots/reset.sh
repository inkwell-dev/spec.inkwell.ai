#!/bin/sh
# Puts the demo database back to the "ready to record" state between takes:
# the magazine's credits, Keeping One Fish unsold, Nadia's draft untouched,
# her AI tokens at 20,000 and her style profile in place.
#
#   ./reset.sh
#
# Close the editor and marketplace tabs first, then reload them after: an open
# editor would autosave its old content over the restored draft.
set -eu
cd "$(dirname "$0")"

# The API and worker hold connections and would write mid-restore; stop them.
docker stop inkwell-api-1 inkwell-worker-1 >/dev/null

# Replace every table with the snapshot, in one transaction.
docker exec -i inkwell-db-1 pg_restore -U inkwell -d inkwell --clean --if-exists \
  --single-transaction < ready-to-record.dump

docker start inkwell-api-1 inkwell-worker-1 >/dev/null

# Show the three numbers a take depends on.
docker exec inkwell-db-1 psql -U inkwell -d inkwell -t -A -F' | ' -c "
  SELECT 'magazine credits', credit_balance::text FROM magazine_profiles WHERE slug = 'the-longform-review'
  UNION ALL
  SELECT 'nadia tokens', ai_tokens_remaining::text FROM users WHERE email = 'nadia@example.com'
  UNION ALL
  SELECT 'keeping-one-fish purchases', count(*)::text FROM article_purchases p
    JOIN articles a ON a.id = p.article_id WHERE a.slug = 'keeping-one-fish';"
echo "reset done — reload the browser tabs"
