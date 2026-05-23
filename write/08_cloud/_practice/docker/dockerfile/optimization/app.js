// 최적화 비교용 간단한 Express 앱
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send('Dockerfile optimization demo');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
