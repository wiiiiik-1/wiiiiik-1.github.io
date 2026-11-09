# Prune "stub" DSH sessions: session dirs that contain only the header plus the
# initial permission/sandbox/approval records, and zero conversation records.
#
# Dry-run by default (prints only). Add -Apply to actually delete.
#
#   pwsh -NoProfile -File .\dsh-migrate\tools\prune-stub-sessions.ps1
#   pwsh -NoProfile -File .\dsh-migrate\tools\prune-stub-sessions.ps1 -Apply
#
# Run it in a NORMAL PowerShell window: the DSH sandbox only allows writes inside
# the workspace, so it cannot touch ~\.dsh.
#
# It does three things: deletes the session dir, deletes the matching projcache
# entry, and removes the id from workspace.json sessionIds (workspace.json is
# backed up first).

[CmdletBinding()]
param(
  # Default: the workspace this script lives in (dsh-migrate\tools\ -> two levels up).
  # Kept free of non-ASCII literals so Windows PowerShell 5.1 (ANSI file reading) is safe.
  [string]$Workspace = ([IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))),
  [string]$DshHome   = (Join-Path $env:USERPROFILE '.dsh'),
  [switch]$Apply
)

$ErrorActionPreference = 'Stop'

function Get-EncodedWorkspace([string]$Path) {
  $abs = [IO.Path]::GetFullPath($Path)
  $s = $abs -replace '^([A-Za-z]):[\\/]', '$1-'
  $sb = [Text.StringBuilder]::new()
  foreach ($ch in $s.ToCharArray()) {
    if ($ch -eq '\' -or $ch -eq '/') { [void]$sb.Append('-') }
    elseif ([string]$ch -match '[A-Za-z0-9_.\-]') { [void]$sb.Append($ch) }
    else { [void]$sb.Append('~' + ([int]$ch).ToString('X4')) }
  }
  '--' + $sb.ToString() + '--'
}

$store = Join-Path (Join-Path $DshHome 'sessions') (Get-EncodedWorkspace $Workspace)
$cache = Join-Path $DshHome 'storages\session_projcache\sessions'
$wsp   = Join-Path $DshHome 'storages\workspace.json'

if (-not (Test-Path -LiteralPath $store)) { throw "session store not found: $store" }
Write-Host "store  $store"
Write-Host "ws     $Workspace"
Write-Host ("mode   " + $(if ($Apply) { 'APPLY (will delete)' } else { 'DRY-RUN (print only)' }))
Write-Host ''

# STUB verdict: header present, no conversation records, <= 6 records total.
$nodeJs = @'
const fs=require('fs'),z=require('zlib');
const M=Buffer.from([0x28,0xb5,0x2f,0xfd]);
const p=process.argv[1];
const b=fs.readFileSync(p);
const parts=[];
for(let i=b.indexOf(M);i!==-1;i=b.indexOf(M,i+1)){try{parts.push(z.zstdDecompressSync(b.subarray(i)))}catch{}}
let recs=[];
try{recs=Buffer.concat(parts).toString('utf8').split('\n').filter(x=>x.trim()).map(x=>JSON.parse(x))}catch(e){console.log('PARSE_ERR');process.exit(0)}
const dlg=recs.filter(r=>['user/message','assistant/message','turn/start','turn/end','tool/call','session/title','workspace/changes'].includes(r.type));
const ok=dlg.length===0 && recs[0] && recs[0].type==='session' && recs.length<=6;
console.log((ok?'STUB':'LIVE')+' records='+recs.length+' dialog='+dlg.length);
'@

$stubs = @()
foreach ($dir in Get-ChildItem -LiteralPath $store -Directory) {
  $file = Join-Path $dir.FullName 'session.v4.jsonl.zstd'
  if (-not (Test-Path -LiteralPath $file)) { continue }
  $verdict = (& node -e $nodeJs $file).Trim()
  $size = (Get-Item -LiteralPath $file).Length
  if ($verdict -match '^STUB') {
    $stubs += [pscustomobject]@{ Id = $dir.Name; Bytes = $size; Verdict = $verdict }
    Write-Host ("STUB    {0}  {1,8} B  {2}" -f $dir.Name, $size, $verdict)
  } else {
    Write-Host ("keep    {0}  {1,8} B  {2}" -f $dir.Name, $size, $verdict)
  }
}

if ($stubs.Count -eq 0) { Write-Host "`nno stub sessions, nothing to do."; return }
$ids = $stubs.Id
Write-Host "`nfound $($stubs.Count) stub(s)."

if (-not $Apply) { Write-Host 'dry-run only; add -Apply to delete.'; return }

foreach ($id in $ids) {
  Remove-Item -LiteralPath (Join-Path $store $id) -Recurse -Force
  $cf = Join-Path $cache "$id.json"
  if (Test-Path -LiteralPath $cf) { Remove-Item -LiteralPath $cf -Force }
  Write-Host "deleted $id"
}

if (Test-Path -LiteralPath $wsp) {
  $ts = Get-Date -Format 'yyyyMMdd-HHmmss'
  Copy-Item -LiteralPath $wsp -Destination "$wsp.bak-$ts" -Force
  $j = [IO.File]::ReadAllText($wsp, [Text.Encoding]::UTF8) | ConvertFrom-Json
  foreach ($k in $j.tables.workspaces.PSObject.Properties.Name) {
    $w = $j.tables.workspaces.$k
    $n = @($w.sessionIds).Count
    $w.sessionIds = @($w.sessionIds | Where-Object { $ids -notcontains $_ })
    if (@($w.sessionIds).Count -ne $n) { Write-Host "registry $($w.title): $n -> $(@($w.sessionIds).Count)" }
  }
  [IO.File]::WriteAllText($wsp, ($j | ConvertTo-Json -Depth 12), (New-Object Text.UTF8Encoding($false)))
  Write-Host "workspace.json updated (backup $wsp.bak-$ts)"
}

Write-Host "`nremaining sessions:"
Get-ChildItem -LiteralPath $store -Directory | ForEach-Object { '  ' + $_.Name }
