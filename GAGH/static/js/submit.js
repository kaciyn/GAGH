$(function () {
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        endDate: '+0d',
        autoclose: true,
        clearBtn: true,
        todayHighlight: true

    });
});


//checkbox hack
if (document.getElementById("gender_remarks").checked) {
    document.getElementById('gender_remarksHidden').disabled = true;
}
if (document.getElementById("gender_charged").checked) {
    document.getElementById('gender_chargedHidden').disabled = true;
}
if (document.getElementById("unsafe").checked) {
    document.getElementById('unsafeHidden').disabled = true;
}})

//receives currently shown gmaps place & parses into place info
window.addEventListener("message", receiveMessage, false);
function receiveMessage(event) {
    //if (event.origin !== "http://localhost:5000")
    //    return;
    //you definitely need to check for the origin here but how to pass in dynamically? who knows!

    $document.getElementsByName('map')[0].value = event.data.split(";")[0];
    $document.getElementsByName('map')[0].value = event.data.split(";")[1];
    $document.getElementsByName('map')[0] = event.data.split(";")[2];
};