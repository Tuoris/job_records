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
        var property = inputs[i].name;
        if (data.hasOwnProperty(property)) {
            inputs[i].value = data[property];
        }
    }
}

var show_add_form = function () {
    var edit_form = document.getElementsByClassName('edit_record')[0];
    var add_form = document.getElementsByClassName('add_record')[0];
    add_form.classList.remove('hidden');
    edit_form.classList.add('hidden');
}
