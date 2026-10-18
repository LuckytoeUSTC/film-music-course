$ErrorActionPreference = 'Stop'
$taskRoot = Join-Path $PSScriptRoot '..'
$taskRoot = (Resolve-Path -LiteralPath $taskRoot).Path
$pptPath = Join-Path $taskRoot '交付\宫门之内的奔跑_展示稿.pptx'
$pdfPath = Join-Path $taskRoot '交付\宫门之内的奔跑_静态备份.pdf'
$renderPath = Join-Path $taskRoot 'build\powerpoint_renders'
New-Item -ItemType Directory -Force -Path $renderPath | Out-Null
$pptApp = New-Object -ComObject PowerPoint.Application
$deck = $null
try {
    $deck = $pptApp.Presentations.Open($pptPath, -1, 0, 0)
    $rows = @()
    foreach ($slide in $deck.Slides) {
        $mediaCount = 0
        foreach ($shape in $slide.Shapes) { if ($shape.Type -eq 16) { $mediaCount++ } }
        $rows += [pscustomobject]@{ slide=$slide.SlideIndex; shapes=$slide.Shapes.Count; media=$mediaCount }
        $slide.Export((Join-Path $renderPath ('slide-{0:00}.png' -f $slide.SlideIndex)), 'PNG', 1920, 1080)
    }
    $deck.SaveAs($pdfPath, 32)
    $rows | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskRoot '制作记录\powerpoint_open.json') -Encoding UTF8
    Write-Output ('PowerPoint opened and rendered ' + $deck.Slides.Count + ' slides; PDF exported.')
} finally {
    if ($null -ne $deck) { $deck.Close() }
    $pptApp.Quit()
}
