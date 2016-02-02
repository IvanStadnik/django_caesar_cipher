$(document).ready(function () {
    var plot1, current, rotation, name_of_diagram;
    name_of_diagram = 'The diagram of frequency analysis of the Caesar cipher (standard)';
    standard = window.standard;
    current = standard;
    var ticks = window.ticks;
    renderGraph()
    function renderGraph() {
        if(plot1) {
            plot1.destroy();
        }
        $.jqplot.config.enablePlugins = true;

        plot1 = $.jqplot('chart1', [current, standard], {
            // Only animate if we're not using excanvas (not in IE 7 or IE 8)..
            animate: !$.jqplot.use_excanvas,
            series:[
                {
                    color: '#44B1E3',
                    pointLabels: {
                        show: true,
                    },
                    markerOptions:{
                        size: 2,
                        color: '#fff'
                    },
                    renderer: $.jqplot.BarRenderer,
                    showHighlight: false,
                    rendererOptions: {
                        animation: {
                            speed: 2500
                        },
                        barWidth: 15,
                        barPadding: -15,
                        barMargin: 0,
                        highlightMouseOver: false,
                    },
                },
                {
                    color: '#84BF2D',
                    pointLabels: {
                        show: false
                    },
                    rendererOptions: {
                        animation: {
                            speed: 2000
                        }
                    },
                    markerOptions:{
                        size: 8,
                    },
                },
            ],
            grid: {
                  background: '#272822',
                  gridLineColor: '#646554'
            },
            legend: {
                show: true,
                location: 'nw',
                placement: 'inside',
                labels: ['&nbsp;current&nbsp;', '&nbsp;standard&nbsp;'],
                textColor: '#000',
            },
            title: {
                text:name_of_diagram,
                fontSize: '17px',
                textColor: '#0C4B33'
            },
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks: ticks,
                    tickOptions: {
                        textColor: '#000',
                        formatString: "% %.3f"
                    },
                },
                yaxis: {
                    tickOptions: {
                        textColor: '#000',
                        formatString: "% %.3f"
                    },
                    rendererOptions: {
                        forceTickAt0: true
                    }
                },
                show: true
            },
            highlighter: {
                show: true,
                showLabel: true,
                tooltipAxes: 'y',
                sizeAdjust: 7.5 , tooltipLocation : 'ne'
            }
        });
    }

// Start set header for CSRF
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    var csrftoken = $.cookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
// End set header for CSRF

// Trying to detect rotation
    $('#caesar_cipher_input').on('paste', function(){
        var self = this
        $('#background_popup').show();
        $('#caesar_cipher_output').val('');
        setTimeout(function() {
            // gets the copied text after a specified time (100 milliseconds)
            var json_data = JSON.stringify({ ciphered_text: $('#caesar_cipher_input').val() })
            $.post($('#detecting_rotation_url').val(), json_data, function(data){
                name_of_diagram = 'The diagram of frequency analysis of the Caesar cipher ( pasted text )';
                rotation = data.frequency.rotation
                current = data.frequency.frequency
                standard = data.frequency.standard
                ticks = data.frequency.symbols
                if (rotation != 0) {
                    $('.system_message').html(data.message);
                    $('.close_obj').slideDown('1000');
                }
                $('#background_popup').hide();
                renderGraph()
            }, 'json')
        }, 100);
    });

//Encrypt the text
    $('#caesar_encrypt_text').on('click', function(){
    $('#background_popup').show();
        var json_data = JSON.stringify({ text_for_encrypt: $('#caesar_cipher_input').val(),
         rotation: $('#rotation_fo_action option:selected').val()});
            $.post($('#caesar_encrypt_text_url').val(), json_data, function(data){
                $('#caesar_cipher_output').val(data.ciphered_text)
                $('#background_popup').hide();
                name_of_diagram = 'The diagram of frequency analysis of the Caesar cipher ( encrypted text )';
                current = data.frequency.frequency
                standard = data.frequency.standard
                ticks = data.frequency.symbols
                renderGraph()
            }, 'json')
    })

// Decrypt the text
    $('#caesar_decrypt_text').on('click', function(){
        $('#background_popup').show();
        var json_data = JSON.stringify({ text_for_decrypt: $('#caesar_cipher_input').val(),
         rotation: $('#rotation_fo_action option:selected').val()});
            $.post($('#caesar_decrypt_text_url').val(), json_data, function(data){
                $('#caesar_cipher_output').val(data.ciphered_text)
                name_of_diagram = 'The diagram of frequency analysis of the Caesar cipher ( decrypted text )';
                current = data.frequency.frequency
                standard = data.frequency.standard
                ticks = data.frequency.symbols
                renderGraph()
                $('#background_popup').hide();
            }, 'json')
    })

// Try decrypt the text
    $('#try_decrypt_text').on('click', function(){
        $('.close_obj').slideUp( "slow", function() {
            $('.system_message').html('');
        })
        $('#rotation_fo_action option[value="'+rotation+'"]').attr("selected", "selected");
        $('#background_popup').show();
        var json_data = JSON.stringify({ text_for_decrypt: $('#caesar_cipher_input').val(),
         rotation: $('#rotation_fo_action option:selected').val()});
            $.post($('#caesar_decrypt_text_url').val(), json_data, function(data){
                $('#caesar_cipher_output').val(data.ciphered_text);
                name_of_diagram = 'The diagram of frequency analysis of the Caesar cipher ( decrypted text )';
                current = data.frequency.frequency
                standard = data.frequency.standard
                ticks = data.frequency.symbols
                renderGraph()
                $('#background_popup').hide();
            }, 'json')
    })

//    Close message
    $('.close_message').on('click', function(){
        $('.close_obj').slideUp( "slow", function() {
            $('.system_message').html('');
        })
    })

//    Render diagram after resize the browser window
    $(window).resize(function () {
        setTimeout(function() {
            renderGraph();
        }, 100)
    })
});