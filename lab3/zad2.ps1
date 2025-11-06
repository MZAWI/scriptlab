param (
    $path='raport.csv'
)

# Get-WinEvent -LogName 'Application' | Where-Object { $_.LevelDisplayName -eq 'Warning' -or $_.Level -eq 'Error'}

$errors=Get-WinEvent -FilterHashtable @{ 
    LogName='Application'
    Level=2
    StartTime=(Get-Date).AddDays(-7)
}
$warnings=Get-WinEvent -FilterHashtable @{ 
    LogName='Application';
    Level=3
    StartTime=(Get-Date).AddDays(-7)
}

$summary = $errors + $warnings

$report = $summary | ForEach-Object {
    $FaultingApplicationName = ''
    if ($_.Message -match "Application[\s:]{1,2}'(.*?)'") {
        $FaultingApplicationName = $Matches[1]
    }

    [PSCustomObject]@{
        TimeCreated            = $_.TimeCreated
        SourceName             = $_.ProviderName          # Same as ProviderName
        ProviderName           = $_.ProviderName
        EventID                = $_.Id
        Level                  = $_.LevelDisplayName
        FaultingApplicationName = $FaultingApplicationName
    }
}

Write-Output $report
$report | Export-Csv -Path $path -Force
$report | Group-Object ProviderName | Select-Object Values, Count | Sort-Object -Descending
$report | Group-Object Level | Select-Object Values, Count | Sort-Object -Descending