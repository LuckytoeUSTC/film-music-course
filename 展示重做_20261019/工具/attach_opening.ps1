$ErrorActionPreference='Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ppt=Join-Path $root '交付\听见末代皇帝_音乐赏析.pptx'
$video=Join-Path $root '交付\媒体\00_开场_追赶离开重访.mp4'
$data=Get-Content -LiteralPath (Join-Path $root '工具\slides.json') -Raw | ConvertFrom-Json
$app=New-Object -ComObject PowerPoint.Application
$deck=$null
try {
 $deck=$app.Presentations.Open($ppt,0,0,0)
 $cover=$deck.Slides.Item(1)
 for($i=$cover.Shapes.Count;$i -ge 1;$i--) {
  $s=$cover.Shapes.Item($i)
  if($s.Type -eq 13 -or $s.Name -eq 'OPENING_VIDEO') {$s.Delete()}
 }
 foreach($s in $cover.Shapes) {
  if($s.HasTextFrame -eq -1 -and $s.TextFrame.HasText -eq -1 -and $s.TextFrame.TextRange.Text -eq '01') {$s.TextFrame.TextRange.Text=$data[0].subtitle}
 }
 $v=$cover.Shapes.AddMediaObject2($video,0,-1,149.33,0,661.34,372)
 $v.Name='OPENING_VIDEO'
 $v.AnimationSettings.PlaySettings.PlayOnEntry=0
 foreach($s in $cover.NotesPage.Shapes) {if($s.Type -eq 14 -and $s.PlaceholderFormat.Type -eq 2){$s.TextFrame.TextRange.Text=$data[0].notes}}
 $deck.Save()
 $deck.SaveAs((Join-Path $root '交付\听见末代皇帝_静态备份.pdf'),32)
 $cover.Export((Join-Path $root 'build\开场剪辑\cover.png'),'PNG',1280,720)
 Write-Output 'Cover video embedded; PDF and cover render updated'
} finally {if($null -ne $deck){$deck.Close()};$app.Quit()}
