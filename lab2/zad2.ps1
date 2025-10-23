$sourceDir="."
$csvFile="testo.csv"
$logFile="testo.log"

$nfound=Get-ChildItem -Path $sourceDir -Recurse -Include *.txt, *.log |  Measure-Object
Write-Output $nfound.Count

Get-ChildItem -Path $sourceDir -Recurse -Filter "*txt" | Select-Object Name, CreationTime, Length, Attributes | Export-Csv -Path $sourceDir\$csvFile

$date=Get-Date
$date.tostring("MM-dd-yyyy ") + $nfound.Count >> $sourceDir\$logFile