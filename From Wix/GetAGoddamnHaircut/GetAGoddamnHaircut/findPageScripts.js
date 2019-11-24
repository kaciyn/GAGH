import wixData from 'wix-data';

$w.onReady(function() {
    $w("#map").onMessage((event) => {
        $w("#placeName").value = event.data.split(";")[0];
        $w("#placeLocation").value = event.data.split(";")[1];
        $w("#placeID").value = event.data.split(";")[2];

    });

    $w("#reviewsDataset").onBeforeSave(() => {
        $w("#reviewsDataset").setFieldValue('title', $w("#placeName").value);
        $w("#reviewsDataset").setFieldValue('name', $w("#placeLocation").value);
        $w("#reviewsDataset").setFieldValue('address', $w("#placeID").value);
    });
});

export function btnAddPronouns_click(event) {

    $w("#pronounsDataset").refresh;
    $w("#pronounsDataset").refresh;

    console.log("Done refreshing the dataset");

    $w("#btnAddPronouns").label = "Added!";
}
