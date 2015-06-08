
function update_current_state(jobname, update_function){
    $.ajax({
            type : 'POST',
            url : SCRIPT_ROOT + '/get_current_state',
            data : {"jobname": jobname},
            success : function(state){
                update_function(state);
            },
    });
}

function update_current_state_periodically(jobname, update_function, interval){
    function worker(){
        $.ajax({
                type : 'GET',
                url : SCRIPT_ROOT + '/get_current_state',
                data: {"jobname": jobname},
                success : function(state){
                    update_function(state);
                },
                complete : function(){
                    setTimeout(worker, interval)
                }
        });
    }
    worker();
}
