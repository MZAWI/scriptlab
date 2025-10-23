param(
    $dirName
)
if (!$dirName) { exit 1 }
$csvFile="created.csv"

if (! (Test-Path -Path $dirName)) {
New-Item -Path $dirName -ItemType Directory
}

foreach ($name in 1..5) {
    if (! (Test-Path -Path $dirName\$name.txt)) {
    New-Item -Path $dirName\$name.txt
    }
}

$createdFiles=Get-ChildItem -Path $dirName | Select-Object Name,FullName,Length,CreationTime,LastWriteTime
Write-Output $createdFiles
$createdFiles | Export-Csv -Path $csvFile

foreach ($file in Get-ChildItem -Path $dirName) {
    Set-ItemProperty -Path $dirName\$file -Name CreationTime -Value "01/01/2000 12:00:00"
}

$twofiles=Get-ChildItem -Path $dirName | Select-Object -First 2

foreach ($file in $twofiles) {
    $file.Attributes = $file.Attributes -bor 'Hidden'
    $file.Name + " " + $file.Attributes >> raport.txt
}