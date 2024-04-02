function handleFileSelect() {

    var apiURL = "https://shoes.ourapp.it/api?type=online";
    var jqxhr = $.get( apiURL, function(data, textStatus, jqXHR) {
        // Arrivo della lista dei file in json
        var arr = data.split(",");


        var table = document.createElement('table');

        var tr = document.createElement('tr');
        tr.appendChild(addColumn("FILE", "th"));
        table.appendChild(tr);

        for (var i = 0; i < arr.length; i++){
            var tr = document.createElement('tr');
            var row = arr[i];
            tr.appendChild(addColumn(row, "td"));
            table.appendChild(tr);
        }

        $("#resultInvio").append(table);
        $("#resultInvio").show();

    })
    .fail(function() {
        console.log("Errore nella richiesta lista dei channel IDs.");
    })

}

document.getElementById('the_form').addEventListener('submit', handleFileSelect, false);