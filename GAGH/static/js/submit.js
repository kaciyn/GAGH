$(function () {
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        endDate: '+0d',
        autoclose: true,
        clearBtn: true,
        todayHighlight: true,
        useCurrent: true

    });
});

$(document).ready(function () {
    //checkbox hack
    if (document.getElementById("gender_remarks").checked) {
        document.getElementById('gender_remarksHidden').disabled = true;
    }
    if (document.getElementById("gender_charged").checked) {
        document.getElementById('gender_chargedHidden').disabled = true;
    }
    if (document.getElementById("unsafe").checked) {
        document.getElementById('unsafeHidden').disabled = true;
    }
});

//receives currently shown gmaps place & parses into place info
$(document).ready(function () {
    window.addEventListener("message", receiveMessage, false);
})

function receiveMessage(event) {
    if (event.isTrusted == true) {
        if (event.data == "") {
            return;
        }
        console.log(event.data);

        var barbershop_data = event.data.split(";");
        var name = barbershop_data[0];
        var address = barbershop_data[1];
        var id = barbershop_data[2];

        console.log(id);
        console.log(name);
        console.log(address);

        document.getElementsByName('placeID')[0].value = id;
        document.getElementsByName('name')[0].value = name;
        document.getElementsByName('address')[0].value = address;
    }
    else {
        return
    }
};

$('.datepicker')
    .on('changeDate show', function (e) {
        // Revalidate the date when user change it

        $('#reviewForm').bootstrapValidator('revalidateField', 'endDate');
    });