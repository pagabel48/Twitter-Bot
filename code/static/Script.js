var stripe = Stripe(checkout_session_id);

console.log("File has been read")

const button = document.querySelector('#checkout-button')

button.addEventListener('click', event => {
    stripe.redirectToCheckout({
        sessionId: checkout_session_id
    }).then(function (result){});
})