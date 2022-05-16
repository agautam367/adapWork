var lat, lon;

window.addEventListener('load', () => {
    
    const searchText = sessionStorage.getItem('searchText');
    const category = sessionStorage.getItem('category');
    const proximity = sessionStorage.getItem('proximity');
    const price = sessionStorage.getItem('price');
    const ucl = sessionStorage.getItem('currentLoc');

    getLocation();

    const lat = sessionStorage.getItem('lat');
    const lon = sessionStorage.getItem('lon');

    console.log("searchText: "+searchText);
    console.log("category: "+category);
    console.log("proximity: "+proximity);
    console.log("price: "+price);
    console.log("Lat: "+lat);
    console.log("Lon: "+lon); 
    console.log("UCL: "+ucl); 

    var body = {};
    var params = {
        'currentLong': lon,
        'openNow': null,
        'minPrice': 0,
        'textLocation': searchText,
        'placeType': category,
        'radius': proximity,
        'rankBy': null,
        'useCurrentLocation': null,
        'currentLat': lat,
        'maxPrice': price,
        'numResults': null,
        'useCurrentLocation': ucl,
        'username': 'user'
    };
        
    var additionalParams = {
        headers: {
            'Content-Type': "application/json",
        },
    };

    searchGet(params,body,additionalParams);

})

function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else { 
      x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    lat = position.coords.latitude;
    lon = position.coords.longitude;
    
    sessionStorage.setItem('lat', lat);
    sessionStorage.setItem('lon', lon);
}

function searchGet(params, body, additionalParams){
    var apigClient = apigClientFactory.newClient({});
    // console.log("abc")
    apigClient.placesNearbySearchGet(params, {}, additionalParams)
        .then(function(result) {
            console.log("Result : ", result);

            places = result["data"];
            console.log("search results : ", places);

            console.log("Length: "+ places.length);

            let content = '';

            places.forEach(p => {
                // var ref = p['photos'][0]['photo_reference'];
                var url = p['image_url'];
                console.log(url)
                var address = p['vicinity'];
                var rating = p['rating'];


                content += `
                <div class="card mb-3">
                    <div class="row no-gutters">
                        <div class="col-md-4">
                            <img class="imgThumbnail" src=${p['image_url']} class="card-img" alt="...">
                        </div>
                        <div class="col-md-8">
                            <div class="card-body">
                                <h5 class="card-title">${p['name']}</h5>
                                <p class="card-text">${p['formatted_address']}</p>
                                <p class="card-text"><small class="text-muted">${rating}/5.0</small></p>
                                <button type="button" class="btn btn-primary" onclick="getDetails('${p['place_id']}')">More Details ></button>
                            </div>
                        </div>
                    </div>
                </div>`
            });
            document.querySelector("#places-result").innerHTML = content;
            if(places.length == 0){
                // Display that no places are found
            }


        }).catch(function(result) {
            console.log(result);
        });

}



function getDetails(place_id){
    sessionStorage.setItem('place_id', place_id);

    location.href = 'details.html';
}
