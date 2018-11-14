#!/usr/bin/python3

from enum import Enum

#---

def CreateCanvasChart( iName, iLabels, iData, iColors ):
	return '<div>\
<canvas id="' + iName + '" width="400" height="50"></canvas>\
<script>\
var ctx = document.getElementById("' + iName + '");\
var myChart = new Chart(ctx, {\
	type: \'bar\',\
	data: {\
		labels: ["' + '", "'.join( iLabels ) + '"],\
		datasets: [{\
			label: \'# of Dividends\',\
			data: [' + ', '.join( iData ) + '],\
			backgroundColor: [\
			"' + '", "'.join( iColors ) + '"\
			],\
			borderColor: [\
			],\
			borderWidth: 3\
		}]\
	},\
	options: {\
		scales: {\
			yAxes: [{\
				ticks: {\
					beginAtZero:true\
				}\
			}]\
		}\
	}\
});\
</script>\
</div>'

class eType( Enum ):
	kNone = 0
	kDividend = 1
	kSplit = 2
	kActionOnly = 3		# add Exceptionel (BIC) ?
	
class cDividend:
	def __init__( self ):
		self.mType = eType.kNone
		self.mYear = 0
		self.mPrice = 0

