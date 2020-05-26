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
    console.log('totalplay', totalCurr, totalPrev)
	var currentTotalCases = parseOrZero(totalCurr.confirmed);
	var currentTotalDeaths = parseOrZero(totalCurr.dead);
	var previousTotalCases = parseOrZero(totalPrev.confirmed);
	var previousTotalDeaths = parseOrZero(totalPrev.dead);
    console.log('izzi', currentTotalCases, currentTotalDeaths)

	state.dates[0].counties.sort(function(a,b) { //sort curr confirmed
	    return b.confirmed - a.confirmed;
	});

	state.dates[1].counties.sort(function(a,b) { // sort prev confirmed
	    return b.confirmed - a.confirmed;
	});

	function parseOrZero(val){
		return val ? parseInt(val.replace(/,/g, '')) : 0
	}

	function displayCasesList(){
		/* THIS IS FOR WHEN THE TEXT ELEMENTS BECOME TSPANS
		var tspanlist = document.querySelectorAll('tspan')
		var tarr = [];
		for(var i = tspanlist.length; i--; tarr.unshift(tspanlist[i])); // cast to list from nodearray or whatever

		var count_elements_list = tarr.filter((_, i) => {
		  return i % 2 == 0;
		});*/
		
		console.log(state, count_elements_list, 'stepan')
		var count_elements_list = document.querySelectorAll('[id*="texts" i] text:not([id])')
		

		state.dates[0].counties.sort(function(a,b) {
		    return b.confirmed - a.confirmed;
		});

		//for (var i = 0; i < state.dates[0].counties.length; i++) {
		//	count_elements_list[i].innerHTML = state.dates[0].counties[i].name + ' ' + state.dates[0].counties[i].confirmed + 'nb'
		//}
		
		for (var i = 0; i < count_elements_list.length; i++) {
		    if (count_elements_list[i].innerHTML.trim() == '' || count_elements_list[i].innerHTML.trim() == ' ' ) {
		        continue
		    }
		    try {
		        var text_count = state.dates[0].counties[i].name + ' ' + state.dates[0].counties[i].confirmed
		    } catch (error) {
		        var text_count = ''
		    }
		    console.log(text_count, state.dates[0].counties[i], 'DARKSOULS')
		    count_elements_list[i].innerHTML = text_count
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
	
	function numberWithCommas(x) {
	    console.log(x, x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","), 'comma')
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
	
	document.querySelector('[id*=date i]').innerHTML = formatToday();
	var total_cases = document.getElementById('total_cases')
	total_cases.innerHTML = numberWithCommas(currentTotalCases);
	var transform = total_cases.getAttribute('transform')
	var tsplit = transform.split(' ')
	var tcx = parseFloat(tsplit[transform.split(')')[0].split(' ').length - 2])-((currentTotalCases.toString().length - 3) * 10)
	// 3. if you add one, you remove 10px
	var prectx = tsplit[0] + ' ' + tsplit[1] + ' ' + tsplit[2] + ' ' + tsplit[3] + ' ' + tcx  + ' ' + tsplit[5]
    total_cases.setAttribute('transform', prectx)
	document.getElementById('current_сases').innerHTML = numberWithCommas(currentTotalCases);
	document.getElementById('current_deaths').innerHTML = numberWithCommas(currentTotalDeaths);
	document.getElementById('current_date').innerHTML = formatToday();
	document.getElementById('previous_date').innerHTML = formatYesterday();
	document.getElementById('previous_сases').innerHTML = numberWithCommas(previousTotalCases);
	document.getElementById('previous_deaths').innerHTML = numberWithCommas(previousTotalDeaths);

	document.getElementById('death_growth_rate').innerHTML = calculateGrowthRate(currentTotalDeaths, previousTotalDeaths) + '%'
	document.getElementById('cases_growth_rate').innerHTML = calculateGrowthRate(currentTotalCases, previousTotalCases) + '%'


	function setMapNumbers(){
	    document.querySelectorAll('[id*=circle i]').forEach(function(el){
	        el.setAttribute('r', 0)
	    })
	    document.querySelectorAll('[id*=number i]').forEach(function(el){
	        el.innerHTML = ''
	    })
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

				var id = splittedString.join('_') + '_number'
			}
			else{
				var id = state.dates[0].counties[i].name  + '_number'
			}
			try {
				console.log(id, 'elid')
    			document.querySelector("[id*=" + id + " i]").innerHTML = state.dates[0].counties[i].confirmed
			}
			catch (e) {}
	
		}
	}

	function uncapitalizeFirstLetter(string) {
  		return string.charAt(0).toLowerCase() + string.slice(1);
	}

	function setMapFontAndCirclesSize(){
		for (var i = 0; i < state.dates[0].counties.length; i++){
		    if (state.dates[0].counties[i].name == 'Morrow'){
		        debugger
		    }
			var circleId = ''
			var textId = ''
			var fontSize = ''
			var transform = ''
			var size = ''
			var color = 'AEDBF5'

			var splittedString = state.dates[0].counties[i].name.replace("'", '_x27_').split(' ')
			if (splittedString.length > 1){
			    textId = splittedString.join('_') + '_number'
				circleId = splittedString.join('_') + '_circle'
			}
			else{
				textId = state.dates[0].counties[i].name.replace("'", '_x27_')  + '_number'
				circleId = state.dates[0].counties[i].name.replace("'", '_x27_')  + '_circle'
			}

			var circleElement = document.querySelector("[id*=" + circleId + " i]")
			console.log(circleId)
			var stconfirmed = parseInt(state.dates[0].counties[i].confirmed.replace(/,/g, ''), 10)

			if(stconfirmed < 10){
				fontSize = "6px"
				var Class = "st1 st2 st5"
				var r = 7.3
				keyword = uncapitalizeFirstLetter(state.dates[0].counties[i].name).replace(' ', '')
				size = 'xsmall'
				//color = 'B0B6CE'
			}
			if(stconfirmed >= 10 && stconfirmed < 100){
				fontSize = "10px"
				var Class = "st1 st2 st4"
				var r = 11.9
				keyword = uncapitalizeFirstLetter(state.dates[0].counties[i].name).replace(' ', '')
				size = 'small'
				color = 'B69BAE' // prev level
				color = 'B0B6CE'
			}
			if(stconfirmed >= 100 && stconfirmed < 1000){
				fontSize = "12px"
				var Class = "st1 st2 st7"
				var r = 14.7
				keyword = uncapitalizeFirstLetter(state.dates[0].counties[i].name).replace(' ', '')
				size = 'medium'
				color = 'B8808E'
				color = 'B69BAE'
			}
			if(stconfirmed >= 1000 && stconfirmed < 10000){
				fontSize = "16px"
				var Class = "st1 st2 st6"
				var r = 21.4
				keyword = uncapitalizeFirstLetter(state.dates[0].counties[i].name).replace(' ', '')
				size = 'large'
				color = 'C3606B'
				color = 'B8808E'
				
			}
			if(stconfirmed >= 10000){
				fontSize = "20px"
				var Class = "st1 st2 st3"
				var r = 35.2
				keyword = uncapitalizeFirstLetter(state.dates[0].counties[i].name).replace(' ', '').replace("'", '_x27_')
				size = 'xlarge'
				color = 'D63B37'
				color = 'C3606B'
			}

			//var countyId = state.dates[0].counties[i].name.replace(' ', '_').replace("'", '_x27_') + '_1_'
			var countyId = state.dates[0].counties[i].name.replace(/ /g, '_').replace("'", '_x27_')
			console.log(countyId, color, size, state.dates[0].counties[i].name)
			var county = document.querySelector("[id*=" + countyId + " i]")
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
            
            if (state.dates[0].counties[i].confirmed >= 100000 && circles.length > 5) {
                circle_sizes['xxlarge'] = circles[6]
                size = 'xxlarge'
            }
            
            console.log(circleElement, circleId, circle_sizes, 'dajsdas', stconfirmed > 1000, size, stconfirmed, state.dates[0].counties[i].confirmed, state.dates[0].counties[i])

			//transform = mapCasesTextPosition[keyword][size]
			
			var cx = parseFloat(circleElement.getAttribute('cx'))
			var cy = parseFloat(circleElement.getAttribute('cy'))
			
			var original_transform = document.querySelector("[id*=" + textId + " i]").getAttribute('transform')
			var otsplit = original_transform.split(' ')
			transform = otsplit[0] + ' ' + otsplit[1] + ' ' + otsplit[2] + ' ' + otsplit[3] + ' ' + (cx + circle_sizes[size].cx) + ' ' + (cy + circle_sizes[size].cy) + ')'
			//transform = "matrix(1 2.630000e-03 -2.630000e-03 1 " + (cx + circle_sizes[size].cx) + " " + (cy + circle_sizes[size].cy) + ")"
			console.log('TRANSFORM', transform)
			console.log(textId)
			console.log(circleId)
			document.querySelector("[id*=" + textId + " i]").setAttribute('transform', transform)
			console.log('tr')
			document.querySelector("[id*=" + textId + " i]").setAttribute('style', 'font-size:' + circle_sizes[size].fontSize + ';')
			circleElement.setAttribute('r', circle_sizes[size].r)
		}
	}

	

	setMapNumbers()
	setMapFontAndCirclesSize()
	
	function nth(d) {
      if (d > 3 && d < 21) return 'th';
      switch (d % 10) {
        case 1:  return "st";
        case 2:  return "nd";
        case 3:  return "rd";
        default: return "th";
      }
    }

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
		return months[cmonth - 1] + ' ' + cday + nth(cday) + ', ' + date.getFullYear()
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
		return months[cmonth - 1] + ' ' + (cday - 1) + nth(cday) + ', ' + date.getFullYear()

	}
	console.log('ABSOLUTELY DONE')
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
    # state = request.files.get('prev-date').filename.split('-')[0].strip()
    state = ' '.join(request.files.get('prev-date').filename.split('-')[:-1])
    prev_date = request.files.get('prev-date').file.read().decode("utf-8").replace('.','')
    curr_date = request.files.get('curr-date').file.read().decode("utf-8").replace('.','')

    cday, cmonth = request.files.get('curr-date').filename.split('-')[-1].split('.')[0].split('_')

    svg_string = ''
    fj = create_full_json_object(prev_date, curr_date, state)
    sdasjs = json.dumps(fj)

    with open(f'1-19/{state} Coronavirus cases.svg', 'r') as state_svg:
        svg_string = state_svg.read()
        # response.headers['Content-Type'] = 'image/svg+xml'
        script_prefix = f"""
        <script type="text/javascript">
            <![CDATA[
        var cday = {cday}
        var cmonth = {cmonth}
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

# if __name__ == '__main__':
#     run(host='localhost', port=8080)
run(host='0.0.0.0', port=8080)
