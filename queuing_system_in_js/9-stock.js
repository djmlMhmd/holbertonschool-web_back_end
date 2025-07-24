const express = require('express');
const redis = require('redis');

const port = 1245;
const app = express();
const client = redis.createClient();

const listProducts = [
  {
    id: 1,
    name: 'Suitcase 250',
    price: 50,
    stock: 4,
  },
  {
    id: 2,
    name: 'Suitcase 450',
    price: 100,
    stock: 10,
  },
  {
    id: 3,
    name: 'Suitcase 650',
    price: 350,
    stock: 2,
  },
  {
    id: 4,
    name: 'Suitcase 1050',
    price: 550,
    stock: 5,
  },
];

function getItemById(id) {
  for (const product of listProducts) {
    if (product.id === id) { return product; }
  }
}

function reserveStockById(itemId, stock) {
  return new Promise((resolve, reject) => {
    client.get(`item.${itemId}`, (err, existingStock) => {
      if (err) { reject(err); } else if (existingStock === null) {
        client.set(`item.${itemId}`, stock, (err) => {
          if (err) { reject(err); } else { resolve(); }
        });
      } else {
        resolve();
      }
    });
  });
}

async function getCurrentReservedStockById(itemId) {
  const stock = await client.get(`item.${itemId}`);

  if (stock === null) {
    throw new Error(`No reserved stock found for item ${itemId}`);
  }
  const reservedStock = parseInt(stock, 10);
  return reservedStock;
}

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', (req, res) => {
  const item = getItemById(Number(req.params.itemId));
  if (!item) {
    res.status(404).json({ status: 'Product not found' });
  } else {
    const currentReservedStock = getCurrentReservedStockById(item.id);
    currentReservedStock.then((reservedStock) => {
      const itemObjectToReturn = {
        itemId: item.id,
        itemName: item.name,
        price: item.price,
        initialAvailableQuantity: item.stock,
        currentQuantity: item.stock - reservedStock,
      };
      res.status(200).json(itemObjectToReturn);
    }).catch((error) => {
      res.status(500).json({ status: 'Internal server error', error: error.message });
    });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  const item = getItemById(itemId);
  const stock = await getCurrentReservedStockById(itemId);
  const noStock = {
    status: 'Not enough stock available',
    itemId,
  };

  if (item === undefined) {
    res.json({ status: 'Product not found' });
    return;
  }

  if (stock === null) {
    reserveStockById(itemId, item.initialAvailableQuantity - 1);
  } else {
    if (stock < 1) {
      res.json(noStock);
      return;
    }
    reserveStockById(itemId, stock - 1);
  }

  res.json({
    status: 'Reservation confirmed',
    itemId,
  });
});

app.listen(port, () => {
  console.log('App started');
});
