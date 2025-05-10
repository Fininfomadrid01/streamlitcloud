# Script PowerShell para insertar todos los ítems de un JSON en DynamoDB usando AWS CLI

$json = Get-Content .\item_opciones_ejemplo_sinbom.json -Raw | ConvertFrom-Json
$i = 1
foreach ($item in $json) {
    $filename = "temp_item_$i.json"
    $jsonStr = $item | ConvertTo-Json -Compress
    # Elimina el BOM si existe
    if ($jsonStr[0] -eq 0xFEFF) { $jsonStr = $jsonStr.Substring(1) }
    [System.IO.File]::WriteAllText($filename, $jsonStr, [System.Text.Encoding]::UTF8)
    aws dynamodb put-item --table-name dev-raw-prices --item file://$filename --region us-east-1
    Remove-Item $filename
    $i++
} 