# 1. 读取 .env 文件
$envFilePath = ".\.env"

if (Test-Path $envFilePath) {
    Get-Content $envFilePath | ForEach-Object {
        $line = $_.Trim()
        
        # 2. 忽略空行和以 # 开头的注释行
        if ($line -ne "" -and $line -notmatch '^\s*#') {
            
            # 3. 仅在第一个等号处分割键和值
            $parts = $line -split '=', 2
            if ($parts.Count -eq 2) {
                $name = $parts[0].Trim()
                $value = $parts[1].Trim()
                
                # 4. 去除值两端可能存在的单引号或双引号
                if ($value -match '^"(.*)"$' -or $value -match "^'(.*)'$") {
                    $value = $matches[1]
                }
                
                # 5. 注入到 PowerShell 环境变量中
                Set-Item -Path "env:\$name" -Value $value
                Write-Host "Inject: $name" -ForegroundColor Green
            }
        }
    }
} else {
    Write-Warning "No file: $envFilePath"
}