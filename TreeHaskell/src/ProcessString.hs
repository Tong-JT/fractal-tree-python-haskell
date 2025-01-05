module ProcessString (buildLSystemString) where

buildLSystemString :: String -> String -> String
buildLSystemString axiomString rule = concatMap replaceChar axiomString
  where
    replaceChar 'F' = rule
    replaceChar c   = [c]
