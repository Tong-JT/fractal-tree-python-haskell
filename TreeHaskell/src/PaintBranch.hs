module PaintBranch (paintBranch) where

import Graphics.Gloss

paintBranch :: String -> Float -> Float -> Float -> Float -> Float -> Float -> Picture
paintBranch [] _ _ _ _ _ _ = Blank
paintBranch (c:cs) x y lineLength angle angleFactor sizeFactor
    | c == 'F' = let
        x2 = x + cos angle * lineLength
        y2 = y - sin angle * lineLength
        in Pictures [Line [(x, y), (x2, y2)], paintBranch cs x2 y2 (lineLength * sizeFactor) angle angleFactor sizeFactor]
    | c == '+' = paintBranch cs x y lineLength (angle + angleFactor) angleFactor sizeFactor
    | c == '-' = paintBranch cs x y lineLength (angle - angleFactor) angleFactor sizeFactor
    | c == '[' = paintBranch cs x y lineLength angle angleFactor sizeFactor
    | c == ']' = paintBranch cs x y lineLength angle angleFactor sizeFactor
    | otherwise = paintBranch cs x y lineLength angle angleFactor sizeFactor