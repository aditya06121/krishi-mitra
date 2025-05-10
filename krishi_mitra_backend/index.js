import express from "express";
import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";
import cors from "cors";

// Setup __dirname for ES Modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());
app.use(express.json());

const PORT = 3000;
const DATA_FILE = path.join(__dirname, "users.json");

// Register route
app.post("/register", async (req, res) => {
  const { name, email, password, occupation, age, gender, phone } = req.body;

  if (!name || !email || !password || !occupation) {
    return res.status(400).json({ message: "All fields are required" });
  }

  let users = [];

  try {
    const data = await fs.readFile(DATA_FILE, "utf-8");
    users = JSON.parse(data);
  } catch (err) {
    if (err.code !== "ENOENT") {
      return res.status(500).json({ message: "Error reading user data" });
    }
  }

  if (users.some((user) => user.email === email)) {
    return res.status(409).json({ message: "Email already registered" });
  }

  users.push({ name, email, password, occupation, age, gender, phone });

  try {
    await fs.writeFile(DATA_FILE, JSON.stringify(users, null, 2));
    res.status(201).json({ message: "User registered successfully" });
  } catch (err) {
    res.status(500).json({ message: "Error saving data" });
  }
});

// Login route
app.post("/login", async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ message: "Email and password are required" });
  }

  let users = [];

  try {
    const data = await fs.readFile(DATA_FILE, "utf-8");
    users = JSON.parse(data);
  } catch (err) {
    return res.status(500).json({ message: "Error reading user data" });
  }

  const user = users.find((u) => u.email === email && u.password === password);

  if (!user) {
    return res.status(401).json({ message: "Invalid email or password" });
  }

  res.status(200).json({
    message: "Login successful",
    user: { name: user.name, email: user.email, occupation: user.occupation },
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
