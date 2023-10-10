// 1-get_list_student_ids.js

export default function getListStudentIds(PreviousTask) {
  if (!Array.isArray(PreviousTask)) {
    return [];
  }

  const ids = PreviousTask.map((student) => student.id);
  return ids;
}
