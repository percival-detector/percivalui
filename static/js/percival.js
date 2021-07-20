api_version = '0.1';
monitor_names = [];
monitor_desc = {};
current_page = "configuration-view";
config_files = "";

percival = {
    api_version: '0.1',
    current_page: '.home-view',
    monitors: {},
    monitor_count: 0,
    monitor_divs: 0,
    groups: {},
    control_names: [],
    current_config: '',
    buffer_values: [],
    write_buffer_rbv: [
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1
    ],
    read_buffer_rbv: [
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1
    ],
    status: {}
};


String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

$.put = function(url, data, callback, type)
{
  if ( $.isFunction(data) ){
    type = type || callback,
    callback = data,
    data = {}
  }

  return $.ajax({
    url: url,
    type: 'PUT',
    success: callback,
    data: data,
    contentType: type
  });
}

class ProgressBar
{
	constructor(id, labelId, units)
	{
		this.elem = $('#' + id);
		this.label = $('#' + labelId);
		this.units = units;
	}

	update(val)
	{
		var min = parseInt(this.elem.attr("aria-valuemin"));
		var max = parseInt(this.elem.attr("aria-valuemax"));
		
		var adjusted;
		if(val < min)
			adjusted = min;
		else if(val > max)
			adjusted = max;
		else
			adjusted = (val - min) / max * 100;

		this.elem.css("width", adjusted + "%");
		this.label.html(Math.round(val * 100) / 100 + this.units);
	}
}

class Monitor
{
  constructor(parent, id, device)
  {
    //this.parent = parent;
    this.disp_name = id;
    this.id = id.split(' ').join('_');
    this.device = device.device;
    this.unit = device.unit;
    this.low_threshold = device.low_threshold;
    this.extreme_low_threshold = device.extreme_low_threshold;
    this.high_threshold = device.high_threshold;
    this.extreme_high_threshold = device.extreme_high_threshold;
    this.safety_exception = device.safety_exception;
    this.i2c_comms_error = device.i2c_comms_error;
    this.value = 0.0;
    this.raw_value = 0;
    this.sample_number = 0;
    this.html_text = "<div class=\"panel-heading clearfix\">" +
                     "<span class=\"panel-title pull-left\">" + this.disp_name + "</span>" +
                     "<button type=\"button\" id=\"" + this.id +
                     "-expbtn\" class=\"btn btn-outline-info btn-sm pull-right float-align-vertical\">" +
                     "<span id=\"" + this.id + "-expglp\" class=\"glyphicon glyphicon-resize-full\"></span></button></div>" +
                     "<table>";
                     //"<tr><td width=120px>Device:</td><td colspan=2 width=150px>" + this.device + "</td></tr>";
    if (this.device == "LTC2309"){
      this.html_text += "<tr><td width=120px>Value:</td><td colspan=2 id=\"" + this.id + "-value\">0.000 ";
    } else if (this.device == "MAX31730"){
      this.html_text += "<tr><td width=120px>Temperature:</td><td colspan=2 id=\"" + this.id + "-value\">0.000 ";
    }
    this.html_text += this.unit + "</td></tr></table>";
    this.html_text += "<table id=\"" + this.id + "-dtbl\">";
    this.html_text += "<tr><td width=120px>Raw Value:</td><td colspan=2 id=\"" + this.id + "-raw\">0</td></tr>";
    this.html_text += "<tr><td width=120px>Sample Number:</td><td colspan=2 id=\"" + this.id + "-sample\">0</td></tr>";
    this.html_text += "<tr><td width=120px></td><td width=75px>Warn</td><td width=75px>Error</td></tr>";
    this.html_text += "<tr><td>Low:</td><td id=\"" + this.id + "-low\">" + led_html(parseInt(device.low_threshold), "yellow", 25) + "</td>" +
                      "<td id=\"" + this.id + "-lolo\">" + led_html(parseInt(device.extreme_low_threshold), "red", 25) + "</td></tr>" + 
                      "<tr><td>High:</td><td id=\"" + this.id + "-high\">" + led_html(parseInt(device.high_threshold), "yellow", 25) + "</td>" + 
                      "<td id=\"" + this.id + "-hihi\">" + led_html(parseInt(device.extreme_high_threshold), "red", 25) + "</td></tr>" + 
                      "<tr><td>Safety Exception:</td><td></td><td id=\"" + this.id + "-safety\">" + led_html(parseInt(device.safety_exception), "red", 25) + "</td>" +
                      "<tr><td>i2c Error:</td><td></td><td id=\"" + this.id + "-i2c\">" + led_html(parseInt(device.i2c_comms_error), "red", 25) + "</td>" +
                      "</table>";

    this.set_parent(parent);

//    $(this.parent).html(this.html_text);
//    $('#' + this.id + '-dtbl').hide();
//    $('#' + this.id + '-expbtn').click(function(){
//        //alert("Clicked!! " + $(this).attr("id"));
//        if ($('#' + $(this).attr("id").replace('-expbtn', '-dtbl')).is(':visible')){
//            $('#' + $(this).attr("id").replace('-expbtn', '-dtbl')).hide();
//            $('#' + $(this).attr("id").replace('-expbtn', '-expglp')).removeClass('glyphicon-resize-small');
//            $('#' + $(this).attr("id").replace('-expbtn', '-expglp')).addClass('glyphicon-resize-full');
//        } else {
//            $('#' + $(this).attr("id").replace('-expbtn', '-dtbl')).show();
//            $('#' + $(this).attr("id").replace('-expbtn', '-expglp')).removeClass('glyphicon-resize-full');
//            $('#' + $(this).attr("id").replace('-expbtn', '-expglp')).addClass('glyphicon-resize-small');
//        }
//    });
    this.update(device);
  }

  set_parent(parent)
  {
    this.parent = parent;
    $(this.parent).html(this.html_text);
    $('#' + this.id + '-dtbl').hide();
    $('#' + this.id + '-expbtn').click(function(){
        //alert("Clicked!! " + $(this).attr("id"));
        if ($('#' + $(this).attr("id").replace('-expbtn', '-dtbl')).is(':visible')){
            $('#' + $(this).attr("id").replace('-expbtn', '-dtbl')).hide();
            $('#' + $(this).attr("id").replace('-expbtn', '-expglp')).removeClass('glyphicon-resize-small');
            $('#' + $(this).attr("id").replace('-expbtn', '-expglp')).addClass('glyphicon-resize-full');
        } else {
            $('#' + $(this).attr("id").replace('-expbtn', '-dtbl')).show();
            $('#' + $(this).attr("id").replace('-expbtn', '-expglp')).removeClass('glyphicon-resize-full');
            $('#' + $(this).attr("id").replace('-expbtn', '-expglp')).addClass('glyphicon-resize-small');
        }
    });
  }

  hide()
  {
    $(this.parent).hide();
  }

  show()
  {
    $(this.parent).insertAfter('#status-anchor');
    $(this.parent).show();
  }

  update(device)
  {
    if (this.device == "LTC2309"){
      if (this.value != device.value){
        this.update_value(device.value);
      }
    } else if (this.device == "MAX31730"){
      if (this.value != device.temperature){
        this.update_value(device.temperature);
      }
    }
    if (this.raw_value != device.raw_value){
      this.update_raw_value(device.raw_value);
    }
    if (this.sample_number != device.sample_number){
      this.update_sample_number(device.sample_number);
    }
    this.update_warnings(device.low_threshold, device.high_threshold);
    this.update_errors(device.extreme_low_threshold,
                       device.extreme_high_threshold,
                       device.safety_exception,
                       device.i2c_comms_error);
  }
  
  update_raw_value(value)
  {
    $('#' + this.id + '-raw').html("" + parseInt(value));
    this.raw_value = value;
  }

  update_sample_number(value)
  {
    $('#' + this.id + '-sample').html("" + parseInt(value));
    this.sample_number = value;
  }

  update_value(value)
  {
    $('#' + this.id + '-value').html("" + parseFloat(value).toFixed(3) + " " + this.unit);
    this.value = value;
  }

  update_warnings(low_val, high_val)
  {
    $('#' + this.id + '-low').html(led_html(parseInt(low_val), "yellow", 25));
    $('#' + this.id + '-high').html(led_html(parseInt(high_val), "yellow", 25));
    this.high_threshold = high_val;
    this.low_threshold = low_val;
    if (high_val == 1 || low_val == 1){
        $(this.parent).addClass("panel-warning");
    } else {
        $(this.parent).removeClass("panel-warning");
    }
  }

  update_errors(lolo_val, hihi_val, safety, comms)
  {
    $('#' + this.id + '-hihi').html(led_html(parseInt(hihi_val), "red", 25));
    $('#' + this.id + '-lolo').html(led_html(parseInt(lolo_val), "red", 25));
    $('#' + this.id + '-safety').html(led_html(parseInt(safety), "red", 25));
    $('#' + this.id + '-i2c').html(led_html(parseInt(comms), "red", 25));
    this.extreme_high_threshold = hihi_val;
    this.extreme_low_threshold = lolo_val;
    this.safety_exception = safety;
    this.i2c_comms_error = comms;
    if (comms == 1){
        $(this.parent).addClass("panel-danger");
    } else {
        $(this.parent).removeClass("panel-danger");
    }
  }
}

$( document ).ready(function() 
{
  update_api_version();
  update_api_adapters();
  update_server_setup();
  //render('#/home-view');
  render(decodeURI(window.location.hash));

  setInterval(update_server_setup, 1000);
  setInterval(update_api_read_monitors, 1000);
  setInterval(update_api_read_controls, 1000);
  setInterval(update_api_read_write_buffer, 1000);
  setInterval(update_api_read_status, 100);
  setInterval(update_server_command_status, 500);

  create_write_buffer(16, 'Zeros');

  $('#server-hw-reconnect').click(function(){
    reconnect_hardware();
  });
  $('#server-db-reconnect').click(function(){
    reconnect_db();
  });
  $('#server-ar-start').click(function(){
    auto_read('start');
  });
  $('#server-ar-stop').click(function(){
    auto_read('stop');
  });
  $('#server-sys-cmd').click(function(){
    send_system_command();
  });
  $('#channel-settings-cmd').click(function(){
    send_load_config_command();
  });
  $('#server-init-cmd').click(function(){
    send_init_command();
  });
  $('#server-set-channel-cmd').click(function(){
    send_set_channel_command();
  });
  $('#server-set-system-val-cmd').click(function(){
      send_set_system_setting_command()
  });
//  $('#server-set-point-cmd').click(function(){
//    send_set_point_command();
//  });
  $('#refresh-monitors').click(function(){
    send_refresh_monitors_command();
  });
  $('#server-scan-set-point-cmd').click(function(){
    send_scan_command();
  });
  $('#server-sscan-set-point-cmd').click(function(){
    send_sscan_command();
  });
  $('#server-abort-scan-cmd').click(function(){
    send_abort_scan_command();
  });
  $('#server-config-cmd').click(function(){
    send_config_command();
  });
  $('#select-config-file').on('change', function(event){
    //alert(event.target.files[0]);
    reader = new FileReader();
    reader.onloadend = function(event){
        //alert(event.target.result);
        percival.current_config = event.target.result
    };
    reader.readAsText(event.target.files[0], 'UF-8');
  });
  $('#buffer-fill-type').on('change', function(event){
      update_buffer_values();
  });
  $('#buffer-no-words').on('change', function(event){
      update_buffer_values();
  });
  $('#buffer-write-to-hw').click(function(){
      write_buffer_values();
  });
  $('#buffer-write-read').click(function(){
      write_buffer_refresh();
  });
  $('#buffer-read-refresh').click(function(){
      read_buffer_refresh();
  });
  $('#buffer-trns-apply').click(function(){
      buffer_transfer_apply();
  });

  $(window).on('hashchange', function(){
		// On every hash change the render function is called with the new hash.
		// This is how the navigation of the app is executed.
		render(decodeURI(window.location.hash));
	});
});

function reconnect_hardware()
{
    $.put('/api/' + api_version + '/percival/cmd_connect_hardware', function(response){});
}

function reconnect_db()
{
    $.put('/api/' + api_version + '/percival/influxdb/connect', function(response){});
}

function auto_read(action)
{
    $.put('/api/' + api_version + '/percival/auto_read/' + action, function(response){});
}

function send_refresh_monitors_command()
{
    $.put('/api/' + api_version + '/percival/cmd_update_monitors', function(response){});
}

function send_config_command()
{
    element = $('#select-config-file')[0];
    reader = new FileReader();
    reader.onloadend = function(event){
        //alert(event.target.result);
        percival.current_config = event.target.result

        config_type = $('#select-config').find(":selected").text();
        $.ajax({
            url: '/api/' + api_version + '/percival/cmd_load_config',
            type: 'PUT',
            dataType: 'json',
            data: 'config=' + encodeURIComponent(percival.current_config.replaceAll('=', '::')) + '&config_type=' + config_type,
            headers: {'Content-Type': 'application/json',
                      'Accept': 'application/json'},
            success: process_cmd_response
        });
    }
    reader.readAsText(element.files[0], 'UF-8');
}

function send_system_command()
{
    cmd_name = $('#select-sys-cmd').find(":selected").text();
    $.put('/api/' + api_version + '/percival/cmd_system_command?name=' + cmd_name, process_cmd_response);
}

function send_load_config_command()
{
    $.put('/api/' + api_version + '/percival/cmd_download_channel_cfg', process_cmd_response);
}

function send_init_command()
{
    $.put('/api/' + api_version + '/percival/cmd_initialise_channels', process_cmd_response);
}

function send_set_channel_command()
{
    set_name = $('#control-set-channel').find(":selected").text();
    set_value = $('#server-set-channel-val').val();
    $.put('/api/' + api_version + '/percival/cmd_set_channel?channel=' + set_name + '&value=' + set_value, process_cmd_response);
}

function send_set_system_setting_command()
{
    set_name = $('#set-system-value').find(":selected").text();
    set_value = $('#server-set-system-val').val();
    $.put('/api/' + api_version + '/percival/cmd_system_setting?setting=' + set_name + '&value=' + set_value, process_cmd_response);
}

//function send_set_point_command()
//{
//    set_name = $('#select-set-point').find(":selected").text();
//    $.put('/api/' + api_version + '/percival/cmd_apply_setpoint?setpoint=' + set_name, process_cmd_response);
//}

function send_scan_command()
{
    //data = {}
    sp = [$('#scan-set-point-start').find(":selected").text(),$('#scan-set-point-end').find(":selected").text()];
    //data = {'setpoints': sp};
    //alert(data)
    steps = $('#scan-sp-steps').val();
    dwell = $('#scan-sp-dwell').val();
    //$.put('/api/' + api_version + '/percival/cmd_scan_setpoints?dwell=' + dwell + '&steps=' + steps, data, process_cmd_response, 'json');
    //alert('/api/' + api_version + '/percival/cmd_scan_setpoints?dwell=' + dwell + '&steps=' + steps);
    $.ajax({
        url: '/api/' + api_version + '/percival/cmd_scan_setpoints',
        type: 'PUT',
        dataType: 'json',
        data: {
            'dwell' : dwell,
            'steps' : steps,
            'setpoints' : sp
        },
        headers: {'Content-Type': 'application/json',
                  'Accept': 'application/json'},
        success: process_cmd_response
    });
}

function send_sscan_command()
{
    //data = {}
    sp = $('#sscan-set-point-end').find(":selected").text();
    //data = {'setpoints': sp};
    //alert(data)
    steps = $('#sscan-sp-steps').val();
    dwell = $('#sscan-sp-dwell').val();
    //$.put('/api/' + api_version + '/percival/cmd_scan_setpoints?dwell=' + dwell + '&steps=' + steps, data, process_cmd_response, 'json');
    //alert('/api/' + api_version + '/percival/cmd_scan_setpoints?dwell=' + dwell + '&steps=' + steps);
    $.ajax({
        url: '/api/' + api_version + '/percival/cmd_scan_setpoints',
        type: 'PUT',
        dataType: 'json',
        data: {
            'dwell' : dwell,
            'steps' : steps,
            'setpoints' : sp
        },
        headers: {'Content-Type': 'application/json',
                  'Accept': 'application/json'},
        success: process_cmd_response
    });
}

function write_buffer_values()
{
    $.ajax({
        url: '/api/' + api_version + '/percival/cmd_write_buffer',
        type: 'PUT',
        dataType: 'json',
        data: {
            'data' : percival.buffer_values
        },
        headers: {'Content-Type': 'application/json',
                  'Accept': 'application/json'},
        success: process_cmd_response
    });
}

function write_buffer_refresh()
{
    $.ajax({
        url: '/api/' + api_version + '/percival/cmd_refresh_write_buffer',
        type: 'PUT',
        dataType: 'json',
        headers: {'Content-Type': 'application/json',
                  'Accept': 'application/json'},
        success: process_cmd_response
    });
}

function read_buffer_refresh()
{
    $.ajax({
        url: '/api/' + api_version + '/percival/cmd_refresh_read_buffer',
        type: 'PUT',
        dataType: 'json',
        headers: {'Content-Type': 'application/json',
                  'Accept': 'application/json'},
        success: process_cmd_response
    });
}

function buffer_transfer_apply()
{
    target = $('#buffer-trns-target').find(":selected").val();
    cmd = $('#buffer-trns-cmd').find(":selected").val();
//    alert("Target: " + target + " Cmd: " + cmd);
    pts = parseInt($('#buffer-trns-no-words').val());
    if (isNaN(pts) || pts < 1 || pts > 64){
        alert("Number of words must be an integer between 1 and 64");
        return;
    }
    address = parseInt($('#buffer-trns-address').val());
    if (isNaN(address) || address < 0){
        alert("Number of words must be an integer 0 or greater");
        return;
    }
//    alert("Number: " + pts + " Address: " + address);

    $.ajax({
        url: '/api/' + api_version + '/percival/cmd_buffer_transfer',
        type: 'PUT',
        dataType: 'json',
        data: {
            'target' : target,
            'command' : cmd,
            'words': pts,
            'address': address
        },
        headers: {'Content-Type': 'application/json',
                  'Accept': 'application/json'},
        success: process_cmd_response
    });
}

function send_abort_scan_command()
{
    $.put('/api/' + api_version + '/percival/cmd_abort_scan', process_cmd_response);
}

function process_cmd_response(response)
{
    str = "Cannot submit command whilst another is active";
    if(response.response == "Failed" && 0<response.error.indexOf(str))
    {
        alert("Busy - your command was rejected; please retry later.");
    }
}


function update_server_command_status()
{
    $.getJSON('/api/' + api_version + '/percival/action/', function(response) {
        $('#ctrl-resp-cmd').text("Command: " + response.command);
        $('#ctrl-resp-success').text(response.response);
        $('#ctrl-resp-time').text(response.time);
        if (response.response == 'Failed'){
            if ($('#ctrl-resp-message').text() != response.error){
                alert(response.error);
            }
            $('#ctrl-resp-message').text(response.error);
            $('#ctrl-msg-response').addClass("panel-danger");
            $('#ctrl-msg-response').removeClass("panel-default");
            $('#ctrl-msg-response').removeClass("panel-warning");
            $('#ctrl-msg-response').removeClass("panel-success");
        } else if (response.response == 'Active'){
            $('#ctrl-resp-message').text("");
            $('#ctrl-msg-response').removeClass("panel-danger");
            $('#ctrl-msg-response').removeClass("panel-default");
            $('#ctrl-msg-response').addClass("panel-warning");
            $('#ctrl-msg-response').removeClass("panel-success");
        } else {
            $('#ctrl-resp-message').text("");
            $('#ctrl-msg-response').removeClass("panel-default");
            $('#ctrl-msg-response').removeClass("panel-danger");
            $('#ctrl-msg-response').removeClass("panel-warning");
            $('#ctrl-msg-response').addClass("panel-success");
        }
        pn = response.param_names;
        html = "<table>";
        for (var index=0; index < pn.length; index++){
            html += "<tr><td>" + pn[index] + " = " + response.parameters[pn[index]] + "</td></tr>";
        }
        html += "</table>";
        $('#ctrl-resp-param').html(html);
    });

    //alert(response.command);
}

function update_api_version() {

    $.getJSON('/api', function(response) {
        $('#api-version').html(response.api_version);
        percival.api_version = response.api_version;
    });
}

function update_api_adapters() {
//alert("HERE");
    $.getJSON('/api/' + api_version + '/adapters/', function(response) {
        adapter_list = response.adapters.join(", ");
        $('#api-adapters').html(adapter_list);
        //alert(adapter_list);
    });
}

function update_server_setup() {
    $.getJSON('/api/' + api_version + '/percival/driver/', function(response) {
        $('#server-start-time').html(response.start_time);
        $('#server-up-time').html(response.up_time);
        $('#server-username').html(response.username);
        $('#server-db-address').html(response.influx_db.address);
        $('#server-db-port').html(response.influx_db.port);
        $('#server-db-name').html(response.influx_db.name);
        if (response.influx_db.connected){
            connected = 1;
            $('#server-db-reconnect').hide();
            $('#server-db-connected').html(led_html(1, "green", 25));
        } else {
            connected = 0;
            $('#server-db-reconnect').show();
            $('#server-db-connected').html(led_html(1, "red", 25));
        }
        $('#server-hw-address').html(response.hardware.address);
        $('#server-hw-port').html(response.hardware.port);
        if (response.hardware.connected){
            connected = 1;
            $('#server-hw-reconnect').hide();
            $('#server-hw-connected').html(led_html(1, "green", 25));
        } else {
            connected = 0;
            $('#server-hw-reconnect').show();
            $('#server-hw-connected').html(led_html(1, "red", 25));
        }
        if (response.auto_read){
            $('#server-ar-start').hide();
            $('#server-ar-stop').show();
            $('#server-ar-status').html(led_html(1, "green", 25));
        } else {
            $('#server-ar-start').show();
            $('#server-ar-stop').hide();
            $('#server-ar-status').html(led_html(1, "red", 25));
        }
    });
    $.getJSON('/api/' + api_version + '/percival/groups/', function(response) {
        percival.groups = response

        // Group list
        mg = percival.groups.monitor_groups.group_names.sort();
        html = "<li role=\"presentation\"><a role=\"menuitem\" tabindex=\"-1\" href=\"#/status-view\" onclick=\"update_visible_monitors('All')\">All</a></li>";
        for (var index=0; index < mg.length; index++){
            html += "<li role=\"presentation\"><a role=\"menuitem\" tabindex=\"-1\" href=\"#/status-view\" onclick=\"update_visible_monitors('"+mg[index]+"')\">"+mg[index]+"</a></li>";
        }
        $('#status-group').html(html);
        //alert(JSON.stringify(response));

        // Control channels for manual set points
        cg = percival.groups.control_groups.group_names.concat(percival.control_names);
		html = "";
		for (var index=0; index < cg.length; index++){
            html += "<option role=\"presentation\">" + cg[index] + "</option>";
        }
        if (html != $('#control-set-channel').html()){
            $('#control-set-channel').html(html);
        }
    });
    $.getJSON('/api/' + api_version + '/percival/commands/', function(response) {
        percival.sys_commands = response.commands;
		html = "";
		for (var index=0; index < percival.sys_commands.length; index++){
            html += "<option role=\"presentation\">" + percival.sys_commands[index] + "</option>";
        }
        if (html != $('#select-sys-cmd').html()){
            $('#select-sys-cmd').html(html);
        }
    });
    $.getJSON('/api/' + api_version + '/percival/system_values/', function(response) {
        percival.system_values = response.system_values.sort();
		html = "";
		for (var index=0; index < percival.system_values.length; index++){
            html += "<option role=\"presentation\">" + percival.system_values[index] + "</option>";
        }
        if (html != $('#set-system-value').html()){
            $('#set-system-value').html(html);
        }
    });
    $.getJSON('/api/' + api_version + '/percival/setpoints/', function(response) {
        //alert(response);
        percival.set_points = response.setpoints.sort();
		html = "";
		for (var index=0; index < percival.set_points.length; index++){
            html += "<option role=\"presentation\">" + percival.set_points[index] + "</option>";
        }
        //alert(html);
        //if (html != $('#select-set-point').html()){
        //    $('#select-set-point').html(html);
        //}
        if (html != $('#scan-set-point-start').html()){
            $('#scan-set-point-start').html(html);
        }
        if (html != $('#scan-set-point-end').html()){
            $('#scan-set-point-end').html(html);
        }
        if (html != $('#sscan-set-point-end').html()){
            $('#sscan-set-point-end').html(html);
        }
        $('#sp-scan-scanning').text(response.status.scanning);
        $('#sp-scan-index').text(response.status.scan_index);
        if (response.status.scan){
            $('#sp-scan-scanpoints').text(response.status.scan);
        }
    });
}

function update_visible_monitors(group)
{
    $('#status-group-name').text("Channels [ " + group + " ] ");

    var mon_length = monitor_names.length;
    //alert(mon_length);
    for (var index = 0; index < mon_length; index++){
        if (group == "All"){
            percival.monitors[monitor_names[index]].show();
        } else {

            percival.monitors[monitor_names[index]].hide();
        }
    }

    if (group != "All"){
        var monitors = percival.groups.monitor_groups[group].channels;
        for (var index = 0; index < monitors.length; index++){
            percival.monitors[monitors[index]].show();
        }
    }
}

function update_api_read_boards() {

    $.getJSON('/api/' + api_version + '/percival/boards/', function(response) {
        board_list = response["boards"];
        $('#overall-boards').tabulator({columns:[
                                          {title:"Name", field:"name", sorter:"string", width:"50%"},
                                          {title:"Type", field:"type", sorter:"string", width:"20%"},
                                          {title:"Controls", field:"controls", sorter:"number", width:"15%"},
                                          {title:"Monitors", field:"monitors", sorter:"number", width:"15%"}
                                          ]
                                        });
        var len = board_list.length;
        var monitor_count = 0;
        var tableData = [];
        for (var index = 0; index < len; index++){
            monitor_count += response[board_list[index]].monitors_count;
            tableData[index] = { id: index,
                               name:response[board_list[index]].name,
                               type:response[board_list[index]].type,
                               controls:response[board_list[index]].controls_count,
                               monitors:response[board_list[index]].monitors_count };
            }
        $('#overall-boards').tabulator("setData", tableData);
    });
}

function update_api_read_controls() {

    $.getJSON('/api/' + api_version + '/percival/controls/', function(response) {
        percival.control_names = response["controls"].sort();
        percival.control_desc = response;
        percival.control_count = percival.control_names.length;
    });
}

function update_api_read_monitors()
{
    $.getJSON('/api/' + api_version + '/percival/monitors/', function(response) {
        monitor_names = response["monitors"].sort();
        monitor_desc = response;
        percival.monitor_count = monitor_names.length;
    });
}

function update_buffer_values()
{
    ft = $('#buffer-fill-type').find(":selected").val();
    pts = parseInt($('#buffer-no-words').val());
    if (isNaN(pts) || pts < 1 || pts > 64){
        alert("Number of words must be an integer between 1 and 64");
    } else {
        create_write_buffer(pts, ft);
    }
}

function create_write_buffer(no_of_words, fill_type)
{
    data_words = [];
    for (index = 0; index < no_of_words; index++){
        switch (fill_type){
            case 'Zeros':
                // Filling with zeros
                data_words.push(0);
                break;
            case 'Ones':
                // Filling with ones
                data_words.push(4294967295);
                break;
            case 'Incrementing':
                // Incrementing
                data_words.push(index+1);
                break;
            case 'Decrementing':
                // Decrementing
                data_words.push(no_of_words-index);
                break;
        }
    }
    percival.buffer_values = data_words;
    render_write_buffer(data_words);
}

function render_write_buffer(data_words)
{
    $('#write-buffer').tabulator({
        height: "220px",
        pagination: "local",
        columns: [
            {title: "Index", field: "index", sorter: "string", width: "20%"},
            {title: "Value", field: "value", sorter: "string", width: "70%"}
        ]
    });
    var tableData = [];
    for (var index = 0; index < data_words.length; index++) {
        tableData[index] = {
            id: index,
            index: index,
            value: data_words[index].toString(2).padStart(32, 0)
        };
    }
    $('#write-buffer').tabulator("setData", tableData);
}

function update_api_read_write_buffer() {

    $.getJSON('/api/' + api_version + '/percival/write_buffer/', function(response) {
        match = 1;
        for (var index = 0; index < response["data"].length; index++) {
            if (response["data"][index] != percival.write_buffer_rbv[index]){
                match = 0;
            }
        }
        if (match == 0){
            percival.write_buffer_rbv = response["data"];
            render_write_buffer_rbv(response["data"]);
        }
    });
    $.getJSON('/api/' + api_version + '/percival/read_buffer/', function(response) {
        match = 1;
        for (var index = 0; index < response["data"].length; index++) {
            if (response["data"][index] != percival.read_buffer_rbv[index]){
                match = 0;
            }
        }
        if (match == 0){
            percival.read_buffer_rbv = response["data"];
            render_read_buffer_rbv(response["data"]);
        }
    });
}


function render_write_buffer_rbv(data_words)
{
    $('#write-buffer-rbv').tabulator({height:"220px",
                                  pagination:"local",
                                  columns:[
                                  {title:"Index", field:"index", sorter:"string", width:"20%"},
                                  {title:"Value", field:"value", sorter:"string", width:"70%"}
                                  ]
                                });
    var tableData = [];
    for (var index = 0; index < data_words.length; index++){
        tableData[index] = { id: index,
                             index:index,
                             value:data_words[index].toString(2).padStart(32, 0)};
    }
    $('#write-buffer-rbv').tabulator("setData", tableData);

}

function render_read_buffer_rbv(data_words)
{
    $('#read-buffer-rbv').tabulator({height:"220px",
                                  pagination:"local",
                                  columns:[
                                  {title:"Index", field:"index", sorter:"string", width:"20%"},
                                  {title:"Value", field:"value", sorter:"string", width:"70%"}
                                  ]
                                });
    var tableData = [];
    for (var index = 0; index < data_words.length; index++){
        tableData[index] = { id: index,
                             index:index,
                             value:data_words[index].toString(2).padStart(32, 0)};
    }
    $('#read-buffer-rbv').tabulator("setData", tableData);

}

function render_config_view()
{

    $('#overall-controls').tabulator({height:"220px",
                                      pagination:"local",
                                      columns:[
                                      {title:"Name", field:"name", sorter:"string", width:"50%"},
                                      {title:"Type", field:"type", sorter:"string", width:"50%"}
                                      ]
                                    });
    var len = percival.control_names.length;
    var tableData = [];
    for (var index = 0; index < len; index++){
        tableData[index] = { id: index,
                             name:percival.control_names[index],
                             type:percival.control_desc[percival.control_names[index]] };
    }
    $('#overall-controls').tabulator("setData", tableData);

    //$('#overall-monitors').html("");
    $('#overall-monitors').tabulator({height:"220px",
                                      pagination:"local",
                                      columns:[
                                      {title:"Name", field:"name", sorter:"string", width:"50%"},
                                      {title:"Type", field:"type", sorter:"string", width:"50%"}
                                      ]
                                    });
    var len = monitor_names.length;
    var tableData = [];
    for (var index = 0; index < len; index++){
        tableData[index] = { id: index,
                             name:monitor_names[index],
                             type:monitor_desc[monitor_names[index]] };
    }
    $('#overall-monitors').tabulator("setData", tableData);
}

function update_api_read_status()
{
  $.getJSON('/api/' + api_version + '/percival/status/', function(response) {
    var detector = response['detector'];
    $('#det-image-counter').html(detector['Image_counter']);
    $('#det-acq-counter').html(detector['Acquisition_counter']);
    $('#det-train-number').html(detector['Train_number']);

//    if (percival.status['LVDS_IOs_enabled'] != detector['LVDS_IOs_enabled']) {
//        percival.status['LVDS_IOs_enabled'] = detector['LVDS_IOs_enabled'];
//        $('#det-lvds-enabled').html(led_html(detector['LVDS_IOs_enabled'], 'green', 20));
//        flash_element($('#det-lvds-enabled'));
//    }

    update_status(detector, '#det-lvds-enabled', 'LVDS_IOs_enabled', 'green');
    update_status(detector, '#det-safety-actions', 'safety_actions_enabled', 'green');

    $('#det-master-reset').html(led_html(detector['Master_reset'],'green', 20));
    $('#det-pll-reset').html(led_html(detector['PLL_reset'],'green', 20));
    $('#det-dmux-cdn').html(led_html(detector['dmux_CDN'],'green', 20));
    $('#det-sr7din-0').html(led_html(detector['sr7DIn_0'],'green', 20));
    $('#det-sr7din-1').html(led_html(detector['sr7DIn_1'],'green', 20));
    $('#det-horiz-data-in-0').html(led_html(detector['horiz_data_in_0'],'green', 20));
    $('#det-horiz-data-in-1').html(led_html(detector['horiz_data_in_1'],'green', 20));
    $('#det-enable-testpoints').html(led_html(detector['enable_testpoints'],'green', 20));
    $('#det-startup-mode-enabled').html(led_html(detector['startup_mode_enabled'],'green', 20));
    $('#det-global-monitoring').html(led_html(detector['global_monitoring_enabled'],'green', 20));
    $('#det-device-safety').html(led_html(detector['device_level_safety_controls_enabled'],'green', 20));
    $('#det-system-safety').html(led_html(detector['system_level_safety_controls_enabled'],'green', 20));
    $('#det-exp-safety').html(led_html(detector['experimental_level_safety_controls_enabled'],'green', 20));
//    $('#det-safety-actions').html(led_html(detector['safety_actions_enabled'],'green', 20));
    $('#det-system-armed').html(led_html(detector['system_armed'],'green', 20));

    $('#det-acquiring').html(led_html(detector['acquiring'],'green', 20));
    $('#det-waiting-for-trigger').html(led_html(detector['wait_for_trigger'],'green', 20));
    $('#det-sensor-active').html(led_html(detector['sensor_active_for_acquisition'],'green', 20));
    $('#det-mezz-a-phy-ok').html(led_html(detector['MEZZ_A_PHY_OK'],'green', 20));
    $('#det-mezz-a-mgt-ok').html(led_html(detector['MEZZ_A_MGT_OK'],'green', 20));
    $('#det-mezz-a-reset').html(led_html(detector['MEZZ_A_RESET'],'red', 20));
    $('#det-mezz-b-phy-ok').html(led_html(detector['MEZZ_B_PHY_OK'],'green', 20));
    $('#det-mezz-b-mgt-ok').html(led_html(detector['MEZZ_B_MGT_OK'],'green', 20));
    $('#det-mezz-b-reset').html(led_html(detector['MEZZ_B_RESET'],'red', 20));
    $('#det-marker-out-0').html(led_html(detector['MARKER_OUT_0'],'green', 20));
    $('#det-marker-out-1').html(led_html(detector['MARKER_OUT_1'],'green', 20));
    $('#det-marker-out-2').html(led_html(detector['MARKER_OUT_2'],'green', 20));
    $('#det-marker-out-3').html(led_html(detector['MARKER_OUT_3'],'green', 20));
    $('#det-include-train').html(led_html(detector['include_train_number_in_status_record'],'green', 20));
    $('#det-plugin-reset').html(led_html(detector['PLUGIN_RESET'],'green', 20));
    $('#det-data-synch-error').html(led_html(detector['DataSynchError'],'green', 20));

    $('#det-hclock-0').html(led_html(detector['HIGH_FREQ_ADJ_CLOCK_0_clock_enable'],'green', 20));
    $('#det-hclock-1').html(led_html(detector['HIGH_FREQ_ADJ_CLOCK_1_clock_enable'],'green', 20));
    $('#det-hclock-2').html(led_html(detector['HIGH_FREQ_ADJ_CLOCK_2_clock_enable'],'green', 20));
    $('#det-hclock-3').html(led_html(detector['HIGH_FREQ_ADJ_CLOCK_3_clock_enable'],'green', 20));
    $('#det-lclock-0').html(led_html(detector['LOW_FREQ_ADJ_CLOCK_0_clock_enable'],'green', 20));
    $('#det-lclock-1').html(led_html(detector['LOW_FREQ_ADJ_CLOCK_1_clock_enable'],'green', 20));

    $('#safety-3').html(led_html(detector['safety_driven_assert_marker_out_3_completed'],'green', 20));
    $('#safety-2').html(led_html(detector['safety_driven_assert_marker_out_2_completed'],'green', 20));
    $('#safety-1').html(led_html(detector['safety_driven_assert_marker_out_1_completed'],'green', 20));
    $('#safety-0').html(led_html(detector['safety_driven_assert_marker_out_0_completed'],'green', 20));
    $('#safety-fast-standby').html(led_html(detector['safety_driven_fast_enable_control_standby_completed'],'green', 20));
    $('#safety-fast-powerdown').html(led_html(detector['safety_driven_fast_sensor_powerdown_completed'],'green', 20));
    $('#safety-exit-armed').html(led_html(detector['safety_driven_exit_acquisition_armed_status_completed'],'green', 20));
    $('#safety-stop-acq').html(led_html(detector['safety_driven_stop_acquisition_completed'],'green', 20));
    //alert(detector['LVDS_IOs_enabled']);
    var len = monitor_names.length;
    render_status_view();
    var tableData = [];
    for (var index = 0; index < len; index++){
      if (percival.monitors[monitor_names[index]] == null){
        percival.monitors[monitor_names[index]] = new Monitor('#stat-' + (index+1), monitor_names[index], response[monitor_names[index]]);
      } else {
        percival.monitors[monitor_names[index]].update(response[monitor_names[index]]);
      }
    }
  });
}

function update_status(detector, tag, name, colour)
{
    if (percival.status[name] != detector[name]) {
        percival.status[name] = detector[name];
        $(tag).html(led_html(detector[name], colour, 20));
        flash_element($(tag));
    }
}

function flash_element(element)
{
    element.animate({opacity: '0.2'}, 500);
    element.animate({opacity: '1.0'}, 500);
    element.animate({opacity: '0.2'}, 500);
    element.animate({opacity: '1.0'}, 500);
    element.animate({opacity: '0.2'}, 500);
    element.animate({opacity: '1.0'}, 500);
}

function led_html(value, colour, width)
{
  var html_text = "<img width=" + width + "px src=img/";
  if (Boolean(value)==false){
    html_text += "led-off";
  } else {
    html_text +=  colour + "-led-on";
  }
  html_text += ".png></img>";
  return html_text;
}


function render(url) 
{
  // This function decides what type of page to show 
  // depending on the current url hash value.
  // Get the keyword from the url.
  var temp = "." + url.split('/')[1];
  if (url.split('/')[1]){
    document.title = url.split('/')[1] + " (Percival)";
  } else {
    document.title = "Percival";
  }
  // Hide whatever page is currently shown.
  $(".page").hide();
		
  // Show the new page
  $(temp).show();
  current_page = temp;
    
  if (temp == ".home-view"){
    update_api_version();
    update_api_adapters();
  } else if (temp == ".configuration-view"){
    // Re-request the configuration
    update_api_read_boards();
    render_config_view();
  }
}

function render_status_view()
{
    // Check if the number of monitors has increased past the number of holder divs
    if (percival.monitor_count > percival.monitor_divs){
        // Calculate the number of new rows
        var new_count = percival.monitor_count - percival.monitor_divs;
        //alert("New rows: " + new_row_count);
        for (var index = percival.monitor_divs; index < (percival.monitor_divs+new_count); index++){
            //html_text = "<div class=\"row sidebar-row vertical-align\"><div class=\"col-xs-1\">&nbsp;</div>";
            html_text = "";
                html_text += "<div id=\"stat-" + (index+1) +
                             "\" class=\"col-xs-3 status vertical-align panel panel-default\">&nbsp;</div>";
            //}
            //html_text += "</div>";
            //alert(html_text);
            // Append the rows to the container
            $('#stat-container').append(html_text);
        }
        percival.monitor_divs += new_count;
    }
}
