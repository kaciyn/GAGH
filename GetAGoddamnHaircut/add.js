// For full API documentation, including code examples, visit http://wix.to/94BuAAs

$w.onReady(function () {
    //TODO: write your page related code here...

});

 

export function button2_click(event) {
    $w("#myDataset").refresh()
  .then( () => {
    console.log("Done refreshing the dataset");
  } ); 
}