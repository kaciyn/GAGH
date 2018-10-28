import wixData from 'wix-data';

$w.onReady(function () {
    //TODO: write your page related code here...

});

export function btnAddPronouns_click(event) {
    $w("#pronounsDataset").refresh()
        .then( () => {
            console.log("Done refreshing the dataset");
        } );
    $w("#btnAddPronouns").label = "Added!";}
//might be able to do this with a save instead

export function btnSubmit_click(event) {
    var mapsFrame = $w("#map");
    var mapsWindow = mapsFrame.contentWindow;

    var placeName = mapsWindow.getElementById("place-name").textContent;
    var placeId=mapsWindow.getElementById("place-id").textContent;
    var placeAddress=mapsWindow.getElementById("place-address").textContent;

    let toSave = {
        "title":         mapsWindow.getElementById("place-id").textContent,
        "reviewerLocation":   $w("inputLocation"),
        "reviewerName":    $w("inputName"),
        "review":    $w("inputReview"),
        "name":    mapsWindow.getElementById("place-id").textContent,
        "avoid":    $w("checkAvoid"),
        "dateVisited":    $w("datePicker"),
//        "last_name":    "Doe",
//        "last_name":    "Doe",
//        "last_name":    "Doe",
//
//        "last_name":    "Doe"
    };

    wixData.save("Reviews", toSave)
        .then( (results) => {
            let item = results; //see item below
        } )
        .catch( (err) => {
            let errorMsg = err;
        } );
}



