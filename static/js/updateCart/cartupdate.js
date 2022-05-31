$(document).ready(function () {

    $('.increment-btn').click(function (e) { 
        e.preventDefault();

        var inc_value = $(this).closest('.cart_data').find('#qty-input').val();
        var value = parseInt(inc_value,10);
        value = isNaN(value) ? 0 : value;
        if ( value < 10){
            value ++;
            $(this).closest('.cart_data').find('#qty-input').val(value);
        }
        
    });

    $('.decrement-btn').click(function (e) { 
        e.preventDefault();
        var dcr_value = $(this).closest('.cart_data').find('#qty-input').val();
        var value =parseInt(dcr_value,10);
        value =  isNaN(value) ? 0 :value;
        if(value>1){
            value--;
            $(this).closest('.cart_data').find('#qty-input').val(value);
        }
    });

    $('#changeQt').click(function (e) { 
        e.preventDefault();
        var product_id = $(this).closest('.cart_data').find('#product_id').val();
        var quantity = $(this).closest('.cart_data').find('#qty_input').val();
        var token = $('input[name= csrfmiddlewaretoken]').val();
        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id':product_id,
                'quantity':quantity,
                csrfmiddlewaretoken :token
            },
            success: function (response) {
                console.log(response)
                swal(response.status)
            }
        });
    });
});