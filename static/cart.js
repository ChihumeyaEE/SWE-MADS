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
    p.innerHTML = text + cart + "]";
    // for (let i = 0; i < cart.length; i++) {
    //     p.innerHTML = cart[i];
    // }
    // document.getElementById("cartItem").innerHTML = cart + "<br>";
});

function displayCart() {
    for (let i = 0; i < cart.length; i++) {
        let ul = document.getElementById("cartItem");
        let li = document.createElement("li");
        li.appendChild(document.createTextNode(cart[i]));
        ul.appendChild(li);
    }

}

function addItem(item) {
    cart.push(item);
}

function removeItem(item) {
    let indexRemoved = cart.indexOf(item);
    if (item === cart[indexRemoved])
        cart.splice(indexRemoved, 1);
}

