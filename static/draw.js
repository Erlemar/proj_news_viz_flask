function change_plot_type() {
    var plot_type_id = document.getElementById('plot_type');
    var plot_type = plot_type_id.options[plot_type_id.selectedIndex].value;



	$.ajax({
		type: "POST",
		url: "/hook_type",
		data:{
			plot_type: plot_type
		}
	}).done(function(response) {
		// console.log(JSON.parse(response), JSON.parse(response)['found_count']);
		if (1 != 1) {
		    // no result
		    console.log('1111111');
		} else {

//		    var topics_dict = JSON.parse(response)['topics_dict'];
//            var select = document.getElementById("topic");
//            $("#topic").empty();
//            select.options[select.options.length] = new Option('All', 'All');
//            for(index in topics_dict) {
//                select.options[select.options.length] = new Option(topics_dict[index], index);
//            }

            var ch = JSON.parse(JSON.parse(response)['chart']);

            vegaEmbed('#bar', ch);

//            var tbl = document.getElementById('table');
//	        tbl.remove();
//            tableCreate(JSON.parse(response)['rubric_topics']);
        };
		}
	);
}

function change_plot_add() {

    var childs_add_data = document.getElementById('add_data').children;
	var add_data_arr = [];
	Array.prototype.forEach.call(childs_add_data, function(el, i) {
        if (el.selected == true) {
            add_data_arr.push(el.value);
        }
    });

	$.ajax({
		type: "POST",
		url: "/hook_add",
		data:{
			add_data: add_data_arr
		}
	}).done(function(response) {
		// console.log(JSON.parse(response), JSON.parse(response)['found_count']);
		if (1 != 1) {
		    // no result
		    console.log('1111111');
		} else {

//		    var topics_dict = JSON.parse(response)['topics_dict'];
//            var select = document.getElementById("topic");
//            $("#topic").empty();
//            select.options[select.options.length] = new Option('All', 'All');
//            for(index in topics_dict) {
//                select.options[select.options.length] = new Option(topics_dict[index], index);
//            }

            var ch = JSON.parse(JSON.parse(response)['chart']);

            vegaEmbed('#bar', ch);

//            var tbl = document.getElementById('table');
//	        tbl.remove();
//            tableCreate(JSON.parse(response)['rubric_topics']);
        };
		}
	);
}

function change_plot_topic() {

	var childs_topic = document.getElementById('topic').children;
	var topic_arr = [];
	Array.prototype.forEach.call(childs_topic, function(el, i) {
        if (el.selected == true) {
            topic_arr.push(el.innerHTML);
        }
    });

	$.ajax({
		type: "POST",
		url: "/hook_topic",
		data:{
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

function change_plot_rubric() {

    var rubric_id = document.getElementById('rubric');
    var rubric = rubric_id.options[rubric_id.selectedIndex].value;

	$.ajax({
		type: "POST",
		url: "/hook_rubric",
		data:{
			rubric: rubric
		}
	}).done(function(response) {
		// console.log(JSON.parse(response), JSON.parse(response)['found_count']);
		if (1 != 1) {
		    // no result
		    console.log('1111111');
		} else {

            var topics_dict = JSON.parse(response)['topics_dict'];
            var select = document.getElementById("topic");
            $("#topic").empty();
            select.options[select.options.length] = new Option('All', 'All');
            for(index in topics_dict) {
                select.options[select.options.length] = new Option(topics_dict[index], index);
            }

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
		type: "get",
		url: "/initial",
		data:{
			placeholder: '0',
		},
      success: function(response) {
        // console.log(JSON.parse(response), JSON.parse(response)['found_count']);
		if (1 != 1) {
		    // no result
		    console.log('1111111');
		} else {
		    // console.log(JSON.parse(response));
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
      }},
      error: function(xhr) {
        console.log('bad')
      }

	});
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
