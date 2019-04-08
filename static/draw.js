function change_plot() {
    var plot_type_id = document.getElementById('plot_type');
    var plot_type = plot_type_id.options[plot_type_id.selectedIndex].value

    var rubric_id = document.getElementById('rubric');
    var rubric = rubric_id.options[rubric_id.selectedIndex].value

	var childs_topic = document.getElementById('topic').children;
	var topic_arr = [];
	Array.prototype.forEach.call(childs_topic, function(el, i) {
        if (el.selected == true) {
            topic_arr.push(el.innerHTML);
        }
    });
	$.ajax({
		type: "POST",
		url: "/hook",
		data:{
			plot_type: plot_type,
			rubric: rubric,
			topics: topic_arr
		}
	}).done(function(response) {
		// console.log(JSON.parse(response), JSON.parse(response)['found_count']);
		if (1 != 1) {
		    // no result
		    console.log('1111111');
		} else {
            var ch = JSON.parse(JSON.parse(response)['chart']);
            vegaEmbed('#bar', ch);

            var tbl = document.getElementById('table');
	        tbl.remove();
            tableCreate(JSON.parse(response)['rubric_topics']);
        };
		}
	);
}

function get_data() {

    $.ajax({
		type: "POST",
		url: "/initial",
		data:{
			placeholder: '0',
		}
	}).done(function(response) {
		// console.log(JSON.parse(response), JSON.parse(response)['found_count']);
		if (1 != 1) {
		    // no result
		    console.log('1111111');
		} else {
		    console.log(JSON.parse(response));
            var rubrics_dict = JSON.parse(response)['rubrics_dict'];
            var select = document.getElementById("rubric");
            for(index in rubrics_dict) {
                select.options[select.options.length] = new Option(rubrics_dict[index], index);
            }

            var topics_dict = JSON.parse(response)['topics_dict'];
            var select = document.getElementById("topic");

            for(index in topics_dict) {
                select.options[select.options.length] = new Option(topics_dict[index], index);
            }

            var ch = JSON.parse(JSON.parse(response)['chart']);
            vegaEmbed('#bar', ch);
            // console.log(JSON.parse(response)['rubric_topics']);
            tableCreate(JSON.parse(response)['rubric_topics']);
        };
		}
	);
}

function tableCreate(table_data) {

    var body = document.getElementsByTagName('body')[0];
    var tbl = document.createElement('table');
    // tbl.style.width = '100%';
    tbl.setAttribute('border', '1');
    tbl.setAttribute('id', 'table');
    var tbdy = document.createElement('tbody');

    var thead = document.createElement('thead');
    var thr = document.createElement('tr');

    Object.keys(table_data).forEach(i => {
        var th = document.createElement('th');
        th.appendChild(document.createTextNode(i));
        thr.appendChild(th);

    })

    thead.appendChild(thr);
    tbl.appendChild(thead);

//    Object.keys(table_data).forEach(i => {
//        var tr = document.createElement('tr');
//        for (var j = 0; j < table_data[i].length; j++) {
//            var td = document.createElement('td');
//            td.appendChild(document.createTextNode(table_data[i][j]))
//            tr.appendChild(td)
//        }
//        tbdy.appendChild(tr);
//    })
//
    for (var j = 0; j < 20; j++) {
        var tr = document.createElement('tr');
        Object.keys(table_data).forEach(i => {
            var td = document.createElement('td');
            td.appendChild(document.createTextNode(table_data[i][j]))
            tr.appendChild(td)
        })
        tbdy.appendChild(tr);
    }
    tbdy.appendChild(tr);



    tbl.appendChild(tbdy);
  body.appendChild(tbl)

}

get_data();
