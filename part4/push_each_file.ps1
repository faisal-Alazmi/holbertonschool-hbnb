# Push every part4 file in its own commit
# Run from repo root: .\part4\push_each_file.ps1

Set-Location $PSScriptRoot\..

$files = @(
    "part4/styles.css",
    "part4/login.html",
    "part4/index.html",
    "part4/place.html",
    "part4/add_review.html",
    "part4/scripts.js",
    "part4/images/.gitkeep"
)

foreach ($f in $files) {
    $name = Split-Path $f -Leaf
    git add $f
    git commit -m "Add part4 $name"
}

git push
