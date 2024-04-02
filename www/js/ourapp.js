function handleFileSelect() {

    var apiURL = "https://shoes.ourapp.it/api?type=online";
    var jqxhr = $.get( apiURL, function(data, textStatus, jqXHR) {
        console.log("Sales channels: " + data);
    })
    .fail(function() {
        console.log("Errore nella richiesta lista dei channel IDs.");
    })

}

document.getElementById('the_form').addEventListener('submit', handleFileSelect, false);