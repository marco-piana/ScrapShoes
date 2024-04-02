$("#resultInvio").hide();
var apiURLUpdate = "https://zalando.ourapp.it/api?type=PriceUpdateRequest";
var isSend = true;

function PriceUpdateRequest() {
    this.product_prices = new Array();
};

function RegularPrice(amount, currency) {
    this.amount = amount.replace(",", ".");
    if (currency == undefined) {
        this.currency = "EUR";
    }
    else {
        this.currency = currency;
    }
}

function ProductPrice(ean, sales_channel_id, amount) {
    this.ean = ean;
    this.sales_channel_id = sales_channel_id;

    if(sales_channel_id == "7ce94f55-7a4d-4416-95c1-bf34193a47e8") {
        // La danimarca
        this.regular_price = new RegularPrice(amount, "DKK");
    }
    else if (sales_channel_id == "091dcbdd-7839-4f39-aa05-324eb4599df0") {
        // La svezia
        this.regular_price = new RegularPrice(amount, "SEK");
    }
    else if (sales_channel_id == "ca9d5f22-2a1b-4799-b3b7-83f47c191489") {
        this.regular_price = new RegularPrice(amount, "PLN");
    }
    else {
        this.regular_price = new RegularPrice(amount);
    }
    this.ignore_warnings = false;
}

function fileInfo(e){
    var file = e.target.files[0];
    if (file.name.split(".")[1].toUpperCase() != "CSV"){
        alert('File CSV non valido!');
        e.target.parentNode.reset();
        return;
    }
    else {
        document.getElementById('file_info').innerHTML = "<p>File Name: "+file.name + " | "+file.size+" Bytes.</p>";
        $('#sendForm').prop('disabled', false);
    }
}

var priceListUpdateRequest = undefined;

function handleFileSelect() {
//    $('#sendForm').prop('disabled', true);
//    var STATUS_ACCEPTED = "ACCEPTED";
//    // Funzione che aggiunge dell'HTML creando un child TD oppure TH
//    // type = "td" oppure "th"
//    var addColumn = function(innerHTML, tagType) {
//        var child = document.createElement(tagType);
//        child.innerHTML = innerHTML;
//        return child;
//    };
//
//    var file = document.getElementById("the_file").files[0];
//    var reader = new FileReader();
//    var link_reg = /(http:\/\/|https:\/\/)/i;
//    priceListUpdateRequest = new PriceUpdateRequest();
//    reader.onload = function(file) {
//        var rows = file.target.result.split(/[\r\n|\n]+/);
//
//        // Recupero le informazioni di invio dalle API
//        // Per ogni riga del CSV
//        for (var i = 1; i < rows.length; i++){
//            var arr = rows[i].split(';');
//            var productEan = arr[0];
//            var productPrice = arr[2];
//            if (productEan != '' && productPrice != '') {
//                // console.log(arr);
//                $("input:checked").each(function() {
//                    product = new ProductPrice(productEan, this.value, productPrice);
//                    priceListUpdateRequest.product_prices.push(product);
//                    if (priceListUpdateRequest.product_prices.length > 1000) {
//                        alert("Superato il limite di un unico invio. Impossibile inoltrare la richiesta a Zalando.");
//                    }
//                });
//            }
//        }
//        //TODO: Controllare che la combinazione ean e channelsID sia univoca
//        if (isSend) {
//            json = JSON.stringify(priceListUpdateRequest);
//            console.log("REQUEST: " + json);
//            var jqxhr = $.post(apiURLUpdate, json, function(data, textStatus, jqXHR) {
//                console.log("RESPONSE: " + data);
//                var result = JSON.parse(data);
//                // console.log(result);
//
//                var table = document.createElement('table');
//
//                var tr = document.createElement('tr');
//                tr.appendChild(addColumn("CODICE EAN", "th"));
//                tr.appendChild(addColumn("PAESE DI PUBBLICAZIONE", "th"));
//                tr.appendChild(addColumn("RISPOSTA", "th"));
//                table.appendChild(tr);
//
//                for (var i = 0; i < result.results.length; i++){
//                    var tr = document.createElement('tr');
//                    var row = result.results[i];
//                    //console.log(row);
//                    var code = row.code;
//                    var description = row.description;
//                    var productObj = row.product_price;
//                    var ean = productObj.ean;
//                    var sales_channel_id = productObj.sales_channel_id;
//                    var country = $(":checkbox[value='" + sales_channel_id + "']").prop("name");
//                    var status = row.status;
//
//                    //TODO: colorare in rosso o verse se la richiesta è accettata o rifiutata
//
//                    if (status != STATUS_ACCEPTED) {
//                        tr.appendChild(addColumn(ean, "td"));
//                        tr.appendChild(addColumn('<span title="' + sales_channel_id + '">' + country + '</span>', "td"));
//                        tr.appendChild(addColumn('<span title="' + description + '">' + status + '</span>', "td"));
//                        table.appendChild(tr);
//                    }
//                }
//
//                $("#resultInvio").append(table);
//                $("#resultInvio").show();
//                alert("Inviata richiesta di aggiornamento prezzo per prodotti: " + priceListUpdateRequest.product_prices.length);
//            }).fail(function(data) {
//                console.log(data);
//                alert("Errore di comunicazione con le API: ripetere l'operazione di invio. Se il problema persiste contattare il supporto tecnico.");
//            });
//        }
//    };
//    reader.readAsText(file);
    alert("Richiesta di download files");
}


document.getElementById('the_form').addEventListener('submit', handleFileSelect, false);
document.getElementById('the_file').addEventListener('change', fileInfo, false);