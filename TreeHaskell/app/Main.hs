import Prelude
import Graphics.Gloss

-- Sources
-- https://www.haskelltutorials.com/guides/haskell-lists-ultimate-guide.html

width :: Int
width = 400
height :: Int
height = 600

lineLength :: Float
lineLength = 60
rule :: String
rule = "F[+F][-F[-F]F]F[+F][-F]"
axiomString :: String
axiomString = "F"

-- Recursion - Will keep calling buildLSystemString until n = 0
generateLSystem :: String -> Int -> String
generateLSystem axiom 0 = axiom
generateLSystem axiom n = generateLSystem (buildLSystemString axiom rule) (n - 1)

-- concatMap breaks string apart, then reassembles with high level function
buildLSystemString :: String -> String -> String
buildLSystemString axiomString rule = concatMap replaceChar axiomString
  where
    replaceChar 'F' = rule
    replaceChar character = [character]

-- Declare an empty stack with floats in it
type Stack = [(Float, Float, Float, Float)]

paintBranch :: String -> Float -> Float -> Float -> Float -> Float -> Float -> Stack -> Picture
-- Base case: if this string is empty, recursion finishes
paintBranch [] _ _ _ _ _ _ _ = Blank
-- Looping through the chars of axiomString and applying the things in the guards
paintBranch (character:processAxiomString) x y length angle angleFactor sizeFactor stack
-- Draw line if F encountered, then calls the next branch
  | character == 'F' = let
      x2 = x + cos angle * length
      y2 = y + sin angle * length
    in Pictures [Line [(x, y), (x2, y2)], paintBranch processAxiomString x2 y2 (length * sizeFactor) angle angleFactor sizeFactor stack]
  
  | character == '+' = let angleChange = angleFactor * (pi / 180)
                        in paintBranch processAxiomString x y length (angle + angleChange) angleFactor sizeFactor stack
  
  | character == '-' = let angleChange = angleFactor * (pi / 180)
                        in paintBranch processAxiomString x y length (angle - angleChange) angleFactor sizeFactor stack
-- Puts the received values into the stack, then moves on
  | character == '[' = paintBranch processAxiomString x y length angle angleFactor sizeFactor ((x, y, angle, length) : stack)
-- Removes all the items in the stack
  | character == ']' = case stack of
      [] -> Blank
      (xPrev, yPrev, anglePrev, lengthPrev) : remaining -> paintBranch processAxiomString xPrev yPrev lengthPrev anglePrev angleFactor sizeFactor remaining
  | otherwise = paintBranch processAxiomString x y length angle angleFactor sizeFactor stack

generateTree :: Int -> Float -> Float -> Picture
generateTree layers angle size =
    let finalAxiomString = generateLSystem axiomString layers
    in paintBranch finalAxiomString 0 (fromIntegral (-height `div` 2)) lineLength (pi / 2) angle size []

main :: IO ()
main = do
    putStrLn "Welcome to the L-System Tree Generator Program!"
    putStrLn "We'll ask you a few questions about the tree you want to generate, then we'll generate an image for you."
    putStrLn "The formula we'll be using is F = F[+F][-F[-F]F]F[+F][-F]"
    putStrLn "Enter the angle in degrees (best 20 - 45 degrees):"
    angleInput <- getLine
    putStrLn "Enter the number of layers (best 3 - 5 layers):"
    layersInput <- getLine
    putStrLn "Enter scale of lines (best 0.9):"
    sizeInput <- getLine

    let angle = read angleInput :: Float
    let layers = read layersInput :: Int
    let size = read sizeInput :: Float

    let treePicture = generateTree layers angle size
    display (InWindow "L-System Tree Generator" (width, height) (10, 10)) white treePicture
