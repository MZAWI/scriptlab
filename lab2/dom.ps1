param(
    $file
)
if (!$file) { exit 1 }
if (!(Test-Path $file)) { exit 2 }

$s1 = "Recenzent"
$s2 = "sledztwo"
$s3 = "Departament"

Get-Item -Path $file -Stream *

Set-Content -Path $file -Stream $s1 -Value "Jan Kowalski", "Anna Nowak"
Set-Content -Path $file -Stream $s2 -Value "Akta 32/2025"
Set-Content -Path $file -Stream $s3 -Value "DEV"

Get-Content -Path $file -Stream $s1
Get-Content -Path $file -Stream $s2
Get-Content -Path $file -Stream $s3