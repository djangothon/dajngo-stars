$(document).ready(function() {
    $('.star-get-rating').each(function (){
        var url = $(this).attr('ajax');
        var target = $(this).attr('target');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(data) {
                $("#"+target).html(data);
            },
        });
    });
    $('.star-show-rating').each(function (){
        var url = $(this).attr('ajax');
        var target = $(this).attr('target');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(data) {
                $("#"+target).html(data);
            },
        });
    });
    $('body').on('submit', '.ajax-form', function(event) {
        var $this = $(this);
        var url = $this.attr('ajax');
        var input = $this.find("input[type=submit][pressed=true]");
        var data = $(this).serialize();
        var target_id = $this.attr('target');
        var target = $('#'+target_id);
        //data.append('submit', 'True');
        $.ajax({
            url: url,
            type: 'POST',
            data: data,

            success: function(response) {
                response = JSON.parse(response);
                if (response['status'] == "OK") {
                    target.html(response['data']);
                } else {
                    target.html("There was some error in backend");
                }
            },
            error: function(response) {
                console.log(response);
                target.html("There was some error in ajax call");
            }
        });
        return false;
    });

    $('body').on('click', '.ajax-get', function(event) {
        var $this = $(this);
        var url = $this.attr('ajax');
        var input = $this.find("input[type=submit][pressed=true]");
        var data = $(this).serialize();
        var target_id = $this.attr('target');
        var target = $('#'+target_id);
        //data.append('submit', 'True');
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',

            success: function(response) {
                if (response['status'] == "OK") {
                    target.html(response['data']);
                } else {
                    target.html("There was some error in backend");
                }
            },
            error: function(response) {
                target.html("There was some error in ajax call");
            }
        });
        return false;
    });
});