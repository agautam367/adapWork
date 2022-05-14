function search(){
    var x = document.getElementById("inputText").value;
    console.log("Search Text: " + x);

    var body = {};
    var params = {
        q: x
    };
        
    var additionalParams = {
        headers: {
            'Content-Type': "application/json",
        },
    };

    searchGet(params,body,additionalParams);
}

function searchGet(params, body, additionalParams){
    var apigClient = apigClientFactory.newClient({});
    console.log("abc")
    apigClient.placesNearbySearchGet(params, {'currentLong':0}, additionalParams)
        .then(function(result) {
            console.log("Result : ", result);

            paths = result["data"];
            console.log("search results : ", paths);

            // var i;
            // if (paths.length > 0){
            //     photosDiv.innerHTML = "<ol>";

            //     for (i = 0; i < paths.length; i++) {
            //         photosDiv.innerHTML += '<li>' + paths[i]["name"] + ", " + paths[i]["vicinity"] + '</li>'
            //     }
            //     photosDiv.innerHTML += "</ol>";
            // }
            // else{
            //     photosDiv.innerHTML += '<h1>NO places found!</h1>';
            // }

        }).catch(function(result) {
            console.log(result);
        });
}
