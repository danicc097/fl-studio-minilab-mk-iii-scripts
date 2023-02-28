$dest = $HOME + '\Documents\Image-Line\FL Studio\Settings\Hardware\Arturia MiniLab 3 - dev'
(mkdir -Force $dest) | out-null
Copy-Item ./*.py $dest
