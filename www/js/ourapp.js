function handleFileSelect() {
    var addColumn = function(innerHTML, tagType) {
        var child = document.createElement(tagType);
        child.innerHTML = innerHTML;
        return child;
    };

    // Avvia il caricamento
    $("#loader").show();
    var apiURL = "https://shoes.ourapp.it/api?type=scrap";
    var jqxhr = $.get( apiURL, function(data, textStatus, jqXHR) {
        // Arrivo della lista dei file in json
        var arr = data.split(",");

        var table = document.createElement('table');

        var tr = document.createElement('tr');
        tr.appendChild(addColumn("FILE", "th"));
        table.appendChild(tr);

        for (var i = 0; i < arr.length; i++){
            var tr = document.createElement('tr');
            var row = '<a href="https://shoes.ourapp.it/scrap/' + arr[i] + '"></a>';
            tr.appendChild(addColumn(row, "td"));
            table.appendChild(tr);
        }

        $("#resultInvio").append(table);

        // Termina il caricamento
        //$("#loader").hide();

        $("#resultInvio").show();

    })
    .fail(function() {
        console.log("Errore nella richiesta lista dei channel IDs.");

        // Fine dello scrap con errore da segnalare
    })

}
$("#loader").hide();
document.getElementById('the_form').addEventListener('submit', handleFileSelect, false);