// Source : http://stackoverflow.com/questions/1051061/convert-json-array-to-an-html-table-in-jquery
$.makeTable = function (mydata) {
           return $('<table border=1>').append("<tr>" + $.map(Object.keys(mydata), function (key) {
                return "<th>" + key + "</th>";
            }).join("\n") + "</tr>").append("<tr>"+$.map(Object.keys(mydata), function (k) {return "<td>"+mydata[k]+"</td>";}).join("\n")  + "</tr>");
}

charts = {};

function curve_new(id, title, xlabel, ylabel, data_names){
    data = [];
    for(i in data_names){
        data.push(
            {
                    type: "line",
                    dataPoints: [
                    ],
                    name: data_names[i],
                    showInLegend: true,        

            }
        );
    };
    chart = new CanvasJS.Chart(id, {
              title: {
                        text: title
               },
               axisX:{
                    title: xlabel
                },
                axisY:{
                    title: ylabel
                },
                data: data
        });
    chart.render();
    return chart;
}

$(document).ready(function(){
 });

function default_update_function(state){
    if(state["meta"] != 'undefined'){
        meta = state["meta"];
        if(typeof(meta) != 'undefined'){
            if(typeof(meta["html"]) != 'undefined'){
                $.each(meta["html"],
                        function(v){
                            if($("#" + meta["html"][v]).length != 0) {
                                return;
                            }
                            $('#html').append("<h1>"+meta["html"][v]+
                                              "</h1><div id='" + 
                                              meta["html"][v] + 
                                              "'></div>");
                        }
                );
            }
            if(typeof(meta["curves"]) != 'undefined'){
                $.each(meta["curves"],
                        function(k, v){
                            if(charts.hasOwnProperty(k)){
                                return;
                            }
                            charts[k] = curve_new("curves", v["title"], 
                                                  v["xlabel"], v["ylabel"], 
                                                  v["data_names"]);
                        }
                );

            }
        }

    }

    curves = state["curves"];
    html = state["html"];
    table = state["tables"];        
    if(typeof(curves) != 'undefined'){
        for(k in curves){
            i = 0;
            for(p in curves[k]){
                point = {}
                point.x = (curves[k][p].x);
                point.y = (curves[k][p].y);
                charts[k].options.data[i].dataPoints.push(point);
                i += 1;
            }
            charts[k].render();
        }
    }
    
    if(typeof(html) != 'undefined'){
        for(h in html){
            $('#'+h).html(html[h]);
        }
    }


}   
