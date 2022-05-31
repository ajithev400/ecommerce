$(document).ready(function () {
    $('.addtocart').click(function (e) { 
        e.preventDefault();
        
        var product_id= $(this).closest('').find('.variant_id').val()
        var size = $(this).closest('.btn-addcart-product-detail').find('.variant_size').val()
        var token = $('input[name= csrfmiddlewaretoken]').val();
        console.log(product_id)
        console.log(size)

        $.ajax({
            type: "POST",
            url: "/add_cart",
            data: {
                'product_id':product_id,
                'size':size,
                csrfmiddlewaretoken :token
            },
            success: function (response) {
                console.log(response)
            }
        });
    });

});