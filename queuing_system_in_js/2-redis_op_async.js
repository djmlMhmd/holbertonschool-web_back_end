import redis from 'redis';
import util from 'util';

const client = redis.createClient();
client.on('error', (err) => console.log('Redis client not connected to the server:', err));
client.on('connect', () => console.log('Redis client connected to the server'));

// Promisify get method of the Redis client
const getAsync = util.promisify(client.get).bind(client);

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

async function displaySchoolValue(schoolName) {
  const result = await getAsync(schoolName);
  console.log(result);
}

async function callAll() {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
}

callAll();
