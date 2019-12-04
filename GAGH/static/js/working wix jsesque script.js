import wixData from 'wix-data';


//receives currently shown gmaps place & parses into place info
$w.onReady(function() {
$w("#map").onMessage((event) => {
    $w("#placeName").value = event.data.split(";")[0];
    $w("#placeLocation").value = event.data.split(";")[1];
    $w("#placeID").value = event.data.split(";")[2];
});

$w('#reviewsDataset').onBeforeSave(async () => {
//sets barbershopid 
    let barbershopId = await updateBarbershop();

//populates review from input
$w("#reviewsDataset").setFieldValue('title', $w("#placeName").value + ";" + Date.now());
$w("#reviewsDataset").setFieldValue('barbershop', barbershopId);
$w("#reviewsDataset").setFieldValue('dateLastVisited', $w("#datePicker").value);
$w("#reviewsDataset").setFieldValue('reviewTitle', $w("#reviewTitle").value);
$w("#reviewsDataset").setFieldValue('review', $w("#inputReview").value);
$w("#reviewsDataset").setFieldValue('haircutRating', $w("#haircutRating").value);
$w("#reviewsDataset").setFieldValue('anxietyRating', $w("#anxietyRating").value);
$w("#reviewsDataset").setFieldValue('friendlinessRating', $w("#friendlinessRating").value);
$w("#reviewsDataset").setFieldValue('priceRange', $w("#dropdownPrice").value);
$w("#reviewsDataset").setFieldValue('commentedOnGender', $w("#checkGenderComment").value);
$w("#reviewsDataset").setFieldValue('avoid', $w("#checkAvoid").value);
$w("#reviewsDataset").setFieldValue('reviewerName', $w("#inputName").value);
$w("#reviewsDataset").setFieldValue('reviewerPronouns', $w("#inputPronouns").value);
$w("#reviewsDataset").setFieldValue('reviewerLocation', $w("#inputLocation").value);
$w("#reviewsDataset").setFieldValue('approved', false);
});
});


//refreshes pronouns, twice bc once isn't enough, Apparently
export function btnAddPronouns_click(event) {
    $w("#pronounsDataset").refresh()
        .then(() => {});
    $w("#pronounsDataset").refresh()
        .then(() => {});

    $w("#btnAddPronouns").label = "Added!";
}


// Updates or creates barbershop 
async function updateBarbershop() {
    var placeID = $w("#placeID").value;

    var quality = parseInt($w('#haircutRating').value, 10);
    var anxietyRaw = parseInt($w('#anxietyRating').value, 10);
    var anxiety = 0;
    if (anxietyRaw === 1) {
        anxiety = 5
    } else if (anxietyRaw === 2) {
        anxiety = 4
    } else if (anxietyRaw === 3) {
        anxiety = 3
    } else if (anxietyRaw === 4) {
        anxiety = 2
    } else if (anxietyRaw === 5) {
        anxiety = 1
    }

    var friendliness = parseInt($w('#friendlinessRating').value, 10);

    var rating = quality + friendliness - anxiety + 1;

    var priceRange = parseInt($w('#dropdownPrice').value, 10);
    var genderComment = ($w('#checkGenderComment') === "true") ? 1 : 0;
    var avoid = ($w('#checkAvoid') === "true") ? 1 : 0;

//searches Barbershops dataset for existing bshop by place id
    let barbershopSearchResults = await wixData.query("Barbershops")
        .eq("placeId", placeID)
        .find();

    if (barbershopSearchResults.items.length > 0) {

        var barbershop = barbershopSearchResults.items[0]; //see item below
        console.log("found barbershop " + barbershop.title);
    } else {
        console.log("new barbershop");
    }

//if barbershop exists update values
    if (barbershop !== undefined && barbershop) {
        barbershop.quality += quality;
        barbershop.anxietyRating += anxiety;
        barbershop.friendliness += friendliness;

        barbershop.rating += rating;

        barbershop.priceRange += priceRange;

        barbershop.commentedOnGender += genderComment;
        barbershop.avoid += avoid;

        barbershop.reviewCount += 1;

await wixData.update('Barbershops', barbershop);
        return barbershop._id;
    }
    else{        
    barbershop = {
        placeId: placeID,
        title: $w("#placeName").value,
        address: $w("#placeLocation").value,

        quality: quality,
        anxietyRating: anxiety,
        friendliness: friendliness,

        rating: rating,

        priceRange: priceRange,

        commentedOnGender: genderComment,
        avoid: avoid,

        reviewCount: 1,
    };

    console.log("adding new barbershop: " + barbershop.title)

//wait for new barbershop to be added
await wixData.insert('Barbershops', barbershop);

let barbershopID;

//looks for new barbershop to make sure it was added
await wixData.query("Barbershops")
                .eq("placeId", $w("#placeID").value)
                .find().then((results)=>{
                    let newBarbershop=results.items[0];
                      barbershopID=newBarbershop._id;
                     console.log("barbershopid: "+barbershopID);
                })
                .catch((err)=>{
                    let errorMsg=err;
                    console.log(err);
                    })
                ;

    return barbershopID
    }
}