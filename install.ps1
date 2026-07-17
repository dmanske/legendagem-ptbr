$ErrorActionPreference = "Stop"

$Repo = if ($env:TRADUTOR_REPO) { $env:TRADUTOR_REPO } else { "dmanske/tradutor-de-clipes" }
$Ref = if ($env:TRADUTOR_REF) { $env:TRADUTOR_REF } else { "main" }
$SkillName = "tradutor-de-clipes"
$CodexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$Destination = Join-Path (Join-Path $CodexRoot "skills") $SkillName
$LocalSource = if ($PSScriptRoot) { Join-Path $PSScriptRoot "skill\$SkillName" } else { $null }
$TempDirectory = $null

try {
    if ($LocalSource -and (Test-Path (Join-Path $LocalSource "SKILL.md"))) {
        $Source = $LocalSource
    }
    else {
        $TempDirectory = Join-Path ([System.IO.Path]::GetTempPath()) ("tradutor-de-clipes-" + [guid]::NewGuid())
        New-Item -ItemType Directory -Path $TempDirectory | Out-Null
        $Archive = Join-Path $TempDirectory "repository.zip"
        $Url = "https://github.com/$Repo/archive/refs/heads/$Ref.zip"
        Invoke-WebRequest -Uri $Url -OutFile $Archive
        Expand-Archive -Path $Archive -DestinationPath $TempDirectory
        $RepoName = ($Repo -split "/")[-1]
        $Source = Join-Path $TempDirectory "$RepoName-$Ref\skill\$SkillName"
    }

    if (-not (Test-Path (Join-Path $Source "SKILL.md"))) {
        throw "A skill não foi encontrada no pacote baixado."
    }

    New-Item -ItemType Directory -Force -Path (Split-Path $Destination) | Out-Null
    if (Test-Path $Destination) {
        $Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $Backup = "$Destination.backup-$Timestamp"
        Move-Item -Path $Destination -Destination $Backup
        Write-Host "Versão anterior preservada em: $Backup"
    }

    Copy-Item -Recurse -Path $Source -Destination $Destination
    Write-Host "Skill instalada em: $Destination"
    Write-Host "Reinicie o Codex e execute: py -3 `"$Destination\scripts\doctor.py`""
}
finally {
    if ($TempDirectory -and (Test-Path $TempDirectory)) {
        Remove-Item -Recurse -Force $TempDirectory
    }
}
