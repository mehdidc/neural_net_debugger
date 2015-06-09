// Source : http://stackoverflow.com/questions/1051061/convert-json-array-to-an-html-table-in-jquery
$.makeTable = function (mydata) {
           return $('<table border=1>').append("<tr>" + $.map(Object.keys(mydata), function (key) {
                return "<th>" + key + "</th>";
            }).join("\n") + "</tr>").append("<tr>"+$.map(Object.keys(mydata), function (k) {return "<td>"+mydata[k]+"</td>";}).join("\n")  + "</tr>");
}


$(document).ready(function(){
    chart = new CanvasJS.Chart("chartContainer", {
              title: {
                        text: "Adding & Updating dataPoints"
               },
               axisX:{
                    title: "epoch"
                },
                axisY:{
                    title: "loss"
                },
                data: [
                {
                        type: "line",
                        dataPoints: [
                        ],
                        name: "train",
                        showInLegend: true,        

                },
                {
                        type: "line",
                        dataPoints: [
                        ],
                        name: "valid",
                        showInLegend: true,        

                }]


        });
     chart.render(); 
     });

function default_update_function(state){
    filters = state["filters"];
    state["filters"] = undefined;
    table = $.makeTable(state);
    $('#content').html(table);

    point = {y: parseFloat(state["loss_train"])};
    chart.options.data[0].dataPoints.push(point);
    if(typeof(state["loss_valid"]) != 'undefined'){
        point = {y: parseFloat(state["loss_valid"])};
        chart.options.data[1].dataPoints.push(point);
    }
    if(typeof(filters) != 'undefined'){
        $('#filters').html(filters);
    }
    chart.render();
}
