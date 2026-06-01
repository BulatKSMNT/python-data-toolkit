"\"id\", \"created_at\", \"name\", \"has_test\", \"alternate_url\"",
(.items | to_entries[] | 
  "\"" + (.value.id | tostring) + "\", " +
  "\"" + (.value.created_at) + "\", " +
  "\"" + (.value.name) + "\", " +
  "\"" + (.value.has_test | tostring) + "\", " +
  "\"" + (.value.alternate_url) + "\"" +
  (if .key == (length - 1) then "" else "," end)
)