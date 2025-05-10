import { useState, useEffect } from "react";
import toast, { Toaster } from "react-hot-toast";

export default function Market() {
  const [role, setRole] = useState("consumer");
  const [activeTab, setActiveTab] = useState("productList");

  // Common data
  const [products, setProducts] = useState([
    {
      name: "Wheat",
      price: "50",
      category: "Grains",
      image: "https://5.imimg.com/data5/ST/QW/MY-38700875/fresh-wheat-crop.jpg",
    },
    {
      name: "Rice",
      price: "60",
      category: "Grains",
      image:
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYCb250Mk3GllPRucE3aHi662xZCBInSjDuw&s",
    },
    {
      name: "Tomato",
      price: "30",
      category: "Vegetables",
      image:
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRp2-wGkyyHymPzZyVJp0RCrZoq8CWR0dsAlg&s",
    },
    {
      name: "Potato",
      price: "25",
      category: "Vegetables",
      image:
        "https://images.unsplash.com/photo-1518977676601-b53f82aba655?fm=jpg&q=60&w=3000",
    },
    {
      name: "Carrot",
      price: "40",
      category: "Vegetables",
      image: "https://www.hhs1.com/hubfs/carrots%20on%20wood-1.jpg",
    },
  ]);

  const [filterCategory, setFilterCategory] = useState("All");

  // Seller-specific
  const [orders] = useState([
    { id: 1, product: "Wheat", customer: "John Doe", status: "Pending" },
    { id: 2, product: "Rice", customer: "Jane Smith", status: "Pending" },
  ]);
  const [form, setForm] = useState({
    name: "",
    price: "",
    category: "",
    photo: null,
    preview: null,
  });

  // Consumer-specific
  const [consumerOrders, setConsumerOrders] = useState(() => {
    const saved = localStorage.getItem("orders");
    return saved ? JSON.parse(saved) : [];
  });
  const [selectedQuantities, setSelectedQuantities] = useState({});

  useEffect(() => {
    localStorage.setItem("orders", JSON.stringify(consumerOrders));
  }, [consumerOrders]);

  const handleInputChange = (e) => {
    const { name, value, files } = e.target;
    if (files) {
      const file = files[0];
      setForm({
        ...form,
        photo: file,
        preview: URL.createObjectURL(file),
      });
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleAddProduct = () => {
    if (form.name && form.price && form.category) {
      const newProduct = {
        name: form.name,
        price: form.price,
        category: form.category,
        image: form.preview,
      };
      setProducts([...products, newProduct]);
      setForm({
        name: "",
        price: "",
        category: "",
        photo: null,
        preview: null,
      });
      toast.success("✅ Product added successfully!");
    }
  };

  const handleOrder = (product, quantity) => {
    const newOrder = {
      id: Date.now(),
      product: product.name,
      image: product.image,
      quantity,
      status: "Placed",
      time: new Date().toISOString(),
    };
    setConsumerOrders([...consumerOrders, newOrder]);
    toast.success("Item added to cart");
  };

  const handleCancelOrder = (orderId) => {
    const now = new Date();
    const order = consumerOrders.find((o) => o.id === orderId);
    const orderTime = new Date(order.time);
    const hoursDiff = (now - orderTime) / (1000 * 60 * 60);
    if (hoursDiff <= 3) {
      setConsumerOrders(consumerOrders.filter((order) => order.id !== orderId));
    } else {
      toast.error("Cannot cancel after 3 hours");
    }
  };

  const filteredProducts =
    filterCategory === "All"
      ? products
      : products.filter((p) => p.category === filterCategory);

  const renderSellerTabs = () => (
    <>
      <button
        onClick={() => setActiveTab("addProduct")}
        className={`w-full p-2 rounded ${
          activeTab === "addProduct"
            ? "bg-green-200 font-bold"
            : "hover:bg-green-100"
        }`}
      >
        Add Product
      </button>
      <button
        onClick={() => setActiveTab("productList")}
        className={`w-full p-2 rounded ${
          activeTab === "productList"
            ? "bg-green-200 font-bold"
            : "hover:bg-green-100"
        }`}
      >
        Product List
      </button>
      <button
        onClick={() => setActiveTab("orders")}
        className={`w-full p-2 rounded ${
          activeTab === "orders"
            ? "bg-green-200 font-bold"
            : "hover:bg-green-100"
        }`}
      >
        Orders
      </button>
    </>
  );

  const renderConsumerTabs = () => (
    <>
      <button
        onClick={() => setActiveTab("productList")}
        className={`w-full p-2 rounded ${
          activeTab === "productList"
            ? "bg-green-200 font-bold"
            : "hover:bg-green-100"
        }`}
      >
        Browse Products
      </button>
      <button
        onClick={() => setActiveTab("orders")}
        className={`w-full p-2 rounded ${
          activeTab === "orders"
            ? "bg-green-200 font-bold"
            : "hover:bg-green-100"
        }`}
      >
        My Orders
      </button>
    </>
  );

  const renderContent = () => {
    if (role === "seller") {
      switch (activeTab) {
        case "addProduct":
          return (
            <div className="space-y-6">
              <label className="flex flex-col items-center justify-center w-32 h-32 border-2 border-dashed border-gray-400 rounded cursor-pointer hover:bg-green-100 relative">
                <span className="text-sm text-gray-600">Upload</span>
                <input
                  type="file"
                  name="photo"
                  accept="image/*"
                  onChange={handleInputChange}
                  className="hidden"
                />
                {form.preview && (
                  <img
                    src={form.preview}
                    className="absolute inset-0 w-full h-full object-cover rounded"
                  />
                )}
              </label>
              <input
                type="text"
                name="name"
                value={form.name}
                onChange={handleInputChange}
                placeholder="Product Name"
                className="border p-2 w-full rounded"
              />
              <input
                type="text"
                name="price"
                value={form.price}
                onChange={handleInputChange}
                placeholder="Price (₹)"
                className="border p-2 w-full rounded"
              />
              <input
                type="text"
                name="category"
                value={form.category}
                onChange={handleInputChange}
                placeholder="Category"
                className="border p-2 w-full rounded"
              />
              <button
                onClick={handleAddProduct}
                className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
              >
                Add Product
              </button>
            </div>
          );
        case "productList":
          return (
            <>
              <div className="mb-4">
                <label className="mr-2 font-semibold">
                  Filter by Category:
                </label>
                <select
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  className="p-2 border rounded"
                >
                  <option value="All">All</option>
                  <option value="Vegetables">Vegetables</option>
                  <option value="Grains">Grains</option>
                </select>
              </div>
              {filteredProducts.length === 0 ? (
                <p>No products found.</p>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                  {filteredProducts.map((product, idx) => (
                    <div
                      key={idx}
                      className="border rounded shadow bg-green-50 p-4"
                    >
                      {product.image && (
                        <img
                          src={product.image}
                          className="h-40 w-full object-cover mb-2 rounded"
                        />
                      )}
                      <h3 className="text-lg font-semibold">{product.name}</h3>
                      <p>
                        <strong>Price:</strong> ₹{product.price}
                      </p>
                      <p>
                        <strong>Category:</strong> {product.category}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </>
          );
        case "orders":
          return orders.length === 0 ? (
            <p>No pending orders.</p>
          ) : (
            <div className="space-y-2">
              {orders.map((order) => (
                <div key={order.id} className="border p-4 rounded bg-green-50">
                  <p>
                    <strong>Product:</strong> {order.product}
                  </p>
                  <p>
                    <strong>Customer:</strong> {order.customer}
                  </p>
                  <p>
                    <strong>Status:</strong> {order.status}
                  </p>
                </div>
              ))}
            </div>
          );
      }
    }

    if (role === "consumer") {
      switch (activeTab) {
        case "productList":
          return (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {products.map((product, index) => (
                <div
                  key={index}
                  className="border p-4 rounded bg-green-50 shadow"
                >
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-40 object-cover rounded mb-2"
                  />
                  <p>
                    <strong>{product.name}</strong>
                  </p>
                  <p>₹{product.price}/kg</p>
                  <p>{product.category}</p>
                  <select
                    value={selectedQuantities[product.name] || ""}
                    onChange={(e) =>
                      setSelectedQuantities({
                        ...selectedQuantities,
                        [product.name]: e.target.value,
                      })
                    }
                    className="mt-2 w-full p-1 border rounded"
                  >
                    <option value="">Select Quantity</option>
                    <option value="0.5kg">0.5kg</option>
                    <option value="1kg">1kg</option>
                    <option value="2kg">2kg</option>
                  </select>
                  <button
                    onClick={() =>
                      handleOrder(product, selectedQuantities[product.name])
                    }
                    disabled={!selectedQuantities[product.name]}
                    className="mt-2 w-full bg-green-600 text-white py-1 rounded hover:bg-green-700 disabled:bg-green-300"
                  >
                    Order
                  </button>
                </div>
              ))}
            </div>
          );
        case "orders":
          return consumerOrders.length === 0 ? (
            <p>No orders placed yet.</p>
          ) : (
            <div className="space-y-4">
              {consumerOrders.map((order) => (
                <div
                  key={order.id}
                  className="border p-4 rounded bg-green-50 shadow"
                >
                  <div className="flex items-center space-x-4">
                    <img
                      src={order.image}
                      className="w-24 h-24 object-cover rounded"
                    />
                    <div>
                      <p>
                        <strong>{order.product}</strong> - {order.quantity}
                      </p>
                      <p>Status: {order.status}</p>
                      <p className="text-xs italic text-gray-500">
                        Cancelable within 3 hours
                      </p>
                      {order.status === "Placed" && (
                        <button
                          onClick={() => handleCancelOrder(order.id)}
                          className="mt-1 bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
                        >
                          Cancel
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          );
      }
    }

    return null;
  };

  return (
    <div className="flex flex-col h-screen bg-white">
      <Toaster position="bottom-center" />

      <header className="bg-green-700 text-white p-4 text-2xl font-bold text-center">
        Krishi Mitra Dashboard
      </header>

      <div className="bg-green-100 text-green-800 p-2 text-center font-semibold">
        🌾 Flash News: Support prices increased for Rabi crops!
      </div>

      <div className="p-4 bg-green-50 border-b flex justify-end items-center">
        <label className="mr-2 font-semibold">Switch Role:</label>
        <select
          value={role}
          onChange={(e) => {
            setRole(e.target.value);
            setActiveTab("productList");
          }}
          className="p-2 border rounded"
        >
          <option value="consumer">Consumer</option>
          <option value="seller">Seller</option>
        </select>
      </div>

      <div className="flex flex-1">
        <aside className="w-64 bg-green-50 p-4 border-r">
          <nav className="space-y-4">
            {role === "seller" ? renderSellerTabs() : renderConsumerTabs()}
          </nav>
        </aside>

        <main className="flex-1 p-6">{renderContent()}</main>
      </div>
    </div>
  );
}
