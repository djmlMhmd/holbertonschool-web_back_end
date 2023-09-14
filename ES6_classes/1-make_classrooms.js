import ClassRoom from './0-classroom';

function initializeRooms() {
  const size_rooms = [19, 20, 24];
  const rooms = size_rooms.map((size) => new ClassRoom(size));
  return rooms;
}
