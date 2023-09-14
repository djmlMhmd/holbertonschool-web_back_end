import ClassRoom from './0-classroom';

function initializeRooms() {
  const sizeRooms = [19, 20, 34];
  const rooms = sizeRooms.map((size) => new ClassRoom(size));
  return rooms;
}
