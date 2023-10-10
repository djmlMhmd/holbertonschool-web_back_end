// 3-get_ids_sum.js

export default function getStudentIdsSum(students) {
  const sumIdStudent = students.reduce((sum, student) => sum + student.id, 0);
  return sumIdStudent;
}
