import React, { useEffect, useState } from "react";

function Cart() {
  const [cartItems, setCartItems] = useState([]);
  const [total, setTotal] = useState(0);

  // Cargar los items del carrito
  useEffect(() => {
    fetch("http://localhost:5000/cart")
      .then(res => res.json())
      .then(data => setCartItems(data));

    // Cargar el total
    fetch("http://localhost:5000/cart/total")
      .then(res => res.json())
      .then(data => setTotal(data.total));
  }, []);

 // Agregar producto (ejemplo: id fijo)
 const addToCart = (productId) => {
  fetch("http://localhost:5000/cart/items", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId, quantity: 1 })
  })
    .then(res => res.json())
    .then(() => {
      refreshCart();
    });
};

// Eliminar producto
const removeFromCart = (productId) => {
  fetch(`http://localhost:5000/cart/items/${productId}`, {
    method: "DELETE"
  })
    .then(res => res.json())
    .then(() => {
      refreshCart();
    });
};

// Refrescar carrito y total
const refreshCart = () => {
  fetch("http://localhost:5000/cart")
    .then(res => res.json())
    .then(data => setCartItems(data));

  fetch("http://localhost:5000/cart/total")
    .then(res => res.json())
    .then(data => setTotal(data.total));
};

return (
  <div>
    <h1>Carrito</h1>
    <ul>
      {cartItems.map(item => (
        <li key={item.product_id}>
          {item.name} - ${item.price} x {item.quantity}
          <button onClick={() => removeFromCart(item.product_id)}>Eliminar</button>
        </li>
      ))}
    </ul>
    <h2>Total: ${total}</h2>

    {/* Botón de prueba para agregar producto con id=1 */}
    <button onClick={() => addToCart(1)}>Agregar producto 1</button>
  </div>
);
}

export default Cart;