let updateBtn = document.getElementsByClassName('update-cart');

for ( i = 0; i < updateBtn.length; i++ ) {
    updateBtn[i].addEventListener('click', function() {
        let qty = null;
        if( document.getElementsByName('product-qty').length > 0 ) {
            qty = document.getElementsByName('product-qty')[0].value
        }
        const data = {
            'productId': this.dataset.product,
            'action': this.dataset.action,
            'quantity': qty
        }

        if ( user === 'AnonymousUser') {
            addCookieItem( data );
        }else {
            updateUserOrder( data );
        }
    })
}

const updateUserOrder = ( data ) => {
    const url = '/store/update_item/';

    fetch( url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({...data})
    })
    .then( res => {
        return res.json()
    })
    .then( data => {
        location.reload()
    })
}

const addCookieItem = ( data ) => {

    productId = data["productId"];
    quantity = data["quantity"];

    if ( action == 'add' ) {
        if ( cart[productId] == undefined) {
            cart[productId] = { 'quantity': quantity};
            
        }else {
            cart[productId]['quantity'] += quantity;
        }
    }

    if ( action == 'remove' ) {
        if ( cart[productId] != undefined) {
            cart[productId]['quantity'] -= quantity;

            if( cart[productId]['quantity'] <= 0 ) {
                delete cart[productId];
            }
        }
    }
    document.cookie = `cart=${JSON.stringify( cart )};domain=;path=/`;
    location.reload();
}
