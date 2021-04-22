let updateBtn = document.getElementsByClassName('update-cart');

for ( i = 0; i < updateBtn.length; i++ ) {
    updateBtn[i].addEventListener('click', function() {
        const productId = this.dataset.product;
        const action = this.dataset.action
        if ( user === 'AnonymousUser') {
            addCookieItem( productId, action );
        }else {
            updateUserOrder( productId, action );

        }
    })
}

const updateUserOrder = ( productId, action ) => {
    const url = '/update_item/';

    fetch( url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        })
    })
    .then( res => {
        return res.json()
    })
    .then( data => {
        location.reload()
    })
}

const addCookieItem = ( productId, action ) => {
    if ( action == 'add' ) {
        if ( cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 };
            
        }else {
            cart[productId]['quantity'] += 1;
        }
    }

    if ( action == 'remove' ) {
        if ( cart[productId] != undefined) {
            cart[productId]['quantity'] -= 1;

            if( cart[productId]['quantity'] <= 0 ) {
                delete cart[productId];
            }
        }
    }
    document.cookie = `cart=${JSON.stringify( cart )};domain=;path=/`;
    location.reload();
}
