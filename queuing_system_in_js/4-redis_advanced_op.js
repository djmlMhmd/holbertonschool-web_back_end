import redis from 'redis';

const client = redis.createClient();

client.on('error', (err) => console.log('Redis client not connected to the server:', err));
client.on('connect', () => console.log('Redis client connected to the server'));

const schools = {
  Portland: 50,
  Seattle: 80,
  'New York': 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2,
};

for (const [city, number] of Object.entries(schools)) {
  client.HSET('HolbertonSchools', city, number, redis.print);
}

client.HGETALL('HolbertonSchools', (err, data) => {
  console.log(data);
});
