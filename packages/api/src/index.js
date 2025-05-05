const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.send("API scaffold up and running");
});

app.listen(PORT, () => {
  console.log(`API listening on http://localhost:${PORT}`);
});
