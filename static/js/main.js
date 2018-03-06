var fetch_record = function(record_id, callback) {
    var xhr = new XMLHttpRequest();
    var query = 'id=' + encodeURIComponent(record_id);

    xhr.onreadystatechange = function() {
        if (xhr.readyState==4 && xhr.status==200) {
            return callback(JSON.parse(xhr.responseText));
        } else {
            return callback({});
        }
    }

    xhr.open("GET", '/get_record?' + query, true);
    xhr.send(null);

};

var edit_record = function(record_id) {
    var edit_form = document.getElementsByClassName('edit_record')[0];
    var add_form = document.getElementsByClassName('add_record')[0];
    edit_form.classList.remove('hidden');
    add_form.classList.add('hidden');

    edit_form.elements['id'].value = parseInt(record_id);

    fetch_record(
        record_id,
        function (record) {
            fill_form(edit_form, record);
        }
    );


};

var delete_record = function(record_id) {
    var xhr = new XMLHttpRequest();
    var body = 'id=' + encodeURIComponent(record_id);
    xhr.open("POST", '/delete_record', true);
    xhr.setRequestHeader(
        'Content-Type', 'application/x-www-form-urlencoded'
    );
    xhr.send(body);

    xhr.onreadystatechange = function() {
        if (xhr.readyState==4 && xhr.status==200){
            window.location.href = '';
        }
    }
};

var get_info_from = function (source) {

    var source_element = get_source_element(source);
    var source_URL = source_element.value.trim()
    if (!source_URL) {
        return;
    };

    source_element.disabled = true;
    var add_form = document.getElementsByClassName('add_record')[0];
    var edit_form = document.getElementsByClassName('edit_record')[0];

    var current_form = add_form;
    if (add_form.classList.contains('hidden')) {
        var current_form = edit_form;
    }

    fetch_info(
        source_URL,
        function (record) {
            fill_form(current_form, record);
            source_element.disabled = false;
        }
    );
};

var get_source_element = function(source) {
    var source = source.trim();

    var source_type = source[0];
    var source_name = source.slice(1);
    if (source_type == '#') {
        var source_element = document.getElementById(
            source_name
        );
    } else if (source_type == '.') {
        var source_element = document.getElementsByClassName(
            source_name
        )[0];
    } else {
        var source_element = undefined;
    }

    if (!source_element.checkValidity()) {
        source_element.reportValidity();
        return;
    }
    return source_element
}


var fetch_info = function(URL, callback) {
    var xhr = new XMLHttpRequest();
    var query = 'url=' + encodeURIComponent(URL);

    xhr.onreadystatechange = function() {
        if (xhr.readyState==4) {
            if (xhr.status == 200) {
                return callback(JSON.parse(xhr.responseText));
            } else {
                return callback({});
            }
        }
    }

    xhr.open("GET", '/get_info?' + query, true);
    xhr.send(null);

};

var isEmpty = function (obj) {
    for(var prop in obj) {
        if(obj.hasOwnProperty(prop))
            return false;
    }
    return JSON.stringify(obj) === JSON.stringify({});
}

var fill_form = function(form, data) {

    if (!data || isEmpty(data)) {
        return;
    }

    var inputs = form.elements;
    for (var i = 0; i < inputs.length; i++) {
        var input = inputs[i];
        var property = input.name;
        if (data.hasOwnProperty(property)) {
            if (input.type === 'radio') {
                var matched = String(input.value) === String(data[property]);
                if (matched) {
                    input.checked = true;
                }
            } else {
                input.value = data[property];
            }
        }
    }
}

var show_add_form = function () {
    var edit_form = document.getElementsByClassName('edit_record')[0];
    var add_form = document.getElementsByClassName('add_record')[0];
    add_form.classList.remove('hidden');
    edit_form.classList.add('hidden');
}
