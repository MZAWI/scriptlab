function Find-ProcessByName {
    param (
        $processName
    )
    $processes=Get-Process -Name $processName -ErrorAction SilentlyContinue
    $found = $processes | Select-Object Name, ID, WorkingSet64
    $found | Format-Table Name, 
        @{l="PID"; e="ID"},
        @{l="Memory (M)"; e={ [math]::Round($_.WorkingSet64 / 1MB, 2) }}

    $found | Measure-Object -Property WorkingSet64 -Average -Sum | ForEach-Object {
        [PSCustomObject]@{
        Count           = $_.Count
        'Sum (M)'       = [math]::Round($_.Sum / 1MB, 2)
        'Average (M)'   = [math]::Round($_.Average / 1MB, 2)
        }
    }
}

Find-ProcessByName('*firefox*')

