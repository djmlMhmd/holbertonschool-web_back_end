// 4-update_grade_by_city.js

export default function updateStudentGradeByCity(students, city, newGrades) {
  const filteredStudentGrade = students.filter(
    (student) => student.location === city,
  );

  const updateStudents = filteredStudentGrade.map((student) => {
    const gradeObject = newGrades.find(
      (grade) => grade.studentId === student.id,
    );

    if (gradeObject) {
      return { ...student, grade: gradeObject.grade };
    }
    return { ...student, grade: 'N/A' };
  });

  return updateStudents;
}
