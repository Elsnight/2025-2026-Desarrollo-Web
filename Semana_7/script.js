const products = [
  {
    name: "Cuaderno A5",
    price: 3.5,
    description: "Cuaderno de notas con 80 hojas rayadas.",
  },
  {
    name: "Bolígrafo azul",
    price: 1.2,
    description: "Tinta de secado rápido para escritura diaria.",
  },
  {
    name: "USB 32GB",
    price: 9.99,
    description: "Almacenamiento portátil con conexión USB 3.0.",
  },
];

const list = document.getElementById("product-list");
const addButton = document.getElementById("add-product");
const form = document.getElementById("product-form");
const nameInput = document.getElementById("name-input");
const priceInput = document.getElementById("price-input");
const descriptionInput = document.getElementById("description-input");
let newProductCount = 1;

function formatPrice(value) {
  return `$${value.toFixed(2)}`;
}

function renderProducts() {
  list.innerHTML = "";

  products.forEach((product) => {
    const item = document.createElement("li");

    const name = document.createElement("span");
    name.className = "name";
    name.textContent = product.name;

    const price = document.createElement("span");
    price.className = "price";
    price.textContent = ` — ${formatPrice(product.price)}`;

    const description = document.createElement("span");
    description.className = "description";
    description.textContent = product.description;

    item.appendChild(name);
    item.appendChild(price);
    item.appendChild(description);
    list.appendChild(item);
  });
}

function addNewProduct() {
  const newProduct = {
    name: `Nuevo producto ${newProductCount}`,
    price: 5 + newProductCount,
    description: "Producto agregado dinámicamente.",
  };

  products.push(newProduct);
  newProductCount += 1;
  renderProducts();
}

addButton.addEventListener("click", addNewProduct);
form.addEventListener("submit", (event) => {
  event.preventDefault();

  const nameValue = nameInput.value.trim();
  const priceValue = parseFloat(priceInput.value);
  const descriptionValue = descriptionInput.value.trim();

  if (!nameValue || !descriptionValue || Number.isNaN(priceValue)) {
    return;
  }

  products.push({
    name: nameValue,
    price: priceValue,
    description: descriptionValue,
  });
  form.reset();
  renderProducts();
});
renderProducts();
