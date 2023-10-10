// 2-get_students_by_loc.js

export default function getStudentsByLocation(students, city) {
  const filterStrudent = students.filter(
    (student) => student.location === city,
  );

  return filterStrudent;
}
