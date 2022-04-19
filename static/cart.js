let cart = []; let posts_id = [];
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
                'posts_id': posts_id,
            })
        })
            .then(response => response.json())
            .then(data => {
                console.log("Here: ", response.json());
                cart = [];
            });
        alert("Checkout Successful");
        window.location.reload();
    } else {
        alert("cart is empty at the moment");
    }
}

function addItem(item, id) {
    if (item !== "") {
        cart.push(item);
        posts_id.push(id);
    }
    console.log(posts_id);
}

function removeItem(item, id) {
    let indexRemoved = cart.indexOf(item);
    let indexRemovedId = posts_id.indexOf(id);
    if (item === cart[indexRemoved])
        cart.splice(indexRemoved, 1);

    if (id === posts_id[indexRemovedId])
        posts_id.splice(indexRemovedId, 1);
    console.log(posts_id);
}

