import os
from bottle import route, request, static_file, run, template, get, response
import csv
from io import StringIO
import json


# Static Routes
@get("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="static/css")
# http://localhost:6968/maps/SR%20Logos/Arizona.png
@get("/maps/SR Logos/<filepath:re:.*\.png>")
def maps(filepath):
    # response.headers['Content-Type'] = 'image/svg+xml'
    return static_file(filepath, root="maps/SR Logos")

@route('/svg/<state>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

script = """
    var currentTotalCases = 0;
	var currentTotalDeaths = 0;
	var previousTotalCases = 0;
	var previousTotalDeaths = 0;
	var svg = document.getElementsByTagName('svg')[0]
	//document.getElementById('state').innerHTML = state.name + ' on';
	var listVerticalOffset = 192.5523
	var listHorizontalOffset = 76.3364
	var secondRowHorizontalOffset = 232.4479
	var transform = ''
	var totalCurr = state.dates[0].counties.pop()
	var totalPrev = state.dates[1].counties.pop()

	var currentTotalCases = parseOrZero(totalCurr.confirmed);
	var currentTotalDeaths = parseOrZero(totalCurr.dead);
	var previousTotalCases = parseOrZero(totalPrev.confirmed);
	var previousTotalDeaths = parseOrZero(totalPrev.dead);

	state.dates[0].counties.sort(function(a,b) { //sort curr confirmed
	    return b.confirmed - a.confirmed;
	});

	state.dates[1].counties.sort(function(a,b) { // sort prev confirmed
	    return b.confirmed - a.confirmed;
	});

	function parseOrZero(val){
		return val ? parseInt(val) : 0
	}

	function displayCasesList(){
		/* THIS IS FOR WHEN THE TEXT ELEMENTS BECOME TSPANS
		var tspanlist = document.querySelectorAll('tspan')
		var tarr = [];
		for(var i = tspanlist.length; i--; tarr.unshift(tspanlist[i])); // cast to list from nodearray or whatever

		var count_elements_list = tarr.filter((_, i) => {
		  return i % 2 == 0;
		});*/
		
		var count_elements_list = document.querySelectorAll('#Texts_1_ > text:not([id])')
		

		state.dates[0].counties.sort(function(a,b) {
		    return b.confirmed - a.confirmed;
		});

		for (var i = 0; i < state.dates[0].counties.length; i++) {
			count_elements_list[i].innerHTML = state.dates[0].counties[i].name + ' ' + state.dates[0].counties[i].confirmed
		}


		console.log(count_elements_list, 'cel')


		for (var i = 0; i < state.dates[0].counties.length; i++) {

	

  		//currentTotalCases = currentTotalCases + parseOrZero(state.dates[0].counties[i].confirmed)
  		//currentTotalDeaths = currentTotalDeaths + parseOrZero(state.dates[0].counties[i].dead)
  		//previousTotalCases = previousTotalCases + parseOrZero(state.dates[1].counties[i].confirmed)
  		//previousTotalDeaths = previousTotalDeaths + parseOrZero(state.dates[1].counties[i].dead)

		}
	}

	displayCasesList()


	function calculateGrowthRate(current, previous){
		growth = ((current - previous) / previous) * 100
		var val = Math.round(growth) 
		return val ? val : 0
	}
	
	document.getElementById('date').innerHTML = formatToday();
	document.getElementById('total_cases').innerHTML = currentTotalCases;
	document.getElementById('current_сases').innerHTML = currentTotalCases;
	document.getElementById('current_deaths').innerHTML = currentTotalDeaths;
	document.getElementById('current_date').innerHTML = formatToday();
	document.getElementById('previous_date').innerHTML = formatYesterday();
	document.getElementById('previous_сases').innerHTML = previousTotalCases;
	document.getElementById('previous_deaths').innerHTML = previousTotalDeaths;

	document.getElementById('death_growth_rate').innerHTML = calculateGrowthRate(currentTotalDeaths, previousTotalDeaths) + '%'
	document.getElementById('cases_growth_rate').innerHTML = calculateGrowthRate(currentTotalCases, previousTotalCases) + '%'


	function setMapNumbers(){
		for (var i = 0; i < state.dates[0].counties.length; i++){
			var splittedString = state.dates[0].counties[i].name.split(' ')
			if (splittedString.length > 1){

				//
				//
				//
				// GENERALIZE
				//
				//
				//

				var firstWord = splittedString[0]
				var secondWord = splittedString[1]
				var id = firstWord + '_' + secondWord + '_numbers'
			}
			else{
				var id = state.dates[0].counties[i].name  + '_numbers'
			}
			try {
				console.log(id, 'elid')
    			document.querySelector("[id*='" + id + "']").innerHTML = state.dates[0].counties[i].confirmed
			}
			catch (e) {}
	
		}
	}

	function uncapitalizeFirstLetter(string) {
  		return string.charAt(0).toLowerCase() + string.slice(1);
	}

	function setMapFontAndCirclesSize(){
		for (var i = 0; i < state.dates[0].counties.length; i++){
			var circleId = ''
			var textId = ''
			var fontSize = ''
			var transform = ''
			var size = ''
			var color = 'AEDBF5'

			var splittedString = state.dates[0].counties[i].name.split(' ')
			if (splittedString.length > 1){
				var firstWord = splittedString[0]
				var secondWord = splittedString[1]
				textId = firstWord + '_' + secondWord + '_numbers'
				circleId = firstWord + '_' + secondWord + '_circle'
			}
			else{
				textId = state.dates[0].counties[i].name  + '_numbers'
				circleId = state.dates[0].counties[i].name  + '_circle'
			}

			var circleElement = document.querySelector("[id*='" + circleId + "']")
			console.log(circleId)
			var cx = parseFloat(circleElement.getAttribute('cx'))
			var cy = parseFloat(circleElement.getAttribute('cy'))

			if(state.dates[0].counties[i].confirmed < 10){
				fontSize = "6px"
				var Class = "st1 st2 st5"
				var r = 7.3
				keyword = uncapitalizeFirstLetter(state.dates[0].counties[i].name).replace(' ', '')
				size = 'xsmall'
				//color = 'B0B6CE'
			}
			if(state.dates[0].counties[i].confirmed > 10 && state.dates[0].counties[i].confirmed < 100){
				fontSize = "10px"
				var Class = "st1 st2 st4"
				var r = 11.9
				keyword = uncapitalizeFirstLetter(state.dates[0].counties[i].name).replace(' ', '')
				size = 'small'
				color = 'B69BAE' // prev level
				color = 'B0B6CE'
			}
			if(state.dates[0].counties[i].confirmed > 100 && state.dates[0].counties[i].confirmed < 500){
				fontSize = "12px"
				var Class = "st1 st2 st7"
				var r = 14.7
				keyword = uncapitalizeFirstLetter(state.dates[0].counties[i].name).replace(' ', '')
				size = 'medium'
				color = 'B8808E'
				color = 'B69BAE'
			}
			if(state.dates[0].counties[i].confirmed > 100 && state.dates[0].counties[i].confirmed < 1000){
				fontSize = "16px"
				var Class = "st1 st2 st6"
				var r = 21.4
				keyword = uncapitalizeFirstLetter(state.dates[0].counties[i].name).replace(' ', '')
				size = 'large'
				color = 'C3606B'
				color = 'B8808E'
				
			}
			if(state.dates[0].counties[i].confirmed > 1000){
				fontSize = "20px"
				var Class = "st1 st2 st3"
				var r = 35.2
				keyword = uncapitalizeFirstLetter(state.dates[0].counties[i].name).replace(' ', '')
				size = 'xlarge'
				color = 'D63B37'
				color = 'C3606B'
			}

			var countyId = state.dates[0].counties[i].name.replace(' ', '_') + '_1_'
			console.log(countyId, color, size)
			var county = document.querySelector("[id^='" + countyId + "']")
			county.setAttribute('style', 'fill: #' + color)
			
            var circles = []
            document.querySelectorAll("[id*='types' i] g").forEach(function(x){
                var circle = x.querySelector('circle')
                var radius = circle.getAttribute('r')
                var cy = circle.getAttribute('cy')
                var cx = circle.getAttribute('cx')
                var text = x.querySelector('text')
                var transform = text.getAttribute('transform')
                var tcx = transform.split(' ')[transform.split(')')[0].split(' ').length - 2]
                var tcy = transform.split(')')[0].split(' ')[transform.split(')')[0].split(' ').length - 1]
                var font_size = getComputedStyle(text).getPropertyValue('font-size')
                console.log('DAMNDANIEL', {r: parseFloat(radius), cx: (tcx - cx), cy: (tcy - cy)})
                circles.push({r: parseFloat(radius), cx: (tcx - cx), cy: (tcy - cy), fontSize: font_size})
                
            })
            console.log('circlesb', circles)
            circles = circles.sort((a, b) => (a.r > b.r) ? 1 : -1)
            console.log('circlesa', circles)
            
            var circle_sizes = {
                xsmall: circles[0],
                small:  circles[1],
                medium: circles[2],
                large:  circles[3],
                xlarge: circles[4]
            }
            
            if (state.dates[0].counties[i].confirmed > 10000 && circles.length > 5) {
                circle_sizes['xxlarge'] = circles[6]
                size = 'xxlarge'
            }

			//transform = mapCasesTextPosition[keyword][size]
			transform = "matrix(1 2.630000e-03 -2.630000e-03 1 " + (cx + circle_sizes[size].cx) + " " + (cy + circle_sizes[size].cy) + ")"
			//console.log('TRANSFORM', transform)
			console.log(textId)
			console.log(circleId)
			document.querySelector("[id^='" + textId + "']").setAttribute('transform', transform)
			console.log('tr')
			document.querySelector("[id^='" + textId + "']").setAttribute('style', 'font-size:' + circle_sizes[size].fontSize + ';')
			circleElement.setAttribute('r', circle_sizes[size].r)
		}
	}

	

	setMapNumbers()
	setMapFontAndCirclesSize()

	function formatToday(){
		var months = {
			0 : 'January',
			1 : 'February',
			2 : 'March',
			3 : 'April',
			4 : 'May',
			5 : 'June',
			6 : 'Jule',
			7 : 'August',
			8 : 'September',
			9 : 'October',
			10 : 'November',
			11 : 'December'
		}
		date = new Date()
		return months[date.getMonth()] + ' ' + date.getDate() + ', ' + date.getFullYear()

	}

	function formatYesterday(){
		var months = {
			0 : 'January',
			1 : 'February',
			2 : 'March',
			3 : 'April',
			4 : 'May',
			5 : 'June',
			6 : 'Jule',
			7 : 'August',
			8 : 'September',
			9 : 'October',
			10 : 'November',
			11 : 'December'
		}
		date = new Date()
		return months[date.getMonth()] + ' ' + (date.getDate() - 1) + ', ' + date.getFullYear()

	}
	]]>
	</script>"""

@route('/')
def root():
    return template("""<form action="/upload" method="post" enctype="multipart/form-data">
  Output File Name:      <input type="text" name="filename" />
  Previous Date: <input type="file" name="prev-date" />
  Current Date: <input type="file" name="curr-date" />
  <input type="submit" value="Start upload" />
</form>""")


def get_json_from_file(file):
    f = StringIO(file)
    reader = csv.DictReader(f)

    # result = [row for row in reader]
    output_json = []
    for row in reader:
        output_json.append({
            'name': row['County'],
            'dead': row['Deaths'],
            'confirmed': row['Cases']
        })
    return output_json

def create_full_json_object(prevfile, currfile, state):
    prev_date = get_json_from_file(prevfile)
    curr_date = get_json_from_file(currfile)
    return {
        'name': state,
        'dates': [{
            'date': 'today',
            'counties': curr_date
        },{
            'date': 'yesterday',
            'counties': prev_date
        }]
    }

@route('/upload', method='POST')
def do_upload():
    filename = request.forms.get('filename')
    state = request.files.get('prev-date').filename.split('-')[0]
    prev_date = request.files.get('prev-date').file.read().decode("utf-8")
    curr_date = request.files.get('curr-date').file.read().decode("utf-8")

    svg_string = ''
    fj = create_full_json_object(prev_date, curr_date, state)
    sdasjs = json.dumps(fj)

    with open(f'1-20/{state} Coronavirus cases.svg', 'r') as state_svg:
        svg_string = state_svg.read()
        # response.headers['Content-Type'] = 'image/svg+xml'
        script_prefix = """
        <script type="text/javascript">
            <![CDATA[
        var state = """
        # remove last closing tag to insert data
        svg_string = svg_string.split('</svg>')[0]
        # add data
        svg_string += script_prefix + json.dumps(fj) + script
        # close svg again
        svg_string += '</svg>'
        pablo_script = "<script>Pablo(document.querySelector('body > svg')).download('png', '" + filename + '.png' + """', function (result) {
            console.log((result.error ? 'Fail' : 'Success'));
        });</script>"""
        return '<html><body>' + svg_string + '</body><script src="http://pablojs.com/downloads/pablo.js"></script>' + pablo_script + '</html>'



    print(json.dumps(fj))

    name, ext = os.path.splitext(prev_date.filename)
    if ext not in ('.csv'):
        return "[Previous Date] File extension not allowed."
    name, ext = os.path.splitext(curr_date.filename)
    if ext not in ('.csv'):
        return "[Current Date] File extension not allowed."



    save_path = "/tmp/{category}".format(category=category)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path)
    return "File successfully saved to '{0}'.".format(save_path)

if __name__ == '__main__':
    run(host='localhost', port=6968)
run(host='localhost', port=6968)
