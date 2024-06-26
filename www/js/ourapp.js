function handleFileSelect() {
    var addColumn = function(innerHTML, tagType) {
        var child = document.createElement(tagType);
        child.innerHTML = innerHTML;
        return child;
    };

    // Avvia il caricamento
    $("#loader").show();
    $("#resultInvio").hide();
    $("#resultInvio").empty();
    var apiURL = "https://shoes.ourapp.it/api?type=scrap";
    var jqxhr = $.get( apiURL, function(data, textStatus, jqXHR) {
        // Arrivo della lista dei file in json
        var arr = data.split(",");

        var table = document.createElement('table');

        var tr = document.createElement('tr');
        tr.appendChild(addColumn("FILE", "th"));
        table.appendChild(tr);

        for (var i = 0; i < arr.length; i++) {
            var tr = document.createElement('tr');
            var row = '<a href="https://shoes.ourapp.it/scrap/' + arr[i] + '">' + arr[i] + '</a>';
            tr.appendChild(addColumn(row, "td"));
            table.appendChild(tr);
        }

        $("#resultInvio").append(table);

        // Termina il caricamento
        $("#loader").hide();

        $("#resultInvio").show();

    })
    .fail(function() {
        console.log("Errore nella richiesta lista dei channel IDs.");

        // Fine dello scrap con errore da segnalare
    })

}

function cleanFiles() {
    var apiURL = "https://shoes.ourapp.it/api?type=clean";
    var jqxhr = $.get( apiURL, function(data, textStatus, jqXHR) {
        // Arrivo della lista dei file in json
        console.log(data);
    })
    .fail(function(err) {
        console.log("Errore nella richiesta di cancellazione file: ".err);
    })
}


$("#loader").hide();
document.getElementById('the_form').addEventListener('submit', handleFileSelect, false);
document.getElementById('clean_form').addEventListener('submit', cleanFiles, false);