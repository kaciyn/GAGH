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
if (document.getElementById("testName").checked) {
    document.getElementById('gender_remarksHidden').disabled = true;
}
if (document.getElementById("gender_charged").checked) {
    document.getElementById('gender_chargedHidden').disabled = true;
}
if (document.getElementById("unsafe").checked) {
    document.getElementById('unsafeHidden').disabled = true;
}
//receives currently shown gmaps place & parses into place info

$(document).ready(function () {
    $document.getElementsByName('map')[0].onMessage((event) => {
        if (event.origin !== "/submit/")
            return;

        $document.getElementsByName('map')[0].value = event.data.split(";")[0];
        $document.getElementsByName('map')[0].value = event.data.split(";")[1];
        $document.getElementsByName('map')[0] = event.data.split(";")[2];
    });
})

