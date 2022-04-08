let cart = [];
const add_btn = document.getElementsByClassName("add-btn");
const remove_btn = document.getElementsByClassName("remove-btn");
const update_cart = document.getElementById("update-cart");

for (let i = 0; i < add_btn.length; i++) {
    add_btn[i].addEventListener('click', addItem(document.getElementsByClassName("item-name")[i]));
}
for (let i = 0; i < remove_btn.length; i++) {
    remove_btn[i].addEventListener('click', removeItem(document.getElementsByClassName("item-name")[i]));
}

update_cart.addEventListener("click", () => {
    let p = document.getElementById("cartItem");
    let text = "[";
    if (cart.length > 0)
        p.innerHTML = text + cart + "]";
    else
        p.innerHTML = cart;
});

function checkout() {
    if (cart.length > 0) {
        fetch('/checkoutCart', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'cart': cart,
            })
        }).then(response => response.json())
            .then(data => {
                console.log(data);
                // cart = [];
            });
        alert("Checkout Successful");
    } else {
        alert("cart is empty at the moment");
    }
}

function addItem(item) {
    cart.push(item);
    console.log(item);
}

function removeItem(item) {
    let indexRemoved = cart.indexOf(item);
    if (item === cart[indexRemoved])
        cart.splice(indexRemoved, 1);
}

