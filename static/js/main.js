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