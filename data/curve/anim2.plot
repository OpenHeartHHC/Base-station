set key off
do for [ii=1:30000] {
	plot 'podo.data'  every ::ii::ii+500 w l ls 1 lt 3
	pause 0.01
}
