
const BASE_URL = "http://127.0.0.1:5000/";
const defaultImg = "https://tinyurl.com/demo-cupcake";
const $addForm = $('#new-cupcake-form');

//renders cupcake json data to html 
function cupcakeToHtml(cupcake){
    const cupcakeHtml = `<div data.id="${cupcake.id}" class="text-center"><b>Flavor: ${cupcake.flavor} - Size: ${cupcake.size}  -  Rating: ${cupcake.rating}</b><div><img class="rounded mx-auto d-block"
    src="${cupcake.image}"></div></div>`;
    return cupcakeHtml;
}

//shows the list of cupcakes 
async function showCupcakes(){
    const response = await axios.get(`${BASE_URL}/api/cupcakes`);

    for(cupcake of response.data.cupcakes){
        $('#cupcake-list').append($(cupcakeToHtml(cupcake)))
    };
}

//handles the add new cupcake form
async function handleNewCupcake(e){
    e.preventDefault();

    // obtain user input and create cupcake
    let flavor = $('#flavor-input').val();
    let size = $('#size-input').val();
    let rating = $('#rating-input').val();
    let image = $('#image-input').val() || defaultImg;
    cupcake = {flavor, size, rating, image}

    //make post request to server
    resp = await axios.post(`${BASE_URL}/api/cupcakes`, cupcake);
    
    //appends the resp data to the page
    $('#cupcake-list').append($(cupcakeToHtml(cupcake)));

    //resets the form 
    $addForm.trigger("reset");
}

//add an event listener to the form
$addForm.on("submit", handleNewCupcake)


$(showCupcakes);
