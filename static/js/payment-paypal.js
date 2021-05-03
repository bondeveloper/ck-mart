
paypal.Buttons({
    style: {
        size: 'small',
        color: 'blue',
        shape: 'rect'
    },

    // Set up the transaction
    createOrder: function(data, actions) {
        console.log( data );
        console.log( actions );
        return actions.order.create({
            purchase_units: [{
                amount: {
                    value: parseFloat( total ).toFixed(2)
                }
            }]
        });
    },

    // Finalize the transaction
    onApprove: function(data, actions) {
        return actions.order.capture().then(function(details) {
            submitFormData();
        });
    }


}).render('#paypal-button-container');