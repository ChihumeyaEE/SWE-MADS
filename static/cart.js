let cart = ["banana", "apple", "orange"];
function displayCart() {
    for (let i = 0; i < cart.length; i++) {
        let ul = document.getElementById("cartItem");
        let li = document.createElement("li");
        li.appendChild(document.createTextNode(cart[i]));
        ul.appendChild(li);
    }
}

function addItem(item) {
    cart.push(item)
}

function removeItem(item) {
    let indexRemoved = cart.indexOf(item);
    cart.splice(indexRemoved, 1);
}

