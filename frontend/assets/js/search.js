function search(){
    var searchText = document.getElementById("inputText").value;
    var proximity = $('#proxSelect').val() * 1609 ;
    var price = $('#price').val();
    var category = $("#catSelect option:selected").text();

    if(category === 'Category'){
        category = "Bar";
    }

    if(isNaN(proximity)){
        proximity = 1000;
    }

    if(price === 'Price'){
        price = 4;
    }
    console.log("searchText: " + searchText);
    console.log("category: " + category);
    console.log("proximity: " + proximity);
    console.log("price: " + price);

    sessionStorage.setItem('searchText', searchText);
    sessionStorage.setItem('category', category);
    sessionStorage.setItem('proximity', proximity);
    sessionStorage.setItem('price', price);
    sessionStorage.setItem('currentLoc', "false");


    location.href = 'results.html';
}

function searchNearme(){
    var searchText = "";
    var proximity = $('#proxSelect').val() * 1609 ;
    var price = $('#price').val();
    var category = $("#catSelect option:selected").text();

    if(category === 'Category'){
        category = "Bar";
    }

    if(isNaN(proximity)){
        proximity = 1000;
    }

    if(price === 'Price'){
        price = 4;
    }
    // console.log("searchText: " + searchText);
    console.log("category: " + category);
    console.log("proximity: " + proximity);
    console.log("price: " + price);

    sessionStorage.setItem('searchText', searchText);
    sessionStorage.setItem('category', category);
    sessionStorage.setItem('proximity', proximity);
    sessionStorage.setItem('price', price);
    sessionStorage.setItem('currentLoc', "true");


    location.href = 'results.html';
    // console.log("XXXXX");

}
