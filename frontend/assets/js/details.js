window.addEventListener('load', () => {
    const pid = sessionStorage.getItem('place_id');
    console.log("CONOSLE: "+pid);

    var body = {};
    var params = {
        'placeId': pid
    };
        
    var additionalParams = {
        headers: {
            'Content-Type': "application/json",
        },
    };

    getPlaceDetails(params,body,additionalParams);

})


function getPlaceDetails(params, body, additionalParams){
    var apigClient = apigClientFactory.newClient({});

    apigClient.placedetailGet(params, {}, additionalParams)
        .then(function(result) {
            console.log("Result : ", result);

            details = result["data"];
            data = result['data']['result'];
            console.log("Details : ", data);
            let content = '';


            let imgPrefix = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=";
            let imgSuffix = "&key=AIzaSyCzSwAomFg7IMtFEENllPtvpld7cfJir50";
            let header = data['name'] + " | " + data['rating']+"/5";
            let mapURL = data['url'];
            
            content = `
            <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
            <div class="carousel-inner">
                <div class="carousel-item active">
                    <img style="filter: blur(10px);
                    -webkit-filter: blur(10px);" class="d-block w-100" src=${imgPrefix}+${data['photos'][2]['photo_reference']}+${imgSuffix} alt="Second slide">
                    <div class="container">
                        <h1>${header}</h1>
                        <p>${data['formatted_address']}</p>
                        <p id="price"></p>
                        <a type="button" class="btn btn-success my-2 my-sm-0" href='${mapURL}')">Get Directions</a>
                        <button type="button" class="btn btn-success my-2 my-sm-0">Mark interested</button>
                    </div>
                </div>
    
                <div class="carousel-item">
                    <div class="container">
                        <h1>CAFE Name 2</h1>
                        <p>The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum".</p>
                        <a type="button" class="btn btn-success my-2 my-sm-0" href="${mapURL}">Get Directions</a>
                        <button type="button" class="btn btn-success my-2 my-sm-0">Mark interested</button>
                    </div>
                </div>
            </div>
        </div>
            `
            let overviewContent = `
            <div class="row border g-0 rounded shadow-sm">
                    <div class="col p-4">
                        <h3>Overview</h3>
                        <p>
                        ABCDEFGHIJK.
                        </p>
                    </div>
                </div>
            `

            let photosContent = `
            <div class="row border g-0 rounded shadow-sm">
                    <div class="col p-4">
                        <h3>Photos</h3>
                        <p>
                        ABCDEFGHIJK.
                        </p>
                        <div class="banner-section" id="img-container" style="padding: 1%;">
                            <p id="displaytext"></p>
                        </div>
                    </div>
                </div>
            `

            let reviewsContent = `
            <div class="row border g-0 rounded shadow-sm">
                    <div class="col p-4">
                        <h3>Reviews</h3>
                        <p>
                        ABCDEFGHIJK.
                        </p>
                    </div>
                </div>
            `

            let contactContent = `
            <div class="row border g-0 rounded shadow-sm">
                    <div class="col p-4">
                        <h3>Contact</h3>
                        <p>
                        ABCDEFGHIJK.
                        </p>
                    </div>
                </div>
            `

            var photos = data['photos'];

            photos.forEach(p => {
                var ref = p['photo_reference'];
                var url =  "https://maps.googleapis.com/maps/api/place/photo?maxwidth=200&photo_reference="+ref+"&key=AIzaSyCzSwAomFg7IMtFEENllPtvpld7cfJir50"
                var img = new Image();
                img.src = url;

                // console.log(${url}');

                document.getElementById("img-container").appendChild(img);
                
            });


            document.querySelector("#infoTile").innerHTML = content;
            if(data['price_level'] === 1){
                $("#price").text("Cost for 2: $ (approx.)");
            } 
            else if (data['price_level'] === 2){
                $("#price").text("Cost for 2: $$ (approx.)");
            }
            else if (data['price_level'] === 3){
                $("#price").text("Cost for 2: $$$ (approx.)");
            }
            else if (data['price_level'] === 4){
                $("#price").text("Cost for 2: $$$$ (approx.)");
            } 

            document.querySelector("#overviewContent").innerHTML = overviewContent;
            document.querySelector("#reviewsContent").innerHTML = reviewsContent;
            document.querySelector("#photosContent").innerHTML = photosContent;
            document.querySelector("#contactContent").innerHTML = contactContent;


        }).catch(function(result) {
            console.log(result);
        });

}

// function redirect(url){
//     console.log("URL");
//     location.href = url;
// }