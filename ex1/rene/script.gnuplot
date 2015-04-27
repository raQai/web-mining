set terminal png large
set output "plot1_log.png"
set grid
set title "Worte-Häufigkeit"
set style fill solid border -1
set boxwidth 0.1
set key opaque
set logscale y
plot "geschwister.txt" using 1:2 with linespoint lt 1 lw 1 title "Die Geschwister", "jedermann.txt" using 1:2 with linespoint lt 1 lw 1 title "Jedermann" , "liliom.txt" using 1:2 with linespoint lt 1 lw 1 title "Liliom", "acres.txt" using 1:2 with linespoint lt 1 lw 1 title "Ten_Acres"
