# ============================================================
# Update-reminder hook (UserPromptSubmit, global)
# ------------------------------------------------------------
# Runs on every user prompt. If the prompt contains an Aspen stream
# paste (kg/hr, Mass Flows, etc.), it injects the Korean update
# protocol (read from update_protocol.md) into Claude's context so that
# stream/evidence updates are never missed. Otherwise it stays silent.
#
# NOTE: This .ps1 is intentionally ASCII-only so PowerShell 5.1 parses
# it regardless of file encoding (no BOM needed). All Korean text lives
# in the .md, read explicitly as UTF-8.
# ============================================================

# Make stdout UTF-8 so the Korean .md prints correctly
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

# Read stdin (JSON) explicitly as UTF-8
$reader = New-Object System.IO.StreamReader([System.Console]::OpenStandardInput(), [System.Text.Encoding]::UTF8)
$raw = $reader.ReadToEnd()
$reader.Close()

# Extract the user prompt from JSON
try {
    $data = $raw | ConvertFrom-Json
    $prompt = [string]$data.prompt
} catch {
    exit 0
}

# Aspen stream-paste signals (ASCII tokens only, single alternation regex)
#  - units: kg/hr kmol/hr lb/hr
#  - flow headers: Mass Flows / Mole Flows
#  - fraction & property labels: Mass/Mole Fractions, Molar Enthalpy, Vapor Fraction, Average MW
$isStream = $prompt -match '(kg/hr|kmol/hr|lb/hr|Mass Flows|Mole Flows|Mass Fractions|Mole Fractions|Molar Enthalpy|Vapor Fraction|Average MW)'

if ($isStream) {
    $proto = Join-Path $PSScriptRoot 'update_protocol.md'
    if (Test-Path $proto) {
        Get-Content $proto -Raw -Encoding UTF8 | Write-Output
    }
}
exit 0
