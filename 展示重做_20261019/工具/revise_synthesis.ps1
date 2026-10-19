$ErrorActionPreference='Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$data=Get-Content -Raw -LiteralPath (Join-Path $root '工具\slides.json') | ConvertFrom-Json
$build=Join-Path $root 'build\合成乐修订'
$ppt=Join-Path $root '交付\听见末代皇帝_音乐赏析.pptx'
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
 $deck=$app.Presentations.Open($ppt,0,0,0)
 if ($deck.Slides.Count -ne 28 -and $deck.Slides.Count -ne 30) {throw 'Expected 28 or 30 slides'}
 if ($deck.Slides.Count -eq 28) {
  for ($i=22;$i -le 23;$i++) {
   $range=$deck.Slides.Item(9).Duplicate()
   $range.Item(1).MoveTo($i)
  }
 }
 for ($i=1;$i -le $data.Count;$i++) {
  $slide=$deck.Slides.Item($i);$d=$data[$i-1]
  $texts=@()
  foreach($shape in $slide.Shapes) {
   if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) {$texts+=,$shape}
  }
  if ($i -eq 22 -or $i -eq 23) {
   $texts[0].TextFrame.TextRange.Text=$d.title
   for ($k=0;$k -lt $d.body.Count;$k++) {$texts[$k+1].TextFrame.TextRange.Text=$d.body[$k]}
  }
  if ($i -eq 9) {for($k=0;$k -lt $d.body.Count;$k++) {$texts[$k+1].TextFrame.TextRange.Text=$d.body[$k]}}
  # Native slide footer is the last text shape.
  if ($i -ne 1) {$texts[-1].TextFrame.TextRange.Text=('{0:00}' -f $i)}
  $found=$false
  foreach($shape in $slide.NotesPage.Shapes) {
   if($shape.Type -eq 14 -and $shape.PlaceholderFormat.Type -eq 2) {
    $shape.TextFrame.TextRange.Text=$d.notes;$found=$true
   }
  }
  if(-not $found) {throw "Notes body missing on slide $i"}
 }
 $deck.SaveAs((Join-Path $build 'revised.pptx'),24)
 $deck.SaveAs((Join-Path $root '交付\听见末代皇帝_静态备份.pdf'),32)
 $render=Join-Path $build 'renders';New-Item -ItemType Directory -Force -Path $render | Out-Null
 foreach($slide in $deck.Slides) {$slide.Export((Join-Path $render ('slide-{0:00}.png' -f $slide.SlideIndex)),'PNG',1280,720)}
 Write-Output ('Saved and rendered '+$deck.Slides.Count+' slides')
} finally {if($null -ne $deck){$deck.Close()};$app.Quit()}
Copy-Item -LiteralPath (Join-Path $build 'revised.pptx') -Destination $ppt -Force
