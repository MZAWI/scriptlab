param (
    $path='raport.csv'
)

$loginAttempts = Get-WinEvent -FilterHashtable @{ 
    LogName='Security'
    ID='4625'
    StartTime=(Get-Date).AddDays(-14) 
} | ForEach-Object { 

    [PSCustomObject]@{
        TimeCreated         = $_.TimeCreated
        TargetUserName      = $_.Properties[5].Value
        TargetDomainName    = $_.Properties[6].Value
        IpAddress           = $_.Properties[19].Value
        WorkstationName     = $_.Properties[13].Value
        LogonType           = $_.Properties[10].Value
        FailureReason       = $_.Properties[8].Value
        SubStatus           = $_.Properties[9].Value
    }
}

$loginAttempts | Format-Table -AutoSize
$loginAttempts | Export-Csv -Path $path -Force

$triesIP = $loginAttempts | Group-Object -Property IpAddress | Sort-Object Count -Descending

$triesIP | Select-Object `
    @{l='IpAddress'; e={$_.Values}}, `
    Count, `
    @{l='LastAccess'; e={$_.Group.timecreated[0].ToShortTimeString()}} | Format-Table



